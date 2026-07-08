---
name: lth-facebook-content
description: Use when generating Facebook post content for LTH Chemistry tutoring page, daily chemistry review questions, or engagement posts targeting Vietnamese THCS/THPT students following SGK Ket noi tri thuc curriculum.
---

# LTH Chemistry Facebook content

## Overview

Generate daily Facebook posts for the LTH Chemistry tutoring page. Two posts per day: one for THCS (grades 6-9, KHTN), one for THPT (grades 10-12, Hoa hoc). All content follows SGK Ket noi tri thuc and must pass through the humanizer skill before publishing.

**REQUIRED SUB-SKILL:** Every piece of output text MUST be processed through `humanizer` before it is considered final. No exceptions.

## When to use

- Generating daily Facebook review questions for LTH Chemistry
- Creating engagement posts (fun facts, polls, common mistakes, mnemonics)
- Planning weekly content calendars for chemistry education Facebook pages
- Writing Vietnamese chemistry education content for social media

Do NOT use for: website copy, lesson plans, exam papers, or non-Facebook content.

## Brand identity

**Who:** Thay Le Trung Hieu, chemistry tutor in Hanoi (Ba Dinh, Cau Giay).
**Audience:** Students grades 6-12 and their parents.
**Voice:** A young teacher talking to students, not a textbook. Mix of mentor authority and friendly approachability.
**Language:** Vietnamese. Natural, spoken Vietnamese, not formal written Vietnamese.

## Content types

Seven post types rotate through the week. Each type has a tone and a template.

### 1. Cau hoi on tap (Review question)

Frequency: 3 days/week (Mon, Wed, Fri).
Tone: Mentor. Clear, direct, no fluff. The question is the star.

Template:
```
[Hook: 1 sentence connecting to what students are learning]

[Question: specific, curriculum-aligned, testable]

[If multiple choice: 4 options A/B/C/D]

[Closing: when the answer will be posted, or invite comments]
```

Example (THPT, lop 11):
```
Chuong Nitrogen dang hoc tuan nay, thu xem em nao nam vung chua.

Cho 6,72 lit khi NH3 (dktc) di qua ong dung CuO du, nung nong. Tinh khoi luong Cu thu duoc.

A. 14,4g
B. 19,2g
C. 9,6g
D. 28,8g

Dap an sang mai nhe. Ai lam duoc comment dap an + cach giai xem.
```

### 2. Sai lam hay gap (Common mistakes)

Frequency: 1 day/week (Tue).
Tone: Empathetic but corrective. "Thay gap nhieu em sai cai nay lam."

Template:
```
[Opening: acknowledge the mistake is common, no judgment]

[The mistake: what students do wrong, specifically]

[Why it's wrong: brief explanation]

[The correct approach: show the fix]

[Optional: a quick practice problem to reinforce]
```

### 3. Hoa hoc quanh ta (Chemistry around us)

Frequency: 1 day/week (Thu).
Tone: Curious, storytelling. Like explaining something cool at a dinner table.

Template:
```
[Hook: a daily-life observation or question]

[Chemistry explanation: connect to curriculum topic]

[Fun detail or surprising fact]

[Optional: tie back to what grade/chapter covers this]
```

Example (THCS, lop 8):
```
Tai sao cat chanh vao coca thi sui bot du doi hon binh thuong?

Acid citric trong chanh phan ung voi CO2 hoa tan trong nuoc ngot, day CO2 thoat ra nhanh hon. Tuong tu nhu khi minh hoc ve tinh chat cua acid voi muoi carbonate o chuong 5.

Thu cat mot lat chanh vao ly nuoc ngot roi quay video gui thay xem.
```

### 4. Meo ghi nho (Memory tricks)

Frequency: 1 day/week (Sat).
Tone: Playful, creative. Mnemonics should be memorable and slightly funny.

Template:
```
[The problem: what's hard to remember]

[The mnemonic or trick]

[How to apply it in a problem]
```

### 5. Do vui / Poll (Quiz poll)

Frequency: 1 day/week (Sun).
Tone: Game-show energy. Light, fun, competitive.

Template:
```
[Question framed as a challenge]

React de tra loi:
👍 A. [option]
❤️ B. [option]
😆 C. [option]
😮 D. [option]

[Dap an cong bo luc 20h toi nay]
```

Use Facebook reactions as voting mechanism. This drives engagement through the algorithm.

### 6. Fact thu vi (Fun facts)

Frequency: mixed into weekends or holidays.
Tone: "Co biet khong?" wonder and curiosity.

Template:
```
[Surprising chemistry fact]

[Brief explanation of why]

[Connection to curriculum if natural, skip if forced]
```

### 7. Countdown thi (Exam countdown)

Frequency: seasonal, before major exams (thi giua ky, cuoi ky, THPT Quoc gia).
Tone: Motivational but practical. Tips, not cheerleading.

Template:
```
[Days remaining]

[One specific, actionable study tip for today]

[One quick review point from a high-frequency topic]
```

## Weekly schedule

| Day | THCS post | THPT post |
|-----|-----------|-----------|
| Mon | Cau hoi on tap | Cau hoi on tap |
| Tue | Sai lam hay gap | Sai lam hay gap |
| Wed | Cau hoi on tap | Cau hoi on tap |
| Thu | Hoa hoc quanh ta | Hoa hoc quanh ta |
| Fri | Cau hoi on tap | Cau hoi on tap |
| Sat | Meo ghi nho | Meo ghi nho |
| Sun | Do vui / Poll | Do vui / Poll |

