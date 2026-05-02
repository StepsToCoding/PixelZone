import os
import re
from glob import glob
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ============================================
# CONFIGURATION
# ============================================
ARTICLES_FOLDER = './Articles/articles/'
BASE_URL = 'https://stepstocoding.github.io/PixelZone'

# ============================================
# PART 1: GENERATE OG IMAGES
# ============================================
def generate_og_images():
    """Create OG images for social sharing"""
    os.makedirs('images', exist_ok=True)
    
    def create_og_image(title, subtitle, filename):
        img = Image.new('RGB', (1200, 630), color='#080b14')
        draw = ImageDraw.Draw(img)
        
        # Border
        draw.rectangle([50, 50, 1150, 580], outline='#00f5ff', width=3)
        
        # Fonts
        try:
            font_large = ImageFont.truetype("arial.ttf", 72)
            font_medium = ImageFont.truetype("arial.ttf", 36)
            font_small = ImageFont.truetype("arial.ttf", 24)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Logo
        draw.text((600, 240), "PIXEL", fill='#00f5ff', anchor='mm', font=font_large)
        draw.text((600, 320), "ZONE", fill='#ff2d78', anchor='mm', font=font_large)
        
        # Text
        draw.text((600, 420), title, fill='#e8eaf6', anchor='mm', font=font_medium)
        draw.text((600, 480), subtitle, fill='#7a8baa', anchor='mm', font=font_small)
        
        img.save(f'images/{filename}', quality=95)
        print(f"   ✅ Created: images/{filename}")
    
    print("\n📸 Generating OG images...")
    create_og_image("Ultimate Gaming Hub", "Guides • Walkthroughs • Free Games", "og-home.jpg")
    create_og_image("Game Guides & Reviews", "Resident Evil • Spider-Man • More", "og-default.jpg")

# ============================================
# PART 2: GENERATE FAVICON
# ============================================
def generate_favicon():
    """Create favicon.ico"""
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Circle background
    draw.ellipse([4, 4, size-4, size-4], fill=(8, 11, 20, 255), outline=(0, 245, 255, 255), width=2)
    
    # Letter "P"
    try:
        font = ImageFont.truetype("arialbd.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    draw.text((32, 30), "P", fill=(0, 245, 255, 255), anchor='mm', font=font)
    
    img.save('favicon.ico', format='ICO', sizes=[(64, 64)])
    img.save('images/favicon.png')
    print("   ✅ Created: favicon.ico and images/favicon.png")

# ============================================
# PART 3: ADD TAGS TO ARTICLES
# ============================================
def extract_article_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<h1 class="post-title" id="postTitleEn">(.*?)</h1>', content)
    if not title_match:
        title_match = re.search(r'<h1 class="post-title">(.*?)</h1>', content)
    if not title_match:
        title_match = re.search(r'<title>(.*?)</title>', content)
    
    title = title_match.group(1).strip() if title_match else os.path.basename(file_path).replace('.html', '').replace('-', ' ').title()
    title_clean = title.replace('"', '\\"')
    
    # Find date
    date_match = re.search(r'<span class="post-date" id="postDateEn">(.*?)</span>', content)
    if not date_match:
        date_match = re.search(r'<span class="post-date">(.*?)</span>', content)
    
    if date_match:
        date_str = date_match.group(1).strip()
        try:
            months = {'January': '01', 'February': '02', 'March': '03', 'April': '04',
                      'May': '05', 'June': '06', 'July': '07', 'August': '08',
                      'September': '09', 'October': '10', 'November': '11', 'December': '12'}
            for month_name, month_num in months.items():
                if month_name in date_str:
                    day = re.search(r'\d+', date_str).group()
                    year = re.search(r'\d{4}', date_str).group()
                    date_iso = f"{year}-{month_num}-{day.zfill(2)}"
                    break
            else:
                date_iso = datetime.now().strftime('%Y-%m-%d')
        except:
            date_iso = datetime.now().strftime('%Y-%m-%d')
    else:
        date_iso = datetime.now().strftime('%Y-%m-%d')
    
    return title, title_clean, date_iso

def add_tags_to_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    title, title_clean, date_iso = extract_article_info(file_path)
    filename = os.path.basename(file_path)
    article_url = f"{BASE_URL}/Articles/articles/{filename}"
    
    # JSON-LD
    if 'application/ld+json' not in content:
        jsonld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title_clean}",
  "description": "Complete game guide for {title_clean}.",
  "author": {{"@type": "Organization", "name": "PixelZone"}},
  "publisher": {{"@type": "Organization", "name": "PixelZone"}},
  "datePublished": "{date_iso}",
  "dateModified": "{date_iso}",
  "mainEntityOfPage": "{article_url}"
}}
</script>'''
        content = content.replace('</head>', f'{jsonld}\n</head>')
        modified = True
        print(f"   ✅ Added JSON-LD")
    
    # OG Tags
    if 'og:image' not in content:
        og_tags = f'''
<meta property="og:title" content="{title} | PixelZone">
<meta property="og:description" content="Read the full guide for {title} on PixelZone.">
<meta property="og:image" content="{BASE_URL}/images/og-default.jpg">
<meta property="og:url" content="{article_url}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} | PixelZone">
<meta name="twitter:image" content="{BASE_URL}/images/og-default.jpg">'''
        content = content.replace('</head>', f'{og_tags}\n</head>')
        modified = True
        print(f"   ✅ Added OG tags")
    
    # Favicon
    if 'favicon' not in content.lower():
        favicon_tag = '<link rel="icon" type="image/x-icon" href="/PixelZone/favicon.ico">'
        content = content.replace('<head>', f'<head>\n{favicon_tag}')
        modified = True
        print(f"   ✅ Added favicon")
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# ============================================
# MAIN
# ============================================
def main():
    print("=" * 50)
    print("🎨 PixelZone Complete SEO Setup")
    print("=" * 50)
    
    # Generate images
    generate_favicon()
    generate_og_images()
    
    # Process articles
    print("\n📄 Processing articles...")
    article_files = glob(os.path.join(ARTICLES_FOLDER, '*.html'))
    
    if not article_files:
        print(f"   ❌ No articles found in {ARTICLES_FOLDER}")
    else:
        updated = 0
        for file_path in article_files:
            print(f"\n   📝 {os.path.basename(file_path)}")
            if add_tags_to_article(file_path):
                updated += 1
        print(f"\n   ✅ Updated {updated} article(s)")
    
    print("\n" + "=" * 50)
    print("🎉 All done! Commit and push to GitHub.")
    print("=" * 50)

if __name__ == '__main__':
    main()