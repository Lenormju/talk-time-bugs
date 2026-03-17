# Timeline Component Demo

<Timeline name="Seconds" unit="s" :start="58" :count="5" :highlights="[60]" :chunks="[[58,59], [60], [61,62]]" />

<Timeline name="Minutes" unit="m" :start="0" :count="5" :highlights="[1]" :chunks="[[0], [1], [2,3,4]]" />

<Timeline name="Hours" unit="h" :start="23" :count="4" :highlights="[0]" :chunks="[[23], [0], [1,2]]" />

---

# Leap Second Bug Demonstration

<TimelineBifurcating
  :main="{
    name: 'RFC-compliant system',
    unit: 's',
    start: 58,
    values: [58, 59, 60, 0, 1, 2],
    highlights: [60]
  }"
  :branches="[
    {
      name: 'System with leap second bug',
      splitAt: 60,
      values: [0, 1, 2, 3],
      highlights: [0]
    }
  ]"
  :chunks="[
    { reveals: [{ timeline: 'main', values: [58] }] },
    { reveals: [{ timeline: 'main', values: [59] }] },
    {
      reveals: [
        { timeline: 'main', values: [60] },  // Main shows 60
        { timeline: 0, values: [0] }          // Branch shows 0
      ]
    },
    {
      reveals: [
        { timeline: 'main', values: [0] },
        { timeline: 0, values: [1] }
      ]
    },
    {
      reveals: [
        { timeline: 'main', values: [1] },
        { timeline: 0, values: [2] }
      ]
    },
    {
      reveals: [
        { timeline: 'main', values: [2] },
        { timeline: 0, values: [3] }
      ]
    }
  ]"
/>

<v-click at="3">

**Bug:** System skips leap second (60s), jumping directly from 59s to 00s

</v-click>
