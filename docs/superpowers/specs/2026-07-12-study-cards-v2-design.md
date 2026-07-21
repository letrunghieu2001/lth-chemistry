# LTH Chemistry Study Cards v2 — Design Spec

## Goal

Redesign the LTH Chemistry Facebook automation pipeline to produce **dense, self-contained educational images** (Study Cards) paired with **short chemistry history captions**. The image carries the full educational payload; the caption is supplementary context only.

## Current Problems

1. **Image has too much whitespace** — content box is large but text is sparse, creating dead space between title and chibi characters
2. **Caption is generic** — mentor-style text doesn't differentiate from other edu pages
3. **Character roster is limited** — only 8 anime characters, gets repetitive
4. **Image ≠ content** — current design treats image as "illustration + text overlay" rather than a complete knowledge unit

---

## Design: Two Components

### Component 1: Caption — "Chemistry History Hook"

Each post caption is a **2-3 sentence chemistry history/trivia hook** that connects to the day's topic. AI randomly selects one of two styles per post:

#### Style A — Story Hook
> "Năm 1774, Lavoisier đốt kim cương trong bình kín và phát hiện nó biến thành CO₂ — chứng minh kim cương chỉ là carbon. Bài hôm nay thầy nói về carbon nhé 👇"

#### Style B — Mini Trivia
> "Bạn biết không? Cơ thể người có đủ carbon để làm 9000 chiếc bút chì. Xem ảnh thầy giải thích thêm! 🧪"

**Rules:**
- Max 40-60 words (2-3 sentences)
- Always tie a real historical fact or trivia to the post topic
- End with a soft CTA pointing to the image: "xem ảnh", "👇"
- 1-2 emoji max, no spam
- Written in Thầy Hiếu's voice (mentor, casual, passionate)
- NO chemical formulas in caption (image handles that)

**Content generator change:** Replace the current `caption` field (80-150 words, mentor explanation) with a new `status` field (40-60 words, history hook). Add `caption_style` field that the AI randomly picks: `"story_hook"` or `"mini_trivia"`.

---

### Component 2: Image — "Dense Study Card"

A compact, information-dense educational card where **every pixel has a purpose**.

#### Layout (1080×1080)

```
┌──────────────────────────────────────┐
│ KHTN Lớp 9          [LTH Logo]      │  ← Header: 50px, grade + logo
├──────────────────────────────────────┤
│                                      │
│     TIÊU ĐỀ NGẮN GỌN               │  ← Title: bold, gold, max 6 words
│     ─────────────                    │     1 line only
│                                      │
│     • Bullet point 1 (~10 từ)        │  ← Content: 3-4 bullet points
│     • Bullet point 2 (~10 từ)        │     Each max 10-12 words
│     • Bullet point 3 (~10 từ)        │     White text on dark BG
│     • Bullet point 4 (~10 từ)        │
│                                      │
│              [CHIBI]                 │  ← Character integrated in scene
│                                      │
│  fb.com/LTHChemistry                 │  ← Footer: 35px
└──────────────────────────────────────┘
```

#### Key Changes from v1

| Aspect | v1 (Current) | v2 (New) |
|--------|-------------|----------|
| Content box | Large semi-transparent box | No box — text directly on AI background |
| `image_content` | 1 paragraph (~35 words) | 3-4 bullet points (each ~10 words) |
| AI visual density | Sparse, lots of empty space | Dense scene — fill entire frame |
| Margins | 35px padding | 20px padding |
| Content area | 40% of image | Text occupies top 55%, visual fills 100% |
| Type label | "CÓ BIẾT KHÔNG?" banner | Removed — grade label only |
| Title size | 40px | 36px |
| Content size | 30px | 26px |

#### AI Visual Prompt Changes

The image prompt must instruct the AI to generate a **dense background scene**:
- "Fill the entire frame, no empty areas"
- "Dark navy/teal chemistry laboratory backdrop"
- "Molecular structures, beakers, periodic table elements scattered throughout"
- Characters positioned naturally within the scene, not isolated in corners

#### Content Format Change

**Before (v1):**
```json
{
  "image_title": "Nồng độ dung dịch",
  "image_content": "Nồng độ dung dịch là đại lượng cho biết lượng chất tan có trong một lượng dung dịch..."
}
```

**After (v2):**
```json
{
  "image_title": "NỒNG ĐỘ DUNG DỊCH",
  "image_bullets": [
    "C% = (m chất tan / m dung dịch) × 100%",
    "CM = n chất tan / V dung dịch (mol/L)",
    "m dung dịch = m chất tan + m dung môi",
    "Pha loãng: C1·V1 = C2·V2"
  ]
}
```

#### Quiz Layout (quiz_mcq type)

For quiz posts, the bullets become the question + 4 answer options:

```json
{
  "image_title": "TRẮC NGHIỆM",
  "image_bullets": [
    "Hòa tan m gam NaCl vào 200g nước,",
    "nồng độ 10%. Giá trị m là?"
  ],
  "quiz_options": ["A. 20,0g", "B. 22,2g", "C. 25,0g", "D. 18,5g"],
  "quiz_answer": "B"
}
```

