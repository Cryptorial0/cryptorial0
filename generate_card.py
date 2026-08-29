import os
import json
import urllib.request
import datetime
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ================= USER CONFIGURATION ================= #
# Fill in any fields you want (or leave as "" if not used):
ROLE        = ""                    # e.g. "Full-Stack Software Engineer"
LANGUAGES   = ""                    # e.g. "TypeScript, Python, Rust, Go"
STACK       = ""                    # e.g. "React, Next.js, Node.js, Tailwind"
TOOLS       = ""                    # e.g. "Linux, Docker, Neovim, Git"
BUILDING    = ""                    # e.g. "Open source developer tools"
LEARNING    = ""                    # e.g. "Distributed Systems & AI Agents"
WEBSITE     = "https://cryptori.al" # Your domain hack website
# ====================================================== #

# 1. Fetch live GitHub statistics
USERNAME = "Cryptorial0"
headers = {'User-Agent': 'fastfetch-generator'}
token = os.environ.get('GITHUB_TOKEN')
if token:
    headers['Authorization'] = f'Bearer {token}'

# Default fallback values
public_repos = "5"
total_commits = "23"
uptime_str = "4 yrs, 1 mos on GitHub"

try:
    user_url = f"https://api.github.com/users/{USERNAME}"
    req = urllib.request.Request(user_url, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as resp:
        user_data = json.loads(resp.read().decode())
        public_repos = str(user_data.get('public_repos', public_repos))
        
        created_at_str = user_data.get('created_at')
        if created_at_str:
            created_at = datetime.datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
            now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            days = (now - created_at).days
            years = days // 365
            months = (days % 365) // 30
            uptime_str = f"{years} yrs, {months} mos on GitHub"

    commits_url = f"https://api.github.com/search/commits?q=author:{USERNAME}"
    req_c = urllib.request.Request(commits_url, headers={**headers, 'Accept': 'application/vnd.github.cloak-preview'})
    with urllib.request.urlopen(req_c, timeout=5) as resp_c:
        commits_data = json.loads(resp_c.read().decode())
        total_commits = f"{commits_data.get('total_count', total_commits):,}"
except Exception as e:
    print(f"Warning fetching live GitHub stats: {e}")

# 2. Process Logo with alpha transparency for green glow
logo = Image.open('logo512.png').convert('RGBA')
arr = np.array(logo, dtype=np.float32)
r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
brightness = np.maximum(g, np.maximum(r, b))
arr[..., 3] = np.clip(brightness * 1.6, 0, 255)
logo_transparent = Image.fromarray(arr.astype(np.uint8), mode='RGBA')

# 3. Canvas setup (2x retina: 1760 x 860)
W, H = 1760, 860
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Terminal window with rounded corners
draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=24, fill='#0d1117', outline='#30363d', width=3)

# Terminal header buttons
draw.ellipse([40, 36, 64, 60], fill='#ff5f56')
draw.ellipse([80, 36, 104, 60], fill='#ffbd2e')
draw.ellipse([120, 36, 144, 60], fill='#27c93f')

# Load fonts reliably from bundled files
script_dir = os.path.dirname(os.path.abspath(__file__))
font_bold_path = os.path.join(script_dir, 'Font-Bold.ttf')
font_reg_path = os.path.join(script_dir, 'Font-Regular.ttf')

if os.path.exists(font_bold_path) and os.path.exists(font_reg_path):
    font_header = ImageFont.truetype(font_reg_path, 24)
    font_bold = ImageFont.truetype(font_bold_path, 28)
    font_regular = ImageFont.truetype(font_reg_path, 28)
    font_blocks = ImageFont.truetype(font_bold_path, 32)
else:
    # Fallback to system fonts
    font_header = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 24)
    font_bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 28)
    font_regular = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 28)
    font_blocks = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 32)

# Window Title
draw.text((W // 2, 48), 'fastfetch', fill='#8b949e', font=font_header, anchor='mm')

# Paste seamless transparent logo on the left
logo_size = 540
logo_resized = logo_transparent.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
img.paste(logo_resized, (70, 160), logo_resized)

# Right side fastfetch modules
x_text = 680
y_start = 145
line_height = 44

# Title: cryptorial0@github
draw.text((x_text, y_start), 'cryptorial0', fill='#27c93f', font=font_bold)
w_user = draw.textlength('cryptorial0', font=font_bold)
draw.text((x_text + w_user, y_start), '@', fill='#484f58', font=font_bold)
w_at = draw.textlength('@', font=font_bold)
draw.text((x_text + w_user + w_at, y_start), 'github', fill='#27c93f', font=font_bold)

# Separator
y_cur = y_start + 34
draw.text((x_text, y_cur), '------------------------------------------', fill='#484f58', font=font_regular)

# Modules List: Auto-updating stats + Customizable fields
modules = [
    ('Role: ', ROLE),
    ('Languages: ', LANGUAGES),
    ('Stack: ', STACK),
    ('Tools: ', TOOLS),
    ('Building: ', BUILDING),
    ('Learning: ', LEARNING),
    ('Commits: ', f"{total_commits} commits"),
    ('Repos: ', f"{public_repos} public repos"),
    ('Uptime: ', uptime_str),
    ('Website: ', WEBSITE if WEBSITE else f"https://github.com/{USERNAME}")
]

y_cur += 36
for key, val in modules:
    draw.text((x_text, y_cur), key, fill='#27c93f', font=font_bold)
    w_key = draw.textlength(key, font=font_bold)
    val_text = val if val else "—"
    val_color = '#58a6ff' if ('https://' in val_text or '@' in val_text or '.al' in val_text) else ('#8b949e' if val_text == "—" else '#c9d1d9')
    draw.text((x_text + w_key, y_cur), val_text, fill=val_color, font=font_regular)
    y_cur += line_height

# Palette color blocks
y_cur += 12
palette = ['#484f58', '#ff7b72', '#7ee787', '#d29922', '#58a6ff', '#bc8cff', '#39c5cf', '#ffffff']
x_block = x_text
for color in palette:
    draw.text((x_block, y_cur), '███ ', fill=color, font=font_blocks)
    x_block += draw.textlength('███ ', font=font_blocks) + 6

img.save('card_v2.png', 'PNG')
print(f"Successfully generated profile.png with bundled fonts! Commits: {total_commits}")
