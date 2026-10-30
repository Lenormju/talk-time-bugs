#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Mini serveur local pour la démo NTP en direct (slide 07-01).

Lancer :   ./ntp.sh   (ou uv run scripts/ntp_server.py)   (127.0.0.1:8123)
Options :  --port N   --no-udp (force le repli HTTP Date)

GET /ntp -> JSON. Cascade : NTP/UDP 123 (fr.pool.ntp.org puis pool.ntp.org),
sinon en-tête HTTP Date (précision ±1 s, ni stratum ni refid).
Pas de dépendance (socket + struct + http.server).
"""
import argparse, errno, json, os, socket, struct, sys, time, urllib.request
from email.utils import parsedate_to_datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

NTP_EPOCH = 2208988800  # secondes entre 1900 et 1970
NTP_SERVERS = ["fr.pool.ntp.org", "pool.ntp.org"]
HTTP_URL = "https://www.google.com"
NO_UDP = False
COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ


def log(msg, color=""):
    now = time.time()
    ts = time.strftime("%H:%M:%S", time.localtime(now)) + f".{int(now % 1 * 1000):03d}"
    if COLOR:
        print(f"\033[2m{ts}\033[0m {color}{msg}\033[0m", flush=True)
    else:
        print(f"{ts} {msg}", flush=True)


CYAN, GREEN, YELLOW, RED = "\033[36m", "\033[32m", "\033[33m", "\033[31m"


def ntp_now():
    return time.time() + NTP_EPOCH


def to_unix(buf, off):
    """Timestamp NTP 64 bits -> secondes Unix (None si zéro)."""
    s, f = struct.unpack("!II", buf[off:off + 8])
    if s == 0 and f == 0:
        return None
    return s + f / 2**32 - NTP_EPOCH


def short_fmt(buf, off):
    """Format NTP 'short' 16.16 -> secondes."""
    return struct.unpack("!I", buf[off:off + 4])[0] / 65536


def iso(t):
    if t is None:
        return None
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(t)) + f".{int((t % 1) * 1e6):06d}Z"


LI = {0: "pas d'alerte", 1: "dernière minute de 61 s", 2: "dernière minute de 59 s", 3: "horloge non synchronisée"}
MODES = {1: "symétrique actif", 2: "symétrique passif", 3: "client", 4: "serveur", 5: "broadcast"}


def query_ntp(host, timeout=2.0):
    pkt = bytearray(48)
    pkt[0] = (0 << 6) | (4 << 3) | 3  # LI=0, VN=4, mode=3 (client)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(timeout)
        ip = socket.gethostbyname(host)
        log(f"→ NTP : requête envoyée à {host} ({ip}:123)", CYAN)
        t1 = time.time()
        s.sendto(bytes(pkt), (ip, 123))
        data, addr = s.recvfrom(512)
        t4 = time.time()
    if len(data) < 48:
        raise ValueError("réponse NTP trop courte")
    li, vn, mode = data[0] >> 6, (data[0] >> 3) & 7, data[0] & 7
    stratum = data[1]
    if stratum == 0:
        raise ValueError("kiss-of-death")
    t2, t3 = to_unix(data, 32), to_unix(data, 40)
    ref = to_unix(data, 16)
    raw = data[12:16]
    if stratum == 1:
        refid_kind, refid = "texte", raw.rstrip(b"\0").decode("ascii", "replace")
    else:
        refid_kind, refid = "IPv4 du serveur amont (ou hash)", ".".join(str(b) for b in raw)
    off = ((t2 - t1) + (t3 - t4)) / 2 * 1000
    log(f"← NTP : réponse reçue en {(t4 - t1) * 1000:.0f} ms · stratum {stratum} · offset {off:+.0f} ms".replace("-", "−"), GREEN)
    return {
        "source": "ntp",
        "server": host,
        "server_ip": addr[0],
        "leap": li,
        "leap_text": LI.get(li, "?"),
        "version": vn,
        "mode": mode,
        "mode_text": MODES.get(mode, "?"),
        "stratum": stratum,
        "poll": data[2],  # log2 secondes
        "precision": struct.unpack("!b", data[3:4])[0],  # log2 secondes
        "root_delay_ms": short_fmt(data, 4) * 1000,
        "root_dispersion_ms": short_fmt(data, 8) * 1000,
        "refid": refid,
        "refid_raw": raw.hex(),
        "refid_kind": refid_kind,
        "reference_time": iso(ref),
        "t1_origin": iso(t1),
        "t2_receive": iso(t2),
        "t3_transmit": iso(t3),
        "t4_destination": iso(t4),
        "offset_ms": ((t2 - t1) + (t3 - t4)) / 2 * 1000,
        "delay_ms": ((t4 - t1) - (t3 - t2)) * 1000,
        "server_time_ms": int(t3 * 1000),
    }


def query_http_date(url=HTTP_URL, timeout=3.0):
    req = urllib.request.Request(url, method="HEAD")
    log(f"→ HTTP : HEAD {url.split('//')[-1]}", CYAN)
    t1 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        date = r.headers["Date"]
    t4 = time.time()
    server_s = parsedate_to_datetime(date).timestamp()  # précision 1 s
    log(f"← HTTP : en-tête Date reçu ({date}) en {(t4 - t1) * 1000:.0f} ms · précision ±1 s", GREEN)
    mid = (t1 + t4) / 2
    return {
        "source": "http-date",
        "server": url,
        "stratum": None,
        "refid": None,
        "t1_origin": iso(t1),
        "t3_transmit": iso(server_s),
        "t4_destination": iso(t4),
        "offset_ms": (server_s + 0.5 - mid) * 1000,  # +0.5 s : troncature
        "delay_ms": (t4 - t1) * 1000,
        "precision_s": 1,
        "server_time_ms": int(server_s * 1000),
    }


def measure():
    errors = []
    if not NO_UDP:
        for host in NTP_SERVERS:
            try:
                return query_ntp(host)
            except Exception as e:
                errors.append(f"{host}: {e!r}")
                why = "délai dépassé" if isinstance(e, socket.timeout) else type(e).__name__
                log(f"✗ NTP : échec UDP vers {host} ({why})", YELLOW)
    try:
        res = query_http_date()
        res["errors"] = errors
        return res
    except Exception as e:
        errors.append(f"http: {e!r}")
        log(f"✗ HTTP : échec ({type(e).__name__})", RED)
        raise RuntimeError("; ".join(errors))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # remplace le log par défaut de http.server
        pass

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Max-Age", "600")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self.path.split("?")[0] != "/ntp":
            code, body = 404, {"error": "not found"}
        else:
            log("GET /ntp", "\033[1m")
            try:
                res = measure()
                res["measured_at_ms"] = int(time.time() * 1000)
                code, body = 200, res
            except Exception as e:
                code, body = 502, {"error": str(e)}
        raw = json.dumps(body).encode()
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8123)
    ap.add_argument("--no-udp", action="store_true", help="saute NTP, force HTTP Date")
    a = ap.parse_args()
    NO_UDP = a.no_udp
    try:
        server = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            log(f"✗ Port {a.port} déjà utilisé : relancer avec --port N (et adapter l'URL du composant)", RED)
        else:
            log(f"✗ Impossible de démarrer le serveur : {e}", RED)
        sys.exit(1)
    log(f"Serveur NTP de démo : http://127.0.0.1:{a.port}/ntp" + (" (UDP désactivé)" if NO_UDP else ""))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    log("Serveur arrêté")