Grade rotation within each group:

- THCS: Lop 6 → 7 → 8 → 9 → 6 → ... (cycle)
- THPT: Lop 10 → 11 → 12 → 10 → ... (cycle)

Topics follow the curriculum map (see `curriculum-map.md`). Align with the Vietnamese school calendar: Semester 1 starts September, Semester 2 starts January.

## Tone rules

Serious posts (review questions, common mistakes):
- No emoji in the question itself
- Short sentences. One idea per sentence.
- Use "em" (for student) and "thay" (for teacher) naturally
- Numbers and formulas must be exact. Double-check stoichiometry.

Light posts (fun facts, polls, chemistry around us, mnemonics):
- 2-3 emoji maximum per post, placed naturally
- Conversational, like texting a student
- Questions that invite comments or shares
- OK to use slang lightly ("quang cao 0 dong cho thay nhe" = joke about sharing)

All posts:
- Under 300 words. Facebook truncates long posts.
- First sentence is the hook. If it's boring, no one reads further.
- End with something that invites action: comment, react, share, tag a friend.

## Hashtag strategy

Every post includes hashtags at the end, separated by a line break.

Required hashtags (always include):
```
#LTHChemistry #HoaHoc
```

Grade-specific (pick one):
```
#KHTN #Lop6 #Lop7 #Lop8 #Lop9
#HoaHoc10 #HoaHoc11 #HoaHoc12
```

Topic-specific (pick 1-2, relevant to the post):
```
#OntapHoaHoc #LuyenThiTHPT #HoaHocVuiVe
#MeoHocHoa #CongThucHoaHoc #DoVuiHoaHoc
```

Maximum 7 hashtags per post. More than that looks spammy.

## Image guidelines

Each post needs an accompanying image. Provide an image prompt with these constraints:

Style: Clean, educational, modern. White or light background. Chemistry-themed (molecules, lab equipment, periodic table elements). Brand color: blue (#1E3A5F) and gold (#D4A843).

For review questions: the image shows the question or formula visually. Periodic table highlights, molecular structures, reaction diagrams.

For fun content: more colorful, eye-catching. Real-world photos with chemistry overlay text.

Image prompt format:
```
[IMAGE_PROMPT]: <description of the image to generate, including style, colors, elements, text overlay if any>
```

## Output format

For each post, output exactly this structure:

```
---
post_type: <cau_hoi_on_tap | sai_lam_hay_gap | hoa_hoc_quanh_ta | meo_ghi_nho | do_vui_poll | fact_thu_vi | countdown_thi>
grade_group: <thcs | thpt>
grade: <6 | 7 | 8 | 9 | 10 | 11 | 12>
topic: <curriculum topic in Vietnamese>
chapter: <chapter number and name from SGK>
---

CAPTION:
<the Facebook post text, already humanized>

IMAGE_PROMPT:
<image generation description>

HASHTAGS:
<hashtag string>

ANSWER (if applicable):
<correct answer with brief explanation, to be posted separately later>
```

## Workflow

```
Input: date, grade rotation index
    |
    v
Determine post_type from weekly schedule (Mon=review, Tue=mistakes, etc.)
    |
    v
Determine grade from rotation cycle
    |
    v
Select topic from curriculum-map.md based on school calendar week
    |
    v
Generate draft content using the template for this post_type
    |
    v
Run draft through humanizer (MANDATORY)
    |
    v
Verify: under 300 words? Hook in first sentence? CTA at end? Formulas correct?
    |
    v
Generate image prompt matching the content
    |
    v
Output in the structured format above
```

## Content quality checks

Before finalizing any post, verify:

1. **Chemistry accuracy**: All formulas balanced? Stoichiometry correct? Names match IUPAC/Vietnamese conventions?
2. **Curriculum alignment**: Does this topic exist in SGK Ket noi tri thuc for this grade?
3. **Humanizer pass**: Output reads like a real teacher wrote it, not an AI. Scan for: em dashes, bolded lists, "Let's dive in", triple patterns, promotional language.
4. **Length**: Under 300 words for caption.
5. **Engagement hook**: First sentence grabs attention? Last sentence invites action?
6. **Tone match**: Serious post sounds serious? Fun post sounds fun? No mixing.

## Common mistakes to avoid

| Mistake | Fix |
|---------|-----|
| Using formal written Vietnamese ("Toi xin trinh bay...") | Use spoken Vietnamese ("Hom nay thay co cau nay hay...") |
| Emoji overload on serious posts | Zero emoji on review questions. 2-3 max on fun posts. |
| Generic questions not tied to SGK | Every question maps to a specific chapter in curriculum-map.md |
| Posting answer in same post as question | Always post answer separately, at least 4-6 hours later |
| Hashtag spam (10+ tags) | Max 7, always relevant |
| Starting with "Xin chao cac em" every post | Vary openings. Jump into the content. |
| Making the post about LTH Chemistry (self-promotional) | Make the post about the student and the chemistry. Brand is in the hashtags. |

## SEO for Facebook

Apply these search-friendly patterns:

- Use searchable Vietnamese terms in the first 2 lines (people search Facebook too)
- Include the grade number and subject name naturally: "Hoa 11", "KHTN lop 8"
- Alt text for images: describe the chemistry concept shown, include grade level
- Post timing: 6-7 AM (students commute), 8-9 PM (evening study). Test and adjust.
- Encourage shares by making content genuinely useful, not by asking "share giup thay nhe"
