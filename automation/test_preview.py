"""
Test preview for Study Card v7 — Two-Stage AI Pipeline.

Stage 1: Gemini Flash composes exact prompt with perfect Vietnamese text
Stage 2: Gemini Pro Image renders the infographic
OCR validates quality, retries if garbled.

Generates 4 preview images + HTML preview page.
"""

import sys
import logging
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import OUTPUT_DIR
from image_generator import create_post_image

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ── Sample Data (tiếng Việt CÓ DẤU) ────────────────────────────────

SAMPLE_MIND_MAP = {
    "post_type": "review_question",
    "image_title": "PHÂN LOẠI OXIT",
    "layout_type": "mind_map",
    "grade_label": "KHTN Lớp 8",
    "image_prompt": "chemistry oxide classification, molecular bonds, oxygen atoms, beaker lab equipment",
    "diagram_data": {
        "center": "OXIT",
        "branches": [
            {"title": "Oxit Axit", "detail": "Phi kim + O₂ → Oxit axit (SO₃, CO₂)"},
            {"title": "Oxit Bazơ", "detail": "Kim loại + O₂ → Oxit bazơ (CaO, Na₂O)"},
            {"title": "Oxit Trung Tính", "detail": "Không tác dụng axit/bazơ (CO, NO)"},
            {"title": "Oxit Lưỡng Tính", "detail": "Vừa axit vừa bazơ (Al₂O₃, ZnO)"},
        ],
    },
    "status": "Năm 1774, Lavoisier đốt cháy lưu huỳnh và phốt pho, quan sát chúng kết hợp với không khí — và khám phá ra vai trò của oxy trong phản ứng cháy! 🔥",
    "cta": "Xem sơ đồ phân loại 4 nhóm oxit trong ảnh nhé! 👇",
    "hashtags": "#LTHChemistry #HoaHoc #KHTN #Lop8 #Oxit",
}

SAMPLE_FLOWCHART = {
    "post_type": "quick_formula",
    "image_title": "CHUỖI PHẢN ỨNG SẮT",
    "layout_type": "flowchart",
    "grade_label": "Hóa Học Lớp 10",
    "image_prompt": "iron metal reactions, rust formation, chemistry lab, periodic table iron element",
    "diagram_data": {
        "steps": [
            {"label": "Fe (Sắt)", "detail": "Kim loại hoạt động trung bình"},
            {"label": "FeCl₂", "detail": "Fe + 2HCl → FeCl₂ + H₂↑"},
            {"label": "Fe(OH)₂", "detail": "FeCl₂ + 2NaOH → Fe(OH)₂↓"},
            {"label": "FeCl₃", "detail": "Fe(OH)₂ + HCl dư → FeCl₃"},
            {"label": "Fe₂O₃", "detail": "Sản phẩm cuối: oxit sắt III"},
        ],
    },
    "status": "Sắt là kim loại được sử dụng từ 3.000 năm TCN. Người Ai Cập cổ đại gọi sắt là \"kim loại từ trời\" vì những mẫu sắt đầu tiên đến từ thiên thạch! ☄️",
    "cta": "Flowchart chuỗi phản ứng Fe → Fe₂O₃ ở ảnh dưới, lưu ôn thi nha! 📚",
    "hashtags": "#LTHChemistry #HoaHoc #Lop10 #ChuoiPhanUng",
}

SAMPLE_INFO_GRID = {
    "post_type": "fun_facts",
    "image_title": "SO SÁNH AXIT VÀ BAZƠ",
    "layout_type": "info_grid",
    "grade_label": "KHTN Lớp 8",
    "image_prompt": "acid base chemistry, litmus paper, pH scale, laboratory beakers colorful solutions",
    "diagram_data": {
        "cells": [
            {"title": "Axit", "bullets": ["Có gốc H", "Quỳ tím → đỏ", "pH < 7", "VD: HCl, H₂SO₄"]},
            {"title": "Bazơ", "bullets": ["Có nhóm OH", "Quỳ tím → xanh", "pH > 7", "VD: NaOH, Ca(OH)₂"]},
            {"title": "Tính chất Axit", "bullets": ["Ăn mòn kim loại", "Tác dụng bazơ → muối + nước"]},
            {"title": "Tính chất Bazơ", "bullets": ["Nhờn tay", "Tác dụng axit → muối + nước"]},
        ],
    },
    "status": "Robert Boyle là người đầu tiên dùng quỳ tím phân biệt axit và bazơ vào năm 1664 — ông phát hiện rằng các loại axit làm đổi màu quỳ tím sang đỏ! 🧪",
    "cta": "Thầy tổng hợp bảng so sánh axit-bazơ trong ảnh, check ngay! 👇",
    "hashtags": "#LTHChemistry #HoaHoc #KHTN #Lop8 #AxitBazo",
}

