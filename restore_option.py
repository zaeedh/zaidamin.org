"""
Option Switcher Utility for zaidamin.org
Usage:
    python restore_option.py "Option 1 storm"
"""

import os
import sys
import shutil
import json

def restore_option(option_name):
    normalized = option_name.lower().replace(" ", "-")
    opt_dir = os.path.join("options", normalized)
    
    # Also check without hyphens
    if not os.path.exists(opt_dir):
        # Look inside options directory for matching name in manifest
        found = False
        if os.path.exists("options"):
            for folder in os.listdir("options"):
                candidate = os.path.join("options", folder)
                manifest_path = os.path.join(candidate, "manifest.json")
                if os.path.isfile(manifest_path):
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data.get("name", "").lower() == option_name.lower() or data.get("id", "").lower() == normalized:
                            opt_dir = candidate
                            found = True
                            break
        if not found:
            print(f"Error: Option '{option_name}' not found in options/ folder.")
            return False

    print(f"Restoring preset: {option_name} from {opt_dir}...")
    
    # 1. Restore JS
    src_js = os.path.join(opt_dir, "rain-lighting.js")
    if os.path.exists(src_js):
        shutil.copyfile(src_js, "assets/js/rain-lighting.js")
        print("  Restored: assets/js/rain-lighting.js")

    # 2. Restore CSS
    src_css = os.path.join(opt_dir, "style.css")
    if os.path.exists(src_css):
        shutil.copyfile(src_css, "assets/css/style.css")
        print("  Restored: assets/css/style.css")

    # 3. Restore Images
    for img_name in ["lighthouse-banner.jpg", "lighthouse-banner.webp"]:
        src_img = os.path.join(opt_dir, img_name)
        if os.path.exists(src_img):
            shutil.copyfile(src_img, os.path.join("assets/images", img_name))
            print(f"  Restored: assets/images/{img_name}")

    # 4. Restore build.py
    src_build = os.path.join(opt_dir, "build.py")
    if os.path.exists(src_build):
        shutil.copyfile(src_build, "build.py")
        print("  Restored: build.py")

    # 5. Run build.py to recompile dist/
    print("Recompiling site with build.py...")
    import subprocess
    subprocess.run([sys.executable, "build.py"], check=True)

    print(f"Option '{option_name}' successfully restored and deployed!")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "Option 1 storm"
    restore_option(target)
