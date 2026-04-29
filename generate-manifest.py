import os
import json
import csv
from datetime import datetime
from glob import glob
from bs4 import BeautifulSoup

# ========== CONFIGURATION ==========
ARTICLES_DIR = './Articles/articles/'      # your blog posts
WALKTHROUGHS_CSV = './walkthroughs.csv'    # CSV for walkthroughs
OUTPUT_FILE = './pixelzone-manifest.json'
YOUTUBE_CHANNEL = "https://www.youtube.com/@Pixel-Zone3"
# ====================================

def extract_article_metadata(file_path):
    """Extract title, date, category, excerpt from your blog template."""
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    title_elem = soup.find(id='postTitle')
    title = title_elem.text.strip() if title_elem else os.path.basename(file_path).replace('.html', '').replace('-', ' ').title()
    
    type_elem = soup.find(id='postType')
    category_raw = type_elem.text.strip().upper() if type_elem else 'GUIDE'
    category_map = {'REVIEW': 'REVIEW', 'GUIDE': 'GUIDE', 'NEWS': 'NEWS', 'WALKTHROUGH': 'WALKTHROUGH'}
    category = category_map.get(category_raw, 'GUIDE')
    
    date_elem = soup.find(id='postDate')
    if date_elem:
        try:
            date_obj = datetime.strptime(date_elem.text.strip(), '%B %d, %Y')
            formatted_date = date_obj.strftime('%Y-%m-%d')
        except:
            formatted_date = datetime.now().strftime('%Y-%m-%d')
    else:
        formatted_date = datetime.now().strftime('%Y-%m-%d')
    
    body = soup.find(class_='post-body')
    if body:
        first_p = body.find('p')
        excerpt = first_p.text.strip() if first_p else ''
        excerpt = ' '.join(excerpt.split())[:160]
        if len(excerpt) >= 157:
            excerpt = excerpt[:157] + '...'
    else:
        excerpt = 'Read the full article on PixelZone.'
    if not excerpt:
        excerpt = 'Click to read this article on PixelZone.'
    
    return {
        'title': title,
        'date': formatted_date,
        'category': category,
        'excerpt': excerpt,
        'file': os.path.basename(file_path)
    }

def load_walkthroughs_from_csv(csv_path):
    """Read walkthroughs from CSV file automatically."""
    walkthroughs = []
    if not os.path.exists(csv_path):
        print(f"⚠️ CSV file not found: {csv_path}")
        print("   Creating a sample walkthroughs.csv for you...")
        # Create a sample CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'game', 'youtubeId', 'duration', 'views'])
            writer.writerow(['Sample Video Title', 'Sample Game', 'dQw4w9WgXcQ', '10:00', '1000'])
        print(f"✅ Created {csv_path} – edit it and run again.")
        return []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip rows with missing youtubeId
            if not row.get('youtubeId') or row['youtubeId'] == 'PLACEHOLDER_ID':
                continue
            walkthroughs.append({
                'title': row.get('title', 'Untitled'),
                'game': row.get('game', 'Various'),
                'youtubeId': row['youtubeId'],
                'duration': row.get('duration', '—'),
                'views': row.get('views', '0')
            })
    return walkthroughs

def build_manifest():
    print("🔍 Scanning for articles...")
    
    # ----- Articles -----
    pattern = os.path.join(ARTICLES_DIR, '*.html')
    html_files = glob(pattern)
    html_files.extend(glob(os.path.join(ARTICLES_DIR, '**', '*.html'), recursive=True))
    html_files = list(set([f for f in html_files if not f.endswith('index.html')]))
    
    articles = []
    for file_path in html_files:
        try:
            meta = extract_article_metadata(file_path)
            articles.append(meta)
            print(f"   ✅ Article: {meta['title']} ({meta['date']})")
        except Exception as e:
            print(f"   ⚠️ Error in {os.path.basename(file_path)}: {e}")
    
    articles.sort(key=lambda x: x['date'], reverse=True)
    print(f"   📄 Total articles: {len(articles)}")
    
    # ----- Walkthroughs from CSV (auto) -----
    walkthroughs = load_walkthroughs_from_csv(WALKTHROUGHS_CSV)
    print(f"   🎬 Walkthroughs loaded from CSV: {len(walkthroughs)}")
    
    # ----- Save manifest -----
    manifest = {
        'articles': articles,
        'walkthroughs': walkthroughs,
        'youtubeChannelUrl': YOUTUBE_CHANNEL
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 Manifest generated!")
    print(f"   → {len(articles)} articles")
    print(f"   → {len(walkthroughs)} walkthroughs")
    print(f"   → Saved to {OUTPUT_FILE}")
    print(f"\n📺 YouTube channel: {YOUTUBE_CHANNEL}")

if __name__ == '__main__':
    build_manifest()