SAMPLE_QUIZ = {
    "post_type": "quiz_mcq",
    "image_title": "TRẮC NGHIỆM HÓA HỌC",
    "layout_type": "info_grid",
    "grade_label": "Hóa Học Lớp 10",
    "image_prompt": "chemistry quiz challenge, NaCl salt crystal, silver nitrate reaction, lab flask",
    "diagram_data": {
        "cells": [
            {"title": "A", "bullets": ["20,0 gam"]},
            {"title": "B", "bullets": ["22,2 gam"]},
            {"title": "C", "bullets": ["25,0 gam"]},
            {"title": "D", "bullets": ["18,5 gam"]},
        ],
    },
    "quiz_data": {
        "question": "Hòa tan hoàn toàn m gam NaCl vào nước, dung dịch thu được phản ứng vừa đủ với 200ml AgNO₃ 1M. Giá trị m là?",
        "options": ["A. 20,0 gam", "B. 22,2 gam", "C. 25,0 gam", "D. 18,5 gam"],
        "answer": "B",
    },
    "status": "Friedrich Wöhler năm 1828 lần đầu tổng hợp urê từ chất vô cơ — phá vỡ niềm tin rằng chỉ sinh vật sống mới tạo được hợp chất hữu cơ! 🔬",
    "cta": "Thử sức với câu trắc nghiệm NaCl trong ảnh, comment đáp án nhé! 💬",
    "hashtags": "#LTHChemistry #HoaHoc #Lop10 #TracNghiem",
}

SAMPLES = [
    ("mind_map", SAMPLE_MIND_MAP),
    ("flowchart", SAMPLE_FLOWCHART),
    ("info_grid", SAMPLE_INFO_GRID),
    ("quiz", SAMPLE_QUIZ),
]


# ── Main ─────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    all_chars = []

    for idx, (name, sample) in enumerate(SAMPLES):
        print(f"\n{'='*60}")
        print(f"  [{idx+1}/4] Generating: {name.upper()}")
        print(f"{'='*60}")

        filename = f"preview_v6_{name}.png"

        path, chars = create_post_image(
            post_type=sample["post_type"],
            image_title=sample["image_title"],
            layout_type=sample["layout_type"],
            diagram_data=sample["diagram_data"],
            grade_label=sample["grade_label"],
            image_prompt=sample["image_prompt"],
            filename=filename,
            recent_characters=all_chars,
            quiz_data=sample.get("quiz_data"),
        )

        if path and chars:
            all_chars.extend(chars)
            results.append({
                "name": name,
                "path": path,
                "chars": chars,
                "sample": sample,
            })
            logger.info("Saved: %s (chars: %s)", path.name, ", ".join(chars))
        else:
            logger.error("FAILED to generate: %s", name)

        # Delay between cards to avoid rate limits
        if idx < len(SAMPLES) - 1:
            time.sleep(5)

    # Generate HTML preview
    _generate_html_preview(results)

    print(f"\n{'='*60}")
    print("  DONE - Study Card v7 - ALL PREVIEWS GENERATED!")
    print(f"{'='*60}")
    for r in results:
        chars_str = ", ".join(r["chars"])
        print(f"  > {r['path'].name}  (chars: {chars_str})")
    print(f"  > facebook_preview.html")
    print(f"{'='*60}\n")


