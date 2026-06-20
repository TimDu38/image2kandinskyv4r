# image2kandinskyv4r

A Python PC-side converter that turns an image into compact drawing data for NumWorks/Kandinsky-style rendering.

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
2. (Optional) Click **Load Palette** to restrict output colors to a palette image.
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

## Conversion modes (summary)

- **Raw**: plain tuple/list representation.
- **Raw+**: delta-style rectangle stream for improved compactness.
- **Hex**: hexadecimal string encoding (strict size/value limits).
- **String**: compact character encoding (larger supported ranges than mini).
- **String mini**: very compact variant with tighter limits.

Use the decoder that corresponds to the selected mode.

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
