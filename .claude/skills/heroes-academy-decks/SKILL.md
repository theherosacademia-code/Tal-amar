---
name: heroes-academy-decks
description: Build and renew Hebrew Canva presentations for האקדמיה לגיבורים (Heroes Academy) comics curriculum. Use whenever the task involves Tal Amar's Canva decks — renewing an old lesson deck, building a new one, editing slides, swapping images or video, or matching the קומיקס דיגיטלי design system. Triggers on "מצגת", "קאנווה", "שקופית", "האקדמיה לגיבורים", "קומיקס דיגיטלי", Canva design IDs, or any request to update lesson slides.
---

# Heroes Academy — Canva deck system

Tal Amar owns האקדמיה לגיבורים, which teaches comics and animation to **grades 3–6** (ages ~8–12) in Israeli schools. Decks are Hebrew, RTL, 1920×1080, one deck ≈ one 60–75 minute session.

## THE GOLDEN RULE

**Never build a slide from scratch. Always copy pages from the reference deck and replace the content.**

Reference deck: **`DAGQ1Ke7cIQ`** — "קומיקס דיגיטלי", 18 pages. Tal authored it in Aug 2026 as the
canonical design language for every deck. It **supersedes** the old Iron Man deck
(`DAHSNrccONo`), which is now only of historical interest — do not build from it.

This is not a stylistic preference. Two things are **impossible** through the Canva API and only survive by copying a page:

1. **The black outline on white text.** It is a Canva *text effect*. It does not appear in the element JSON at all — a title reads back as `{"color": "#ffffff"}` with no stroke. You cannot add it. It is load-bearing: it is the only reason white titles stay legible where they cross onto white, and the only reason white card headings work on a near-white card.
2. **Font family.** `format_text` has no font parameter, and `add_text` uses a default. Copied text elements keep the right fonts; new ones never will.

Building from scratch produces something that looks *almost* right and is therefore wrong. Tal will notice.

## Workflow

1. `merge-designs` with `type: create_new_design`, one `insert_pages` operation, `page_numbers` listing reference pages in order — **duplicates are allowed**, e.g. `[1,2,3,7,7,7,4,17,18]`. Only one operation per request.
2. Harvest media IDs from the old deck (`read-design` with `open_transaction: true` — the ids only appear in a transaction read).
3. `read-design` the new deck for locator ids, then per page: `replace_text`, `update_fill`, `resize_element`, `position_element`, `crop_media`.
4. Commit. Never touch the original deck — it is the backup.

### Layout inventory — `DAGQ1Ke7cIQ`

| Page | Layout | Use for |
|---|---|---|
| 1 | Cover — comic collage inside a tablet frame, red angular blocks, yellow burst holding the title, subtitle, logo bottom-right | Deck cover |
| 2 | TOC — crimson panel down the right edge, gold badges with icons beside each chapter, large image left | Table of contents |
| 3 | Tall portrait illustration left + card right | Opening / definition |
| 4 | **Five-column grid** — each column a bordered card: heading, body, image at the foot | Curriculum overview, any 5-part breakdown |
| 5–15 | **The workhorse** — image left + card right carrying an outlined heading and centred body | Almost every content slide |
| 16 | Image + logo left + card right | Tool / software intro |
| 17 | Portrait image left + card right with a bulleted list | Assignment |
| 18 | Card top + social icon cluster + logo | עקבו אחרינו closer |

Pages 5–15 are eleven variations of one layout. Copy whichever one's image proportions match the picture you have.

## Design tokens — exact values

| | |
|---|---|
| Canvas | 1920×1080, white background |
| Crimson | `#960b0b` · secondary red `#c61b1b` (cover only) · yellow `#fdf03d` |
| Body ink | `#231f20` — **not** pure black |
| Card | `#f7f8f8` (columns: `#fffcfc`) · **opacity 1** · black stroke **4** · cornerRounding 0 |
| Display font | **`YAG2s6gDzUY`** — titles, card headings, column headings |
| Body font | `YAG2sxXkTBU` |
| Cover subtitle font | `YAFwAZ01Tmw` · 33.786px · normal weight |
| Banner | rot 90 · stored `top -1189.869, left 838.447, width 243.106, height 2316.810` · `#960b0b` · stroke 4 |
| Banner visual span | y `0 → 90.09`, x `-198.4 → 2118.4` (it deliberately overhangs both edges) |
| Title | `top 35.148, left 514.871, width 890.258` · **121.481px** · bold + italic · `#ffffff` · **center** · lineHeight **1.4** |
| Cover title | 160.942px, same font |
| Card — standard | `top 231.79, left 807.97, 1341.62 × 704.36` |
| Card — full width | `top 244.42, left 59.68, 1800.63 × 704.36` |
| Card body | **45.181px** · bold · `#231f20` · **center** · lineHeight 1.4 |
| Column card | `334.216 × 662.321` · top `265.444` · lefts `77.25 / 434.59 / 791.92 / 1149.25 / 1506.58` (pitch **357.331**) |
| Column heading | 27.091px · bold + italic · `#ffffff` (outlined) · center |
| Column body | 25.106px · bold · `#231f20` · center · lineHeight 1.4 |
| Corner watermark | `MAG0d6qCfTo` at `top 0, left 1399.29, 524.59 × 523.28`, **opacity 0.11**, flipX + flipY |

