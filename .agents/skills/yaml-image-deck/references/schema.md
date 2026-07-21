# YAML Schema

Use four layers:

1. `deck`: audience, purpose, mode, slide count, output.
2. `canvas` and `design_system`: fixed ratio, safe area, palette, visual direction, rounded typography, negative prompt.
3. `layout_router` and `layout_library`: controlled layout choices.
4. `slides`: page-specific teaching or communication data.

Required top-level keys:

```yaml
schema_version: "yaml_image_deck_v1"
deck: {}
canvas: {}
design_system: {}
layout_router: {}
slides: []
validation: {}
```

Required slide keys:

```yaml
- page: 1
  role: "cover"
  core_point: "One claim"
  semantic_structure: "focus"
  layout: {id: "cover_hero", variant: "left_title_right_visual"}
  visible_text: {title: "Short title"}
  visual: "Concrete image brief"
  output: "slides/images/page_01.png"
```

Use percentage zones for image prompting. Use PowerPoint coordinates only in a separate `overlay_blocks` section for `plate` mode.

Keep keys and enum values in English. Content may use the audience language.

