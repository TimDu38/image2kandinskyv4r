> [!IMPORTANT]
> **Choose the right version for your use case**
>
> - **[TimDu38/image2kandinskyv4r](https://github.com/TimDu38/image2kandinskyv4r)** → recommended for most practical use, especially game-dev assets (small images, sharp edges, low color count), with much faster decode on calculator.
> - **[TimDu38/image2kandinskyv4](https://github.com/TimDu38/image2kandinskyv4)** → recommended for compression/showcase workflows, including larger image conversions (pictures conversion, for example), but significantly slower to decode on calculator.
>
> Both are **PC-side converters** for NumWorks/Kandinsky: encode on computer, then copy generated data + matching decoder script to NumWorks.
> 
# image2kandinskyv4r

A Python PC-side converter that can turn images into a custom python format to load them on a Numworks calculator.

> **Purpose:** This tool is mostly made for **game development assets** (or similar graphics):
> - low amount of unique colors,
> - lots of sharp edges / pixel-art-like content,
> - small image sizes.
>
> It is **not** intended to convert typical photos into NumWorks-friendly data efficiently.

## Quick start

1. Install dependency:
   ```bash
   pip install pillow
   ```
2. Run the app:
   ```bash
   python src/main.py
   ```
3. In the GUI:
   - Select an image
   - Choose a conversion mode (recommended: **String mini** when compatible)
   - Click **Convert**
4. Open generated `data.py` and copy all content.
5. On NumWorks website, create a script and paste `data.py` content.
6. Copy the matching decoder from `src/decoders/` into a second NumWorks script.
7. Transfer both scripts to calculator, import them, and call the decoder.

---

The app provides a GUI to:
- load an image,
- convert it into color + rectangle data,
- preview the reconstructed result,
- export encoded data to `data.py`.

You then copy that generated `data.py` content to NumWorks, add the matching decoder script from `src/decoders/`, and call the decoder on calculator.

---

## What this project does

`image2kandinskyv4r` converts an image into:
- `colors` data (RGB565-based pipeline, exported in decoder-friendly formats),
- `rectangles` data (x, y, width, height + color index, or compressed variants depending on mode).

Internally it:
1. Loads image as RGBA.
2. Collects unique visible colors (alpha > 127), with optional custom palette restriction.
3. Converts image pixels into indexed map.
4. Groups pixels into rectangles and merges compatible adjacent regions.
5. Writes encoded output to `data.py`.

---

## Repository structure

- `src/main.py` — Tkinter GUI app entry point.
- `src/encoder.py` — image loading + color extraction + conversion orchestration.
- `src/rect_converter.py` — image-to-rectangles and merge logic.
- `src/ui_previewer.py` — rectangle preview renderer.
- `src/file_writer.py` — export logic (`Raw`, `Raw+`, `Hex`, `String`, `String mini`).
- `src/decoders/` — decoder scripts to use on NumWorks side.
- `data.py` — generated output file (overwritten on each conversion).

---

## Requirements

- Python 3.10+ (recommended)
- Pillow
- Tkinter (usually included with standard Python installations)
- Kandinsky (if you want to emulate the calculator/preview with `src/decoders/decoder_test_script.py` directly on PC)

Install dependency:

```bash
pip install pillow
```

---

## Run the converter

From repository root:

```bash
python src/main.py
```

---

## How to use (PC side)

1. Click **Select Image** and choose your source image.
2. (Optional) Click **Load Palette**.
3. Click **Preview** to visualize conversion.
4. Choose conversion mode from the dropdown next to **Convert**:
   - Raw
   - Raw+
   - Hex
   - String
   - String mini
5. Click **Convert (...mode...)**.
6. The converter writes output to **`data.py`**.

> Important: `data.py` is regenerated/overwritten each time you convert.

---

## Palette loading mode (important)

Palette loading mode is especially useful for games and multi-image projects.

How it works:
1. Prepare an image that contains **all colors of your target palette**.
2. Click **Load Palette** and select that palette image.
3. From now on, every image you load will be encoded using that same loaded palette (until you click **Unload Palette**).
4. Each image must only contain colors that exist in the loaded palette, otherwise conversion will fail.

Why this is useful:
- Multiple encoded images can share the same `colors` definition.
- In your decoder-side workflow, you can reuse one palette/colors value across many images and only swap rectangle payloads.
- This helps keep assets consistent and can reduce duplicated color data in game pipelines.

---

## NumWorks workflow (website + calculator)

After encoding on PC:

1. Open `data.py` in this repo.
2. Copy its full content.
3. Go to NumWorks website (Python scripts manager) and create a new script.
4. Paste the `data.py` content there and save.
5. In this repo, go to `src/decoders/` and pick the decoder matching your chosen conversion mode.
6. Copy that decoder code.
7. Create another script on NumWorks website and paste the decoder code.
8. Transfer both scripts to calculator.
9. In your program:
   - import values from the data script,
   - import decoder/draw function from decoder script,
   - call the decoder function with the data.

---

## Conversion modes (performance / memory tradeoffs)

- **Raw**
  - Fastest to decode by far.
  - Heaviest on RAM and storage.

- **Raw+**
  - Somewhat slower than Raw.
  - Somewhat less heavy on storage.
  - Similar RAM profile to Raw.

- **Hex**
  - Outdated mode.
  - Generally recommended to avoid.

- **String mini** (recommended)
  - Recommended default in most practical cases.
  - Much slower than Raw (still acceptable in many use cases).
  - Far lighter on RAM and storage.
  - Limits: **max 92 unique colors** and **max 91x91 image dimensions**.

- **String**
  - By far the slowest mode.
  - Use when you want String mini-like storage/memory efficiency but need images larger than 91x91 and/or more than 92 colors.

Always use the decoder that matches the selected conversion mode.

---

## Notes and limits

- Transparency is supported (alpha threshold logic used during conversion).
- If using a custom palette, all image colors must exist in that palette.
- Encoder enforces color/count/range limits depending on export mode.
- Extremely detailed images can produce many rectangles; simplify images for better results.

---

## Troubleshooting

- **"Image has too many colors"**
  - Reduce color count before conversion.
- **Palette mismatch error**
  - Use a compatible image for that palette, or unload palette.
- **Output too large / not practical**
  - Resize image and/or reduce details/colors.
- **Wrong decoder behavior on NumWorks**
  - Ensure decoder matches the exact mode used during conversion.

---

## Quick checklist

- [ ] Convert image in GUI
- [ ] Copy generated `data.py`
- [ ] Paste as script on NumWorks website
- [ ] Copy matching decoder from `src/decoders/`
- [ ] Paste as second script
- [ ] Transfer both to calculator
- [ ] Import and call decoder with `data.py` values
