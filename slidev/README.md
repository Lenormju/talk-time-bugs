# Slidev presentation

Setup with `npm install`.

Run with `npm run dev` then visit <http://localhost:3030>.

## Notes on Slidev

Default layouts:
- `default`: Simple centered content
- `cover`: Title slide with large text
- `center`: Everything centered
- `two-cols`: Two-column layout
- `image-right`: Content left, image right
- `quote`: Styled blockquote
- `section`: Section divider
- `fact`: Big number/fact display

Special files for Slidev:
- `./global-top.vue`
- `./global-bottom.vue`
- `./custom-nav-controls.vue`

Custom components are auto-loaded from: `./components/*.vue`

Stateful logic is loaded from: `./composables`

The slides contents are in `./pages/*.md`, and imported from `./slides.md`

Javascript code that is not Vue-related can be loaded from `./snippets.js`
