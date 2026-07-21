"""Test free image generation APIs."""
import requests
import os
import time

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PROMPT = "cute chibi chemistry teacher anime style holding beaker educational poster navy blue background 1080x1080"

def test_pollinations():
    """Pollinations.ai - No API key needed."""
    print("\n=== Testing Pollinations.ai ===")
    url = f"https://image.pollinations.ai/prompt/{PROMPT}"
    params = {"width": 1080, "height": 1080, "seed": 42, "nologo": "true"}
    
    start = time.time()
    try:
        r = requests.get(url, params=params, timeout=120, allow_redirects=True)
        elapsed = time.time() - start
        ct = r.headers.get("content-type", "unknown")
        print(f"  Status: {r.status_code}, Size: {len(r.content)} bytes, Type: {ct}, Time: {elapsed:.1f}s")
        
        if r.status_code == 200 and len(r.content) > 10000:
            path = os.path.join(OUTPUT_DIR, "test_pollinations.jpg")
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"  SAVED: {path}")
            return True
        else:
            print(f"  FAILED - response too small or error")
            # Print first 500 chars if text
            if "text" in ct or "html" in ct or len(r.content) < 5000:
                print(f"  Body: {r.text[:500]}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_huggingface():
    """Hugging Face Inference API - Free, needs token."""
    print("\n=== Testing Hugging Face (free serverless) ===")
    # No token = anonymous, may work with popular models
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {}  # No token for anonymous
    payload = {"inputs": PROMPT}
    
    start = time.time()
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        elapsed = time.time() - start
        ct = r.headers.get("content-type", "unknown")
        print(f"  Status: {r.status_code}, Size: {len(r.content)} bytes, Type: {ct}, Time: {elapsed:.1f}s")
        
        if r.status_code == 200 and "image" in ct:
            path = os.path.join(OUTPUT_DIR, "test_huggingface.png")
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"  SAVED: {path}")
            return True
        else:
            print(f"  FAILED")
            if len(r.content) < 2000:
                print(f"  Body: {r.text[:500]}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

if __name__ == "__main__":
    results = {}
    results["Pollinations.ai"] = test_pollinations()
    results["HuggingFace"] = test_huggingface()
    
    print("\n" + "="*50)
    print("RESULTS:")
    for name, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"  {name}: {status}")