Body copy in this system is **centred**, not start-aligned. That is a deliberate change from
the old Iron Man decks — do not "correct" it back.

### The banner CUTS the title — non-negotiable

The crimson banner's bottom edge **slices through the middle of the title**: the upper half of
the letterforms sits on crimson, the lower half on white. It is not a container. Do not "fix" a
title that hangs below the bar — that is the design. The black outline on the white title is
what makes it work; the outline and the cut are one idea and neither works alone.

The arithmetic, because it is not obvious: the banner is rotated 90°, so its *stored* `width` is
what you see as its height, and its visible bottom edge lands at `stored_width − 153.02`.

Applied per page as two ops in one call:

```
resize_element   width: 243.106, height: 2316.810   ← element-local, so resize first
position_element top: -153.02, left: -198.40        ← POST-rotation bounding box
```

Then check where the cut actually lands, because **a title's `top` alone does not predict it**.
Title elements copied from different source pages carry different internal line metrics even at
the same font size, and one that renders higher ends up sitting entirely inside the crimson with
no visible cut. Match the rendered result, not the number.

### Thumbnails lie — Tal's Canva view is the authority

The previews this tool returns are ~596×335 exports, roughly a third of full size, from a
different render path than the live editor. Two consequences, both of which have already cost a
round of pointless work:

- `read-design` thumbnails can come back **cached at an older document version**, showing a state
  that no longer exists.
- The **black outline is a text effect** and does not survive the small export faithfully, so how
  the crimson cut reads looks meaningfully different here than on screen.

So: `edit-design`'s after-thumbnail is the best check available and worth using to catch gross
errors, but it is not the verdict. When Tal says it looks right in Canva, it is right — do not
"fix" a slide against a preview he has not complained about. When a preview looks wrong but he
has not mentioned it, ask before acting.

## Drawing icons with `insert_shape`

Stock photography could not serve the icon-design slides — the useful images are watermarked
commercial stock. Vector shapes drawn straight into the page solve it, stay exactly on palette,
and scale perfectly. This is the preferred illustration route for any abstract concept.

**Recipe.** A tile is `M0 0H64V64H0z` with `corner_rounding` ≈ 22% of its width, fill `#960b0b`,
black stroke. A glyph sits on top at ~55% of the tile, fill `#ffffff`, `stroke_weight: 0`, centred
by hand: `glyph_left = tile_left + (tile − glyph) / 2`. `stroke_weight` is **absolute pixels**,
not viewBox units — 4 on big shapes, 2 on small. Only `M/L/H/V/C/S/A/Z` are supported; `Q` and `T`
are rejected.

Tested glyph paths, all on a 64×64 viewBox:

| Glyph | `d` |
|---|---|
| bolt | `M38 4L14 36H30L26 60L50 26H34L38 4Z` |
| shield | `M32 4L58 14V34C58 48 46 57 32 61C18 57 6 48 6 34V14Z` |
| star | `M32 4L40 24L62 24L44 37L51 58L32 45L13 58L20 37L2 24L24 24Z` |
| eye | `M2 32C2 32 14 14 32 14C50 14 62 32 62 32C62 32 50 50 32 50C14 50 2 32 2 32ZM32 42A10 10 0 1 0 32 22A10 10 0 1 0 32 42Z` |
| flame | `M32 2C32 2 12 24 12 38A20 20 0 0 0 52 38C52 24 32 2 32 2Z` |
| plus | `M26 4H38V26H60V38H38V60H26V38H4V26H26Z` |
| circle | `M32 2A30 30 0 1 0 32 62A30 30 0 1 0 32 2Z` |
| rectangle | `M4 12H60V52H4Z` |
| triangle | `M32 6L60 56H4Z` |
| camera | `M12 20H20L24 14H40L44 20H52C55 20 58 23 58 26V48C58 51 55 54 52 54H12C9 54 6 51 6 48V26C6 23 9 20 12 20ZM32 46A12 12 0 1 0 32 22A12 12 0 1 0 32 46Z` |
| play | `M20 12L52 32L20 52Z` |