def _generate_html_preview(results: list[dict]):
    """Generate the Facebook preview HTML with real data."""
    posts_js = []
    for r in results:
        s = r["sample"]
        badge_map = {"mind_map": "mind-map", "flowchart": "flowchart", "info_grid": "info-grid", "quiz": "quiz"}
        label_map = {"mind_map": "Mind Map", "flowchart": "Flowchart", "info_grid": "Info Grid", "quiz": "Quiz MCQ"}
        group = "THCS" if "KHTN" in s["grade_label"] else "THPT"

        posts_js.append(f"""\
{{
        group: "{group}",
        type: "{r['name']}",
        typeLabel: "{label_map.get(r['name'], r['name'])}",
        badgeClass: "{badge_map.get(r['name'], 'info-grid')}",
        image: "{r['path'].name}",
        title: "{s['image_title']}",
        grade: "{s['grade_label']}",
        chars: "{', '.join(r['chars'])}",
        status: `{s['status']}`,
        cta: `{s['cta']}`,
        hashtags: "{s['hashtags']}"
    }}""")

    posts_json = ",\n    ".join(posts_js)

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LTH Chemistry - Study Card v7 Preview</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --bg: #18191A; --card: #242526; --input: #3A3B3C;
            --text: #E4E6EB; --muted: #8A8D91; --border: #3E4042;
            --teal: #0BA5A5; --gold: #D4A017; --navy: #213555;
            --blue: #1877F2; --red: #F33E58;
        }}
        body {{
            font-family: 'Be Vietnam Pro', -apple-system, sans-serif;
            background: var(--bg); color: var(--text);
            min-height: 100vh; padding: 20px 16px;
        }}
        .header {{ text-align: center; padding: 28px 20px 20px; }}
        .header h1 {{
            font-size: 2rem; font-weight: 700;
            background: linear-gradient(135deg, var(--teal), var(--gold));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .header .sub {{ color: var(--muted); font-size: 0.9rem; margin-top: 4px; }}
        .header .badge {{
            display: inline-block; margin-top: 10px; padding: 4px 14px;
            border-radius: 20px; font-size: 0.72rem; font-weight: 600;
            background: linear-gradient(135deg, var(--teal), #0d8080); color: #fff;
        }}
        .grid {{
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 24px; max-width: 1200px; margin: 12px auto 0;
        }}
        @media (max-width: 900px) {{ .grid {{ grid-template-columns: 1fr; max-width: 540px; }} }}

        .post {{
            background: var(--card); border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.4); overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .post:hover {{ transform: translateY(-3px); box-shadow: 0 6px 24px rgba(0,0,0,0.5); }}

        .post-head {{ display: flex; align-items: center; gap: 12px; padding: 14px 16px 10px; }}
        .avatar {{
            width: 44px; height: 44px; border-radius: 50%; flex-shrink: 0;
            background: linear-gradient(135deg, var(--teal), var(--navy));
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 1.1rem; color: #fff;
        }}
        .meta .name {{ font-weight: 600; font-size: 0.95rem; }}
        .meta .time {{ font-size: 0.78rem; color: var(--muted); }}
        .tbadge {{
            margin-left: auto; padding: 3px 10px; border-radius: 6px;
            font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
        }}
        .tbadge.mind-map {{ background: rgba(11,165,165,0.15); color: var(--teal); }}
        .tbadge.flowchart {{ background: rgba(212,160,23,0.15); color: var(--gold); }}
        .tbadge.info-grid {{ background: rgba(24,119,242,0.15); color: #5B9BF7; }}
        .tbadge.quiz {{ background: rgba(243,62,88,0.15); color: var(--red); }}

        .status {{ padding: 0 16px 12px; font-size: 0.9rem; line-height: 1.55; white-space: pre-wrap; }}
        .status .cta {{ display: block; margin-top: 6px; color: var(--teal); font-weight: 500; }}
        .tags {{ padding: 0 16px 10px; font-size: 0.8rem; color: var(--blue); line-height: 1.6; }}
        .chars-info {{ padding: 0 16px 8px; font-size: 0.75rem; color: var(--muted); }}
        .chars-info span {{ color: var(--gold); }}

        .img-wrap {{ position: relative; width: 100%; background: #1a1a1a; }}
        .img-wrap img {{ width: 100%; height: auto; display: block; }}
        .img-wrap .label {{
            position: absolute; top: 10px; left: 10px; padding: 3px 10px;
            border-radius: 6px; font-size: 0.7rem; font-weight: 600;
            background: rgba(0,0,0,0.65); color: #fff; backdrop-filter: blur(4px);
        }}

        .reactions {{
            display: flex; align-items: center; justify-content: space-between;
            padding: 8px 16px; border-bottom: 1px solid var(--border);
            font-size: 0.8rem; color: var(--muted);
        }}
        .actions {{ display: flex; padding: 4px 8px; border-bottom: 1px solid var(--border); }}
        .act-btn {{
            flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px;
            padding: 8px; border: none; background: transparent; color: var(--muted);
            font-size: 0.85rem; font-weight: 500; font-family: inherit;
            border-radius: 6px; cursor: pointer; transition: background 0.15s;
        }}
        .act-btn:hover {{ background: var(--input); }}

        .comment-bar {{
            padding: 10px 16px 14px; display: flex; align-items: center; gap: 10px;
        }}
        .comment-bar .mini-av {{
            width: 32px; height: 32px; border-radius: 50%; background: var(--input); flex-shrink: 0;
        }}
        .comment-bar .inp {{
            flex: 1; padding: 8px 14px; background: var(--input); border: none;
            border-radius: 20px; color: var(--muted); font-size: 0.85rem; font-family: inherit;
        }}

        .footer {{ text-align: center; padding: 32px 20px; color: var(--muted); font-size: 0.8rem; max-width: 1200px; margin: 0 auto; }}
        .footer a {{ color: var(--teal); text-decoration: none; }}
    </style>
</head>
<body>
<div class="header">
    <h1>LTH Chemistry - Study Cards v7</h1>
    <p class="sub">Facebook Post Preview - Two-Stage AI Pipeline</p>
    <span class="badge">STUDY CARD v7 — FLASH→PRO IMAGE</span>
</div>
<div class="grid" id="grid"></div>
<div class="footer">
    <p>Generated by LTH Chemistry Automation Pipeline &bull; <a href="https://fb.com/LTHChemistry">fb.com/LTHChemistry</a></p>
</div>
<script>
const POSTS = [
    {posts_json}
];

function rand(a, b) {{ return Math.floor(Math.random() * (b - a + 1)) + a; }}

const grid = document.getElementById('grid');
POSTS.forEach(p => {{
    grid.insertAdjacentHTML('beforeend', `
    <div class="post">
        <div class="post-head">
            <div class="avatar">TH</div>
            <div class="meta">
                <div class="name">LTH Chemistry - Thầy Hiếu</div>
                <div class="time">Vừa xong &bull; ${{p.grade}}</div>
            </div>
            <span class="tbadge ${{p.badgeClass}}">${{p.typeLabel}}</span>
        </div>
        <div class="status">${{p.status}}<span class="cta">${{p.cta}}</span></div>
        <div class="tags">${{p.hashtags}}</div>
        <div class="chars-info">Chibi: <span>${{p.chars}}</span></div>
        <div class="img-wrap">
            <img src="${{p.image}}" alt="${{p.title}}" loading="lazy">
            <span class="label">${{p.group}} - ${{p.typeLabel}}</span>
        </div>
        <div class="reactions">
            <span>${{rand(20,90)}} reactions</span>
            <span>${{rand(3,18)}} comments &bull; ${{rand(2,12)}} shares</span>
        </div>
        <div class="actions">
            <button class="act-btn">Thích</button>
            <button class="act-btn">Bình luận</button>
            <button class="act-btn">Chia sẻ</button>
        </div>
        <div class="comment-bar">
            <div class="mini-av"></div>
            <div class="inp">Viết bình luận...</div>
        </div>
    </div>`);
}});
</script>
</body>
</html>"""

    html_path = OUTPUT_DIR / "facebook_preview.html"
    html_path.write_text(html, encoding="utf-8")
    logger.info("HTML preview saved: %s", html_path)


if __name__ == "__main__":
    main()
