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
4. **Commit every two or three pages.** Canva editing transactions expire. Holding one
   open across a long build — especially with pauses to answer questions — loses
   everything uncommitted. This has already cost a full rebuild once.
5. Never touch the original deck — it is the backup.

### Layout inventory — `DAGQ1Ke7cIQ`

| Page | Layout | Use for |
|---|---|---|
| 1 | Cover — comic collage inside a tablet frame, red angular blocks, yellow burst holding the title, subtitle, logo bottom-right | Deck cover |
| 2 | TOC — crimson panel down the right edge, gold badges with icons beside each chapter, large image left | Table of contents |
| 3 | Tall portrait illustration left + card right | Opening / definition |
| 4 | **Five-column grid** — each column a bordered card: heading, body, image at the foot | Curriculum overview, any 5-part breakdown |
| 5–15 | **Image-and-card** — tilted image left + card right carrying an outlined heading and centred body | Almost every content slide |
| 16 | Image + logo left + card right | Tool / software intro |
| 17 | Portrait image left + card right with a bulleted list | Assignment |
| 18 | Card top + social icon cluster + logo | עקבו אחרינו closer |

Pages 5–15 are eleven variations of one layout — call it **image-and-card** with Tal, not
"workhorse", which meant nothing to him. Copy whichever variation's image proportions
match the picture you have.

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

### Canva's PowerPoint export drops the title outline

Confirmed by inspecting the exported file, not guessed: export any deck in this system to
PPTX and every white text run comes out as plain `FFFFFF` with no `<a:ln>`. The outline is
a Canva-only render effect. It happens on the **untouched reference deck** too, so it is
never caused by editing — do not go hunting for it in the design.

The damage is severe here because the design leans on the outline twice: the title crosses
onto white below the banner, and card headings are white on a near-white card. Without it
they vanish.

**The fix**, when Tal needs a working .pptx: export with `export-design`, download it, run
`fix-pptx-outlines.py` (in this skill folder) over it, and send him the repaired file. The
script injects `<a:ln>` on every white run at or above 20pt — titles and card headings get
it, dark body copy does not — with the stroke scaled to 4% of the type size. PDF and PNG
exports keep the effect and need no repair.

### Delivering a .pptx that fits the 30 MiB limit

The standing delivery pipeline: `export-design` with `export_quality: "pro"` → download →
`fix-pptx-outlines.py` → send. Slides always go out at pro quality; never lower it.

When the file lands over 30 MiB, the cost is almost always **an embedded video encoded far
larger than the slot it plays in**. Measure before degrading anything:

- **Images** — Canva already sizes these correctly. They are also RGBA cut-outs, so JPEG
  conversion is off the table and lossless PNG recompression saves nothing. Skip them.
- **Video** — compare the encode to its display size. Pull `<a:ext cx cy>` from the `<p:sp>`
  carrying the video relationship and convert EMU to slide pixels with `1920 / sldSz.cx`.
  In כתיבת תסריט the clip was 1920×888 but played in a 696×500 slot: three times the pixels
  anyone can see.

Re-encode to **2× the display width**, which stays retina-sharp in the frame:

```
ffmpeg -i vid.mp4 -vf "scale=<2x display width>:-2:flags=lanczos" \
       -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -c:a aac -b:a 128k out.mp4
```

18.75 MB → 12.3 MB, file 34.5 → 28.1 MiB, nothing visibly changed. Then swap the entry back
into the zip by name and re-verify with `testzip()`.

Plain CRF re-encoding at the original resolution is not worth it — Canva's encode is already
efficient, and CRF 22 bought only 1.5 MB. Downscaling to the slot is the move.

Tell Tal what changed and what the trade-off is: the clip is still 2× its on-slide size, so it
is identical inside the deck, but softer if he ever plays that file full-screen on its own.
ffmpeg comes from `pip install imageio-ffmpeg` — there is no system ffmpeg in the container.

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

### Two layouts the reference does not have

Two shapes recur in Tal's older decks and neither fits the reference's image-and-card or
five-column pages. Both are built the same way: take the **five-column** page (ref p4), delete
its column furniture, and keep the full-width card underneath.

- **Three portrait panels + one caption.** Panels 376 × 560 at `top 360`, lefts **356 / 772 /
  1188**, each with black stroke 4; the caption is one reused column-body text reformatted to
  40px, width 1620 at `top 278, left 150`.
- **Two wide strips stacked.** Grow the standard card to `1800.63 × 800` at `top 210, left
  59.68`, then strips 1100 wide at `top 320` and `top 648`.

For a **three-column** breakdown, keep three of the five column cards and widen each to
**573.17 × 662.32** at lefts **77.25 / 673.42 / 1269.59**; headings go to 40px, bodies to 32px.

**A title longer than ~13 characters** does not need a smaller font — widen its box instead and
re-centre it (`width 1300, left 310` holds ~19 characters at 121.481px). The size stays constant
across the deck, which is what reads as consistent; the box width is invisible.

**`insert_fill` and a re-purposed background image both land behind the card.** Anything you
place on top of a card needs `layer_element` to `front` afterwards, or it silently disappears —
the edit reports success and the thumbnail just shows white.

## API traps — learned the hard way

**`position_element` takes POST-rotation coordinates.** For a 90°-rotated element the stored `top`/`left` you read back are pre-rotation and differ by `(height − width) / 2`.

**Resize before positioning.** `resize_element` re-centres the element, discarding any position you just set.

**`crop_media` after every `update_fill` + `resize`.** Otherwise Canva keeps the old image box and the picture shows a random crop. Pass `top: 0, left: 0` and the element's new width/height.

