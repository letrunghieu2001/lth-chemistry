"""End-to-end test: generate a real chemistry post image."""
import os
from google import genai
from PIL import Image
from io import BytesIO

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Realistic chemistry prompt (what the automation would generate)
prompt = """Modern educational chemistry infographic poster for Vietnamese high school students:
- Title: 'Chemical Bonding Types' displayed prominently at top
- Three sections showing: Ionic Bond (Na+ and Cl- with electron transfer arrow), Covalent Bond (H2O molecule with shared electrons), Metallic Bond (sea of electrons model)
- Each section has a clear labeled diagram with chemical formulas
- Color scheme: dark blue gradient background, neon cyan and magenta accents
- Style: clean modern infographic, bold sans-serif typography, flat design icons
- Layout: 1080x1080 square, organized grid layout
- Include small 'LTH Chemistry' watermark at bottom right
- No Vietnamese text, use English labels and chemical symbols only"""

print("Generating chemistry infographic with Nano Banana 2...")
resp = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents=[prompt],
)

for part in resp.parts:
    if part.inline_data is not None:
        img = Image.open(BytesIO(part.inline_data.data))
        # Resize to 1080x1080 for Facebook
        img = img.resize((1080, 1080), Image.LANCZOS)
        img.save("test_chemistry_post.png", "PNG", quality=95)
        print(f"SUCCESS! Final image: {img.size}")
    elif part.text:
        print(f"Text: {part.text[:300]}")