**A phone** is three shapes: black body (rounding ~64), white screen inset 20–25px (rounding ~42),
and a small black notch bar centred on the screen top. Drop a tile grid inside. An empty tile —
white fill, black stroke 4, no glyph — reads as "waiting for you to draw here", which is how an
assignment slide invites students in.

**Diagrams that teach.** A size ladder (one tile at 380 / 250 / 160 / 100 / 60, all sharing a
bottom baseline, largest on the right for RTL) shows scalability far better than any sentence.
Three grey tiles against one crimson tile shows uniqueness.

## Page structure — what needs Tal's word

`merge-designs` inserting pages from the reference deck is routine. Two things are not:

- **Deleting a page** requires Tal to type the exact phrase the tool demands. Never approximate
  it. When he asks for a slide to go, repurpose the page instead — replace its title and text with
  content that belongs at that point in the sequence — and tell him the page is still there if he
  wants it truly removed.
- **Reordering pages** he has declined once. Design around the existing order rather than
  proposing a move again.

## API traps — learned the hard way

**`position_element` takes POST-rotation coordinates.** For a 90°-rotated element the stored `top`/`left` you read back are pre-rotation and differ by `(height − width) / 2`.

**Resize before positioning.** `resize_element` re-centres the element, discarding any position you just set.

**`crop_media` after every `update_fill` + `resize`.** Otherwise Canva keeps the old image box and the picture shows a random crop. Pass `top: 0, left: 0` and the element's new width/height.

**Portrait images do not belong in full-bleed slots.** A 0.65-ratio photo stretched across 1920×1080 crops to an unrecognisable detail. Put it in a side panel instead.

**Hebrew gershayim is `״` (״), not `ע` (ע).** Getting this wrong silently turns every quotation mark into an ayin.

**Video works.** `update_fill` with `asset_type: "video"` swaps an uploaded Canva video. Tal edits and uploads his own videos — never offer to generate them.

## Content rules

- Hebrew body copy, direct address to students (״זכרו…״, ״בחרו…״). Explanations in Hebrew even when the source material is English.
- Grades 3–6 do not read eight-line paragraphs. Split a dense slide into two rather than shrinking the type.
- English video is fine **with Hebrew subtitles** (Tal adds them in his own edit; there is no Canva API operation for subtitles). Comic panels need no subtitles — they are visual.
- Sequence runs easy → hard across the curriculum.
- The academy writes inclusively: ״גיבורים.ות״.
- Keep Tal's facts. Tighten phrasing, never invent curriculum content without flagging it.

## Copyright — operative rules

An opinion by עו״ד אריאל דובינסקי covers Marvel/DC use under **§19 שימוש הוגן** of Israel's Copyright Act. It holds only while all four conditions hold:

1. Credit the creators.
2. Partial, proportionate use — never whole issues.
3. Teaching only. **Never** use this material to market or brand the courses.
4. No wide digital distribution beyond the classroom — do not publish these decks publicly.

Non-comic imagery is restricted to Unsplash / Pexels / Wikimedia. Never upload watermarked or
paid commercial stock into Tal's Canva. `upload-asset-from-url` accepts only already-public URLs —
never publish his private files to create one.

## Assets in Tal's Canva

**Reference deck:** `MAGpZ-dAQGs` cover collage · `MAEqOGm_aLE` tablet frame (two halves, one flipped) · `MAFFlAHmZ4I` yellow burst (recoloured `#ec1c24→#960b0b`, `#f9ec31→#fdf03d`) · `MAGO3pvU4rg` academy logo · `MAG0d6qCfTo` corner watermark · `MAEL5Bmn-RI` gold TOC badge · `MAGOlmkSCxM` `MAGOlgZ1bKw` `MAGOliU7hjk` `MAGOlm3_Fu0` TOC icons

**Comics:** `MAGdrxx6z7s` Marvel icon pattern · `MAFqqanf2cg` Hulk vs Spider-Man · `MAGsbH_IAmE` Spider-Man with camera · `MAGd9C28GlA` app icon grid

## Decks

- `DAGQ1Ke7cIQ` — קומיקס דיגיטלי — **the design reference**, 18 pages. Never modify.
- `DAHTZQw6jBw` — מבוא לאיור ואייקון דיגיטלי | מהדורת 2026 — done, 12 pages, built on the old Iron Man language
- `DAHTZhm6Fqc` — כתיבת תסריט לחוברת קומיקס | מהדורת 2026 — cover only, 8 pages still holding Iron Man content
- `DAFuytczpME` — מצגת שיעור - ספיידרמן ודחייה חברתית — 9 pages, original, awaiting rebuild
- `DAHSNrccONo` — Iron Man — superseded as reference, keep for history
- `DAHTZaBP_SY` — abandoned first attempt, ignore

The full catalogue of all 81 presentations is at https://claude.ai/code/artifact/ce821a49-7453-4b59-8d7a-11c663adaa1b