**Check `rotation` before placing an image.** Several reference slots are rotated —
the image-and-card layout tilts its photo by 17.87°, and the assignment slot sits at
-90°. `update_fill` keeps the existing rotation, so a photo dropped into the -90° slot
renders on its side. Call `rotate_element` to 0 first, then resize, then position.

**Canva library elements cannot be transferred between designs.** An asset Tal picked
from Canva's own library — the gold TOC badge `MAEL5Bmn-RI`, for one — fails
`insert_fill` with "media bundle not found". Only his own uploads carry across. Draw a
substitute with `insert_shape`, or leave the slot empty and let him place it himself.

**The TOC page cannot be copied — rebuild it from these numbers.** Both the reference's
page 2 and Tal's own version in `DAHT3XvFzCc` carry an element the API reports as
`unsupported`, so `merge-designs` silently drops the whole page: you get one page fewer than
you asked for, with no error. Do **not** substitute the image-and-card layout — Tal checks
this slide against his other decks. Build it on a copied image-and-card page by stripping the
card and the top banner and laying out:

| | |
|---|---|
| Crimson panel | `545.6 × 1280` at `top -100, left 1810.9` · rounding 16 · stroke 4 — a vertical strip down the **right** edge; there is **no** horizontal banner on this page |
| Title | same 121.481px display type, but at `top 93.16, left 1059.03` (width 890.258) |
| Chapter list | one text element, no numbering, body font, centred · his is 36px |
| Chapter icons | `left ≈ 1737`, straddling the panel edge — roughly 45% of each icon on white, 55% on crimson |

The chapter list must be **one** text element: `add_text` cannot set a font, so six separate
lines would come out in the wrong typeface. Line pitch is therefore capped at
`font_size × 2.5` (the `line_height` maximum) — at 42px that is ~96px, which fits six rows
where his four sit at ~150. Scale the icons to match the tighter rhythm rather than
overlapping them.

**The gold badge behind each icon (`MAEL5Bmn-RI`) cannot be placed at all** — it is a Canva
library element, and `insert_fill` fails with `A media bundle required to process the request
was not found in resources.mediaFiles`. His four chapter icons (`MAGOlmkSCxM` `MAGOlgZ1bKw`
`MAGOliU7hjk` `MAGOlm3_Fu0`) are his own uploads and do insert. Place those, leave the badges,
and tell Tal — he adds them himself and has said so.

**Title width is capped at about 13 Hebrew characters** at 121.481px in the 890px box.
"ההיסטוריה של הקומיקס" overflows; "ההיסטוריה" fits. Push the rest of the phrase into
the card heading, which holds ~17 characters at 69.246px.

**Portrait images do not belong in full-bleed slots.** A 0.65-ratio photo stretched across 1920×1080 crops to an unrecognisable detail. Put it in a side panel instead.

**Hebrew gershayim is `״` (״), not `ע` (ע).** Getting this wrong silently turns every quotation mark into an ayin.

**Video works.** `update_fill` with `asset_type: "video"` swaps an uploaded Canva video. Tal edits and uploads his own videos — never offer to generate them.

## Content rules

- **Never drop content from the source deck.** Tal's rule, stated plainly: content wins
  over design fit. If an image, a caption, a credit line or a paragraph existed on the old
  slide, it belongs on the new one — even where it does not sit neatly in the layout.
  When something genuinely cannot fit, say so and offer an extra slide; do not quietly
  leave it out. He checks.
- **Diff the rebuilt deck against the source before handing it over.** Go slide by slide and
  compare the actual strings, not your memory of them. Four kinds of drift creep in and Tal
  catches all of them:
  - **Borrowed imagery.** An image that is in his Canva but not in *this* deck is still a
    substitution. When the source slide carried a drawn diagram, redraw that diagram — do not
    swap in a photo because it is easier.
  - **Invented card headings.** The new layout has a white heading slot the old decks did not,
    so it must be filled — but with a phrase lifted from that slide's own body text, never a
    fresh one you wrote. Say which ones you added.
  - **Rewritten phrasing.** ״ברור גם בקטן״ is not an invitation to write ״ברור גם כשמקטינים
    לגודל של ציפורן״. Keep his words.
  - **Collapsed structure.** A label on its own line (״בדקו את עצמכם:״) stays on its own line;
    a run of quotes keeps its original spacing.
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
- `DAHUWraekK8` — מבוא לאיור ואייקון דיגיטלי | קומיקס דיגיטלי — **the current version**, 12 pages,
  rebuilt on the new reference
- `DAHTZQw6jBw` — מבוא לאיור ואייקון דיגיטלי | מהדורת 2026 — the old Iron Man-language version it was
  rebuilt from; keep as the backup
- `DAHT3XvFzCc` — כתיבת תסריט לחוברת קומיקס | קומיקס דיגיטלי — **done, 11 pages**, first deck
  built on the new reference. Page 3 is a superseded table of contents awaiting Tal's deletion.
- `DAHTZhm6Fqc` — earlier partial attempt at the same deck on the old Iron Man language — superseded, Tal can delete
- `DAFuytczpME` — מצגת שיעור - ספיידרמן ודחייה חברתית — 9 pages, original, awaiting rebuild
- `DAHSNrccONo` — Iron Man — superseded as reference, keep for history
- `DAHTZaBP_SY` — abandoned first attempt, ignore

The full catalogue of all 81 presentations is at https://claude.ai/code/artifact/ce821a49-7453-4b59-8d7a-11c663adaa1b
