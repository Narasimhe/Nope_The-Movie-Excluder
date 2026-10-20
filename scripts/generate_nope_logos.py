import os
from PIL import Image, ImageDraw, ImageFont

banners_dir = r"F:\Movie_Excluder\movie-excluder\data\banners"
data_dir = r"F:\Movie_Excluder\movie-excluder\data"

svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 140" width="520" height="140">
  <defs>
    <style>
      .nope-text {
        font-family: 'Segoe UI Black', -apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, Arial, sans-serif;
        font-weight: 900;
        font-size: 104px;
        fill: #ef4444;
        letter-spacing: 0.08em;
      }
      .nope-scope {
        stroke: #ef4444;
        fill: none;
        stroke-linecap: round;
      }
      .nope-dot {
        fill: #ef4444;
      }
    </style>
  </defs>
  <!-- N -->
  <text x="32" y="104" class="nope-text">N</text>
  <!-- O (Target Scope) -->
  <g transform="translate(142, 20)">
    <circle cx="50" cy="50" r="36.5" class="nope-scope" stroke-width="11.2"/>
    <line x1="50" y1="2" x2="50" y2="31" class="nope-scope" stroke-width="6.6"/>
    <line x1="50" y1="69" x2="50" y2="98" class="nope-scope" stroke-width="6.6"/>
    <line x1="2" y1="50" x2="31" y2="50" class="nope-scope" stroke-width="6.6"/>
    <line x1="69" y1="50" x2="98" y2="50" class="nope-scope" stroke-width="6.6"/>
    <circle cx="50" cy="50" r="7.5" class="nope-dot"/>
  </g>
  <!-- PE -->
  <text x="268" y="104" class="nope-text">PE</text>
</svg>"""

icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 140" width="140" height="140">
  <g transform="translate(20, 20)">
    <circle cx="50" cy="50" r="36.5" fill="none" stroke="#ef4444" stroke-width="11.2" stroke-linecap="round"/>
    <line x1="50" y1="2" x2="50" y2="31" stroke="#ef4444" stroke-width="6.6" stroke-linecap="round"/>
    <line x1="50" y1="69" x2="50" y2="98" stroke="#ef4444" stroke-width="6.6" stroke-linecap="round"/>
    <line x1="2" y1="50" x2="31" y2="50" stroke="#ef4444" stroke-width="6.6" stroke-linecap="round"/>
    <line x1="69" y1="50" x2="98" y2="50" stroke="#ef4444" stroke-width="6.6" stroke-linecap="round"/>
    <circle cx="50" cy="50" r="7.5" fill="#ef4444"/>
  </g>
</svg>"""

for target_dir in [data_dir, banners_dir]:
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, "nope_logo.svg"), "w", encoding="utf-8") as f:
        f.write(svg_content)
    with open(os.path.join(target_dir, "nope_icon.svg"), "w", encoding="utf-8") as f:
        f.write(icon_svg)

# Generate crisp high-resolution Transparent PNGs using PIL
scale = 4
width = 520 * scale
height = 140 * scale
img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

font_file = "C:/Windows/Fonts/seguibl.ttf"
if not os.path.exists(font_file):
    font_file = "C:/Windows/Fonts/ariblk.ttf"

font = ImageFont.truetype(font_file, int(104 * scale))
red = (239, 68, 68, 255)

# Draw N
draw.text((int(32 * scale), int(4 * scale)), "N", fill=red, font=font)

# Draw Scope
ox = int(142 * scale)
oy = int(20 * scale)
cx = ox + int(50 * scale)
cy = oy + int(50 * scale)
r = int(36.5 * scale)
stroke_w = int(11.2 * scale)
line_w = int(6.6 * scale)

# Outer circle
draw.ellipse(
    [cx - r, cy - r, cx + r, cy + r],
    outline=red,
    width=stroke_w,
)

# Crosshairs
draw.line([(cx, oy + int(2 * scale)), (cx, oy + int(31 * scale))], fill=red, width=line_w)
draw.line([(cx, oy + int(69 * scale)), (cx, oy + int(98 * scale))], fill=red, width=line_w)
draw.line([(ox + int(2 * scale), cy), (ox + int(31 * scale), cy)], fill=red, width=line_w)
draw.line([(ox + int(69 * scale), cy), (ox + int(98 * scale), cy)], fill=red, width=line_w)

# Center dot
dot_r = int(7.5 * scale)
draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=red)

# Draw PE
draw.text((int(268 * scale), int(4 * scale)), "PE", fill=red, font=font)

# Trim transparent bounding box slightly for clean padding
bbox = img.getbbox()
if bbox:
    pad = int(16 * scale)
    cropped = img.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(width, bbox[2] + pad), min(height, bbox[3] + pad)))
else:
    cropped = img

for target_dir in [data_dir, banners_dir]:
    cropped.save(os.path.join(target_dir, "nope_logo.png"), "PNG")

# Also generate icon-only high-res PNG
icon_img = Image.new("RGBA", (140 * scale, 140 * scale), (0, 0, 0, 0))
icon_draw = ImageDraw.Draw(icon_img)
icx = int(70 * scale)
icy = int(70 * scale)

icon_draw.ellipse(
    [icx - r, icy - r, icx + r, icy + r],
    outline=red,
    width=stroke_w,
)
icon_draw.line([(icx, icy - int(48 * scale)), (icx, icy - int(19 * scale))], fill=red, width=line_w)
icon_draw.line([(icx, icy + int(19 * scale)), (icx, icy + int(48 * scale))], fill=red, width=line_w)
icon_draw.line([(icx - int(48 * scale), icy), (icx - int(19 * scale), icy)], fill=red, width=line_w)
icon_draw.line([(icx + int(19 * scale), icy), (icx + int(48 * scale), icy)], fill=red, width=line_w)
icon_draw.ellipse([icx - dot_r, icy - dot_r, icx + dot_r, icy + dot_r], fill=red)

for target_dir in [data_dir, banners_dir]:
    icon_img.save(os.path.join(target_dir, "nope_icon.png"), "PNG")

print("Generated nope_logo.svg, nope_logo.png, nope_icon.svg, and nope_icon.png successfully!")
