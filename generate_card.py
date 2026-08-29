from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 1. Process logo to make its background completely transparent
logo = Image.open('logo512.png').convert('RGBA')
arr = np.array(logo, dtype=np.float32)
r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
brightness = np.maximum(g, np.maximum(r, b))
arr[..., 3] = np.clip(brightness * 1.5, 0, 255)
logo_clean = Image.fromarray(arr.astype(np.uint8), mode='RGBA')

# 2. Canvas size - completely transparent background
W, H = 1600, 680
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Fonts
try:
    font_bold = ImageFont.truetype('/usr/share/fonts/Adwaita/AdwaitaMono-Bold.ttf', 30)
    font_regular = ImageFont.truetype('/usr/share/fonts/Adwaita/AdwaitaMono-Regular.ttf', 30)
    font_blocks = ImageFont.truetype('/usr/share/fonts/noto/NotoSansMono-Bold.ttf', 34)
except Exception:
    font_bold = font_regular = font_blocks = ImageFont.load_default()

# Paste seamless transparent logo on the left
logo_size = 500
logo_resized = logo_clean.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
img.paste(logo_resized, (30, 80), logo_resized)

# Right side fastfetch text
x_text = 580
y_start = 80
line_height = 48

# Title: cryptorial0@github
draw.text((x_text, y_start), 'cryptorial0', fill='#27c93f', font=font_bold)
w_user = draw.textlength('cryptorial0', font=font_bold)
draw.text((x_text + w_user, y_start), '@', fill='#8b949e', font=font_bold)
w_at = draw.textlength('@', font=font_bold)
draw.text((x_text + w_user + w_at, y_start), 'github', fill='#27c93f', font=font_bold)

# Separator
y_cur = y_start + 40
draw.text((x_text, y_cur), '------------------------------------------', fill='#8b949e', font=font_regular)

# Modules
modules = [
    ('OS: ', 'Linux x86_64'),
    ('Kernel: ', 'Full-Stack Software Engineer'),
    ('Shell: ', 'fish / zsh / bash'),
    ('Uptime: ', '24/7 coding & building projects'),
    ('CPU: ', 'TypeScript, Rust, Python, Go'),
    ('GPU: ', 'React, Next.js, Docker, Linux'),
    ('RAM: ', 'High Performance / Endless Curiosity'),
    ('Host: ', 'https://github.com/cryptorial0')
]

y_cur += 42
for key, val in modules:
    draw.text((x_text, y_cur), key, fill='#27c93f', font=font_bold)
    w_key = draw.textlength(key, font=font_bold)
    val_color = '#58a6ff' if key == 'Host: ' else '#c9d1d9'
    draw.text((x_text + w_key, y_cur), val, fill=val_color, font=font_regular)
    y_cur += line_height

# Palette color blocks
y_cur += 15
palette = ['#484f58', '#ff7b72', '#7ee787', '#d29922', '#58a6ff', '#bc8cff', '#39c5cf', '#ffffff']
x_block = x_text
for color in palette:
    draw.text((x_block, y_cur), '███ ', fill=color, font=font_blocks)
    x_block += draw.textlength('███ ', font=font_blocks) + 6

img.save('card.png', 'PNG')
print('Generated 100% transparent background card.png!')
