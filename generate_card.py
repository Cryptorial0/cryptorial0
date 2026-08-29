from PIL import Image, ImageDraw, ImageFont

# Canvas size (2x retina: 1760 x 840)
W, H = 1760, 840

img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Terminal window with rounded corners
draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=24, fill='#0d1117', outline='#30363d', width=3)

# Terminal header buttons
draw.ellipse([40, 36, 64, 60], fill='#ff5f56')
draw.ellipse([80, 36, 104, 60], fill='#ffbd2e')
draw.ellipse([120, 36, 144, 60], fill='#27c93f')

# Header Title font
try:
    font_header = ImageFont.truetype('/usr/share/fonts/Adwaita/AdwaitaMono-Regular.ttf', 24)
    font_bold = ImageFont.truetype('/usr/share/fonts/Adwaita/AdwaitaMono-Bold.ttf', 28)
    font_regular = ImageFont.truetype('/usr/share/fonts/Adwaita/AdwaitaMono-Regular.ttf', 28)
    font_blocks = ImageFont.truetype('/usr/share/fonts/noto/NotoSansMono-Bold.ttf', 32)
except Exception:
    font_header = font_bold = font_regular = font_blocks = ImageFont.load_default()

# Window Title
draw.text((W // 2, 48), 'fastfetch', fill='#8b949e', font=font_header, anchor='mm')

# Paste logo512.png on the left
logo = Image.open('logo512.png').convert('RGBA')
logo_size = 540
logo_resized = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
img.paste(logo_resized, (70, 150), logo_resized)

# Right side fastfetch text
x_text = 680
y_start = 160
line_height = 46

# Title: cryptorial0@github
draw.text((x_text, y_start), 'cryptorial0', fill='#27c93f', font=font_bold)
w_user = draw.textlength('cryptorial0', font=font_bold)
draw.text((x_text + w_user, y_start), '@', fill='#484f58', font=font_bold)
w_at = draw.textlength('@', font=font_bold)
draw.text((x_text + w_user + w_at, y_start), 'github', fill='#27c93f', font=font_bold)

# Separator
y_cur = y_start + 36
draw.text((x_text, y_cur), '------------------------------------------', fill='#484f58', font=font_regular)

# Modules (You can customize these anytime!)
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

y_cur += 40
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
print('Generated card.png!')