---

### Component 3: Expanded Character Roster

From 8 anime characters to **24 characters** across 6 categories:

#### Anime (7)
| Name | Description | Preferred Types |
|------|-------------|----------------|
| doraemon | Blue robot cat pulling chemistry beaker from pocket | fun_facts, chemistry_around_us |
| conan | Detective boy with glasses examining molecules with magnifying glass | quiz_mcq, review_question |
| naruto | Ninja with spiky blonde hair, chemistry jutsu hand signs | mnemonic_tips |
| luffy | Pirate with straw hat grabbing periodic table element card | common_mistakes |
| nobita | Sleepy student suddenly excited reading chemistry textbook | exam_countdown |
| goku | Spiky-haired warrior with chemical energy aura | fun_facts |
| kiki | Young witch stirring chemistry cauldron | chemistry_around_us |

#### Marvel (4)
| Name | Description | Preferred Types |
|------|-------------|----------------|
| spider_man | Friendly web-slinging hero connecting molecular bonds with webs | common_mistakes, review_question |
| iron_man | Armored genius hero analyzing holographic periodic table | mnemonic_tips, review_question |
| hulk | Giant green hero smashing atoms apart (fission visual) | fun_facts |
| dr_strange | Sorcerer hero opening portals with chemistry symbols | quiz_mcq |

#### Disney/Pixar (4)
| Name | Description | Preferred Types |
|------|-------------|----------------|
| elsa | Ice princess creating crystalline molecular structures | chemistry_around_us |
| buzz | Space ranger astronaut scanning alien chemical compounds | fun_facts |
| remy | Chef rat mixing colorful chemical solutions in beakers | chemistry_around_us |
| baymax | Friendly healthcare robot analyzing molecular diagrams | common_mistakes |

#### Football (3)
| Name | Description | Preferred Types |
|------|-------------|----------------|
| messi | Football star juggling atom models like footballs | exam_countdown |
| ronaldo | Athletic star doing chemistry goal celebration with test tubes | mnemonic_tips |
| mbappe | Speed star racing past flying periodic table elements | exam_countdown |

#### Music (3)
| Name | Description | Preferred Types |
|------|-------------|----------------|
| kpop_idol | Stylish K-pop boy band member singing into molecule microphone | fun_facts |
| son_tung | Vietnamese pop star with chemistry-themed stage effects | chemistry_around_us |
| taylor | Pop diva writing chemistry formulas on glowing notebook | mnemonic_tips |

#### Science Legends (3) — Special guests, lower frequency
| Name | Description | Preferred Types |
|------|-------------|----------------|
| einstein | Wild-haired genius professor writing E=mc² on blackboard | review_question |
| marie_curie | Female scientist with glowing radium vials | fun_facts |
| mendeleev | Bearded chemist arranging periodic table cards | quiz_mcq |

#### Selection Rules
- Random pick from roster, **weighted by post type preference**
- **No repeat within last 3 posts** (up from 1)
- Science legends appear with **0.5× weight** (special guest frequency)
- All rendered as **chibi/cute fan art style** for brand consistency

---

## Pipeline Changes Summary

### Files to modify:

#### config.py
- Expand `CHIBI_GUEST_CHARACTERS` from 8 → 24 entries
- Add `CAPTION_STYLES = ["story_hook", "mini_trivia"]`
- Adjust text sizes: title 36px, content 26px
- Reduce margins from 35px → 20px
- Remove `POST_TYPE_LABELS` from image (keep only in config for internal use)

#### content_generator.py
- Replace `caption` prompt → `status` (40-60 word history hook)
- Add `caption_style` random selection in prompt
- Replace `image_content` → `image_bullets` (list of 3-4 short strings)
- Update JSON schema accordingly
- Add explicit instruction: "status must contain a real chemistry history fact"

#### image_generator.py
- Redesign `_composite_text_overlay()`:
  - Remove content box (semi-transparent rectangle)
  - Remove type label banner
  - Render bullet points with "•" prefix, tighter spacing
  - Reduce all margins and padding
  - Move grade label to header strip with logo
- Update `_rewrite_prompt_for_chibi()`:
  - Add "dense scene, fill entire frame, no empty areas" instruction
  - Add "dark navy/teal chemistry laboratory backdrop covering full canvas"
- Update `pick_guest_character()`:
  - Track last 3 characters instead of last 1
  - Add weight system for science legends (0.5×)

#### test_preview.py
- Update sample data to use new `image_bullets` format
- Update caption to use `status` format with history hooks

### Files unchanged:
- daily_post.py (orchestrator — field names change but flow stays same)
- facebook_poster.py (posts caption + image, no structural change)
- state_manager.py (tracks character history — extend to track last 3)

---

## Verification Plan

### Automated
1. Run `test_preview.py` with updated formats — verify image output
2. Verify bullet text renders within bounds (no overflow)
3. OCR validation still catches garbled AI text

### Manual
1. Visual inspection of generated study card — whitespace, readability
2. Compare v1 vs v2 side-by-side
3. User reviews HTML preview in browser
