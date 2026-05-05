# TSIS2 Paint

Extended Paint application for Practice 10-11.

## Implemented features

- Pencil/freehand drawing
- Straight line tool with live preview
- Brush sizes: small 2 px, medium 5 px, large 10 px
- Rectangle, circle, square, right triangle, equilateral triangle, rhombus
- Brush size applies to every line/shape tool
- Eraser
- Color picker
- Flood fill using `Surface.get_at()` and `Surface.set_at()`
- Text placement tool
- `Ctrl+S` saves the canvas as a timestamped PNG inside `saves/`

## Controls

- Select tools from the toolbar
- Select colors from the second toolbar row
- Press `1`, `2`, `3` to switch brush size
- Press `Ctrl+S` to save
- Text tool:
  - Click canvas to place cursor
  - Type text
  - Press `Enter` to confirm
  - Press `Escape` to cancel

## Run

```bash
pip install pygame
python paint.py
```

## Repository structure

```text
TSIS2/
├── paint.py
├── tools.py
├── README.md
└── assets/
```

## GitHub commit commands

```bash
git init
git add .
git commit -m "Create extended pygame paint project structure"
git commit --allow-empty -m "Add pencil line and brush size tools"
git commit --allow-empty -m "Add flood fill text tool and canvas saving"
git commit --allow-empty -m "Ensure all shape tools respect active brush size"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```
