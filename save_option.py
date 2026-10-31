import os
import shutil
import json

def save_option_1():
    opt_dir = os.path.join("options", "option-1-storm")
    os.makedirs(opt_dir, exist_ok=True)

    # 1. Copy core files
    files_to_copy = [
        ("assets/js/rain-lighting.js", "rain-lighting.js"),
        ("assets/css/style.css", "style.css"),
        ("assets/images/lighthouse-banner.jpg", "lighthouse-banner.jpg"),
        ("assets/images/lighthouse-banner.webp", "lighthouse-banner.webp"),
        ("index.html", "index.html"),
        ("build.py", "build.py"),
    ]

    for src, dst_name in files_to_copy:
        dst = os.path.join(opt_dir, dst_name)
        shutil.copyfile(src, dst)
        print(f"Copied {src} -> {dst}")

    # 2. Write Manifest
    manifest = {
        "name": "Option 1 storm",
        "id": "option-1-storm",
        "timestamp": "2026-11-01T07:14:00+08:00",
        "title": "Atmospheric Lighthouse Storm - Clean & Borderless Standard",
        "description": "Balanced realistic maritime storm featuring silky smooth DOF rain, atmospheric volumetric cloud churn, distant village lights, feathered lighthouse beam, and natural borderless background dissolution with unobstructed ocean waves.",
        "specs": {
            "rain_drops": "~540 heterogeneous streaks (3 optical depth layers: 44% far mist, 45% focal in-focus, 11% near bokeh)",
            "rain_motion_blur": "5-stop optical feathered gradient (0% -> 25% -> 50% -> 75% -> 100%)",
            "clouds": "4 procedural multi-lobed volumetric clusters + 8 low scud vapor wisps",
            "lightning": "Procedural branching fractal strikes deep in background with ambient flash wash",
            "lighting_beam": "Multi-pass Gaussian feathered beam (shadowBlur=18, zero hard cut edges)",
            "distant_lights": "Twinkling cottage lamps mapped to cliff cottages and secondary rhythmic lighthouse beacon",
            "framing": "Borderless with soft radial edge mask: radial-gradient(ellipse 98% 90% at 50% 50%, #000 76%, transparent 100%)",
            "wave_rendering": "Pure, unobstructed fine-art painting (zero artificial splash/mist sprites)"
        },
        "archived_files": [
            "rain-lighting.js",
            "style.css",
            "lighthouse-banner.jpg",
            "lighthouse-banner.webp",
            "index.html",
            "build.py"
        ]
    }

    with open(os.path.join(opt_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # 3. Write README
    readme_content = """# Option 1 Storm: Atmospheric Lighthouse & Clean Ocean Preset

**Saved Date**: November 1, 2026  
**Status**: Archived & Production-Ready  
**Preset Name**: `Option 1 storm`

## Overview
This preset captures the harmonious, realistic maritime storm composition developed for **Dr. Zaid Amin** (`zaidamin.org`).

### Key Visual Characteristics:
1. **Unobstructed Fine-Art Waves**: Pure, natural ocean waves as rendered in the 2K master artwork—free from artificial vector splashes or mist sprites.
2. **Smooth Heterogeneous Rain with Depth of Field**: ~540 delicate raindrops distributed across 3 optical depth layers (atmospheric far mist, crisp in-focus driving rain, and soft near-camera bokeh blur) with silky 5-stop feathered motion blur.
3. **Living Atmospheric Clouds**: 4 procedural volumetric cloud clusters that churn and drift in `screen` mode over the dark sky.
4. **Soft Procedural Lightning**: Realistic fractal lightning bolts deep behind the clouds, casting soft ambient storm washes.
5. **Distant Cottage Lights & Horizon Beacon**: Warm golden cottage lamps mapped across the bay cliff and a rhythmic secondary lighthouse on the horizon.
6. **Zero Cut Edges on Lighthouse Beam**: Multi-pass Gaussian-feathered beam with radiant lens flare and eye-bloom.
7. **Seamless Borderless Integration**: Radial dissolution mask (`ellipse 98% 90%`) smoothly fusing the painting into the dark navy page canvas.

## Restoration
To restore this preset at any time:
```bash
python restore_option.py "Option 1 storm"
```
"""
    with open(os.path.join(opt_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("Option 1 storm successfully saved!")

if __name__ == "__main__":
    save_option_1()
