---
name: heroes-academy-decks
description: Build and renew Hebrew Canva presentations for האקדמיה לגיבורים (Heroes Academy) comics curriculum. Use whenever the task involves Tal Amar's Canva decks — renewing an old lesson deck, building a new one, editing slides, swapping images or video, or matching the Iron Man design system. Triggers on "מצגת", "קאנווה", "שקופית", "האקדמיה לגיבורים", "קומיקס דיגיטלי", Canva design IDs, or any request to update lesson slides.
---

# Heroes Academy — Canva deck system

Tal Amar owns האקדמיה לגיבורים, which teaches comics and animation to **grades 3–6** (ages ~8–12) in Israeli schools. Decks are Hebrew, RTL, 1920×1080, one deck ≈ one 60–75 minute session.

## THE GOLDEN RULE

**Never build a slide from scratch. Always copy pages from the Iron Man reference deck and replace the content.**

Reference deck: **`DAHSNrccONo`** — "סדנת איירון מן - קומיקס דיגיטלי"

This is not a stylistic preference. Two things are **impossible** through the Canva API and only survive by copying a page:

1. **The black outline on white title text.** It is a Canva *text effect*. It does not appear in the element JSON at all — a title reads back as `{"color": "#ffffff"}` with no stroke. You cannot add it.
2. **Font family.** `format_text` has no font parameter, and `add_text` uses a default. Copied text elements keep the right fonts; new ones never will.

Building from scratch produces something that looks *almost* right and is therefore wrong. Tal will notice.

## Workflow

1. `merge-designs` with `type: create_new_design`, one `insert_pages` operation, `page_numbers` listing Iron Man pages in order — **duplicates are allowed**, e.g. `[1,3,3,4,2,2,3,6,6]`. Only one operation per request.
2. Harvest media IDs from the old deck (`read-design` with `open_transaction: true` — the ids only appear in a transaction read).
3. `read-design` the new deck for locator ids, then per page: `replace_text`, `update_fill`, `resize_element`, `position_element`, `crop_media`.
4. Commit. Never touch the original deck — it is the backup.

### Iron Man page layouts

| Page | Layout |
|---|---|
| 1 | Cover — full-bleed hero, yellow comic burst, title + subtitle, logo bottom-left |
| 2 | Tall image left + three stacked fact cards right |
| 3 | Tall media left + one large text card right — **the workhorse** |
| 4 | Wide text bar top + three images in a row |
| 5 | Video + text card + bottom image strip |
| 6 | Full-bleed image + task card — closing/assignment slide |

## Design tokens — exact values

| | |
|---|---|
| Canvas | 1920×1080, white background |
| Crimson banner | `#960b0b`, black stroke **6** |
| Banner geometry | stored `top: -1636.21, left: 503.33, width: 822.29, height: 2819.25, rotation: 90` |
| Title text | `YAGRfpd9t4I` · 128.014px · bold + italic · `#ffffff` · align start · lineHeight 1 · at `top 21.1, left 30.59, width 1840.12` |
| Body text | `YAG2sxXkTBU` · 36.4px · bold · `#000000` · lineHeight 1.74 |
| Grey card | `#d5d3d4` at opacity **0.21**, black stroke **4**, cornerRounding **0** |
| Image/video frame | black stroke 4 (6 on full-height media) |
| Card grid (p2) | left 1028.96, width 655.51, height 161.01, vertical pitch 261.67 |

Off-system colors that appear in old decks and must go: `#002c66` (navy connector lines), `#dd1414` / `#c61b1b` / `#fa2828` (extra reds), rounded pills (`cornerRounding: 51`).

## API traps — learned the hard way

**`position_element` takes POST-rotation coordinates.** For a 90°-rotated element the stored `top`/`left` you read back are pre-rotation and differ by `(height − width) / 2`. To land the banner on its canonical stored values, pass `top: -637.73, left: -495.15`.

**Resize before positioning.** `resize_element` re-centres the element, discarding any position you just set.

**`crop_media` after every `update_fill` + `resize`.** Otherwise Canva keeps the old image box and the picture shows a random crop. Pass `top: 0, left: 0` and the element's new width/height.

**Portrait images do not belong in full-bleed slots.** A 0.65-ratio photo stretched across 1920×1080 crops to an unrecognisable detail. Put it in a side panel instead.

**Video works.** `update_fill` with `asset_type: "video"` swaps an uploaded Canva video. Tal edits and uploads his own videos — never offer to generate them.

## Content rules

- Hebrew body copy, direct address to students (״זכרו…״, ״בחרו…״). Explanations in Hebrew even when the source material is English.
- Grades 3–6 do not read eight-line paragraphs. Split a dense slide into two rather than shrinking the type.
- English video is fine **with Hebrew subtitles** (Tal adds them in his own edit). Comic panels need no subtitles — they are visual.
- Sequence runs easy → hard across the curriculum.
- The academy writes inclusively: ״גיבורים.ות״.
- Keep Tal's facts. Tighten phrasing, never invent curriculum content without flagging it.

## Copyright — operative rules

An opinion by עו״ד אריאל דובינסקי covers Marvel/DC use under **§19 שימוש הוגן** of Israel's Copyright Act. It holds only while all four conditions hold:

1. Credit the creators.
2. Partial, proportionate use — never whole issues.
3. Teaching only. **Never** use this material to market or brand the courses.
4. No wide digital distribution beyond the classroom — do not publish these decks publicly.

## Assets already in Tal's Canva

`MAGO3pvU4rg` academy logo · `MAFFlAHmZ4I` yellow comic burst · `MAGdrxx6z7s` Marvel icon pattern · `MAFqqanf2cg` Hulk vs Spider-Man

## Decks

- `DAHTZQw6jBw` — מבוא לאיור ואייקון דיגיטלי | מהדורת 2026 — **done, 10 pages**
- `DAHTZhm6Fqc` — כתיבת תסריט לחוברת קומיקס | מהדורת 2026 — cover done, 8 pages still holding Iron Man content
- `DAHTZaBP_SY` — abandoned first attempt, superseded, ignore

The full catalogue of all 81 presentations is at https://claude.ai/code/artifact/ce821a49-7453-4b59-8d7a-11c663adaa1b
