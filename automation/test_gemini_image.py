"""Test Gemini Flash Image model (free tier)."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

key = os.environ.get("GEMINI_API_KEY", "")
print(f"Key: {key[:20]}...")

from google import genai

client = genai.Client(api_key=key)

# Test multiple model names
models_to_try = [
    "gemini-2.5-flash-preview-image",
    "gemini-2.5-flash-image",  
    "gemini-2.0-flash-image",
]

prompt = (
    "A cute chibi chemistry teacher character with round glasses and a teal lab coat, "
    "holding a beaker with colorful bubbling liquid. Warm cream background (#FDF8F0). "
    "Clean educational infographic style, modern flat illustration, 1080x1080px."
)

for model_name in models_to_try:
    print(f"\nTrying model: {model_name}")
    try:
        resp = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        parts = getattr(resp, "parts", None)
        if parts:
            for part in parts:
                inline = getattr(part, "inline_data", None)
                if inline is not None and hasattr(inline, "data"):
                    outpath = f"output/test_{model_name.replace('-','_')}.png"
                    with open(outpath, "wb") as f:
                        f.write(inline.data)
                    print(f"  SUCCESS! Image saved: {outpath} ({len(inline.data)} bytes)")
                    break
            else:
                txt = resp.text[:200] if resp.text else "none"
                print(f"  Parts found but no image data. Text: {txt}")
        else:
            print("  No parts returned")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nDone!")
