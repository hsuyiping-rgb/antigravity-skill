---
name: yaml-image-deck
description: Create consistent image-first slide decks from a structured YAML design system, layout registry, and per-slide content. Use when the user asks for a YAML image deck, NotebookLM-style image presentation, full-image PPTX, fixed visual grammar with controlled layouts, golden-sample style locking, or batch image slides across any subject. Supports baked slides and text-free plates with editable overlays.
---

# YAML Image Deck

Turn structured content into a consistent full-image presentation. Treat YAML as a design contract and prompt compiler input, not as pixel-perfect rendering code.

## Configuration Axes

- `output_mode`: `baked` or `plate`.
- `planning_mode`: `quick` or `yaml_spec`.
- `generation_strategy`: `sequential` or `subagents`.
- `style_lock`: `none` or `golden_sample`.

Default to `yaml_spec`, `sequential`, and `golden_sample`. Use `subagents` only when the user explicitly requests parallel generation and the active environment permits it.

## Hard Rules

- Use Antigravity built-in image generation by default. Do not require an API key unless the user explicitly selects an API/CLI workflow.
- Generate every slide visual with image generation before packaging. Local tools may crop, validate, montage, and package; they must not replace AI-generated slide art.
- Keep one core claim per slide and visible Chinese text short.
- Use a 16:9 target canvas and keep critical content inside the YAML safe area.
- Preserve each final image in the project; never leave project assets only under the built-in generated-images directory.
- Visually inspect every slide and the full montage before delivery.

## Rounded Typography Policy

The default visual language must use bold rounded Traditional Chinese lettering: thick strokes, generous counters, soft terminals, low corner sharpness, and no narrow mechanical forms.

For `baked` slides, repeat this typography direction in every image prompt and prohibit angular, condensed, high-contrast, or techno-stencil Chinese type.

For `plate` slides, use the first installed font from:

1. `jf open 粉圓 2.1`
2. `GenSenRounded TW`
3. `源柔ゴシック` / `GenJyuuGothic`

If none is installed, report the missing rounded Chinese font before final packaging. Do not silently substitute an angular default. Read `references/prompting.md` for the exact prompt tokens.

## Workflow

1. Define the communication job, audience, central takeaway, and slide count.
2. Create or normalize `spec.yaml` from `assets/spec-template.yaml`.
3. Assign each slide a semantic relationship and a fixed `layout.id`. Read `references/layout-library.md`.
4. Validate the spec:

   ```powershell
   python .\scripts\validate_spec.py --spec .\spec.yaml
   ```

5. Compile each prompt in this order: canvas and safe area, layout, page visual, exact text, global style, typography, reference image, negative constraints.
6. Generate one representative content slide first. Review it as the golden sample and save its path into `design_system.style_reference`.
7. Generate remaining slides one image call per slide. When explicit parallel generation is requested, read `references/subagent-batching.md` and give every worker the same YAML and golden sample.
8. Inspect exact text, layout, subject count, safe area, rounded typography, and style consistency. Regenerate only failed pages.
9. Run output verification:

   ```powershell
   python .\scripts\verify_images.py --spec .\spec.yaml --images-dir .\slides\images
   ```

10. Package through the active presentation workflow. In Antigravity, use the Presentations skill and Artifact Tool; embed one full-bleed image per slide, render the exported PPTX, inspect a montage, and run overflow checks.
11. Report the PPTX path, mode, source-image folder, spec path, and final prompt records.

## Output Modes

- `baked`: text is rendered inside each image. Use for fast demos, social sharing, and visual storytelling.
- `plate`: image generation produces a text-free designed plate with reserved zones; editable PowerPoint text is applied afterward. Use for revisions, dense Chinese, formulas, exact data, and long-lived decks.

Keep formulas, precise geometry, charts, and numeric evidence native/editable whenever correctness matters.

## References

- Read `references/schema.md` when creating or changing YAML fields.
- Read `references/layout-library.md` before routing slides.
- Read `references/prompting.md` before image generation.
- Read `references/subagent-batching.md` when the user requests parallel generation.
- Read `references/validation.md` before packaging and delivery.

