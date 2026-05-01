import os
import json
import csv
from datetime import datetime
from glob import glob
from bs4 import BeautifulSoup # type: ignore

# ========== CONFIGURATION ==========
ARTICLES_DIR = './Articles/articles/'
WALKTHROUGHS_CSV = './walkthroughs.csv'
OUTPUT_FILE = './pixelzone-manifest.json'
YOUTUBE_CHANNEL = "https://www.youtube.com/@Pixel-Zone3"
# ====================================

def extract_article_metadata(file_path):
    """Extract title, date, category, excerpt from bilingual article template."""
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Detect language from filename or html lang attribute
    filename = os.path.basename(file_path)
    lang = 'ar' if '-ar.' in filename or filename.endswith('-ar.html') else 'en'
    
    # Title from either language-specific element or general
    title_elem = soup.find(id='postTitle')
    title = title_elem.text.strip() if title_elem else filename.replace('.html', '').replace('-en', '').replace('-ar', '').replace('_', ' ').title()
    
    # Category
    type_elem = soup.find(id='postType')
    category_raw = type_elem.text.strip().upper() if type_elem else 'GUIDE'
    category_map = {'REVIEW': 'REVIEW', 'GUIDE': 'GUIDE', 'NEWS': 'NEWS', 'WALKTHROUGH': 'WALKTHROUGH'}
    category = category_map.get(category_raw, 'GUIDE')
    
    # Date
    date_elem = soup.find(id='postDate')
    if date_elem:
        try:
            date_obj = datetime.strptime(date_elem.text.strip(), '%B %d, %Y')
            formatted_date = date_obj.strftime('%Y-%m-%d')
        except:
            formatted_date = datetime.now().strftime('%Y-%m-%d')
    else:
        formatted_date = datetime.now().strftime('%Y-%m-%d')
    
    # Excerpt - try to get from English content first
    excerpt = ''
    content_en = soup.select_one('.content-en')
    if content_en:
        first_p = content_en.find('p')
        if first_p:
            excerpt = first_p.text.strip()
    
    if not excerpt:
        body = soup.find(class_='post-body')
        if body:
            first_p = body.find('p')
            excerpt = first_p.text.strip() if first_p else ''
    
    excerpt = ' '.join(excerpt.split())[:160]
    if len(excerpt) >= 157:
        excerpt = excerpt[:157] + '...'
    if not excerpt:
        excerpt = 'Click to read this article on PixelZone.'
    
    # Generate base filename (without language suffix)
    base_name = filename.replace('-en.html', '').replace('-ar.html', '')
    
    return {
        'title': title,
        'date': formatted_date,
        'category': category,
        'excerpt': excerpt,
        'file': filename,
        'base_name': base_name,
        'lang': lang
    }

def load_walkthroughs_from_csv(csv_path):
    """Read walkthroughs from CSV file automatically."""
    walkthroughs = []
    if not os.path.exists(csv_path):
        print(f"⚠️ CSV file not found: {csv_path}")
        print("   Creating a sample walkthroughs.csv for you...")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'game', 'youtubeId', 'duration', 'views'])
            writer.writerow(['Sample Video Title', 'Sample Game', 'dQw4w9WgXcQ', '10:00', '1000'])
        print(f"✅ Created {csv_path} – edit it and run again.")
        return []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
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
    
    # ----- Articles (bilingual support) -----
    pattern = os.path.join(ARTICLES_DIR, '*.html')
    html_files = glob(pattern)
    html_files.extend(glob(os.path.join(ARTICLES_DIR, '**', '*.html'), recursive=True))
    html_files = list(set([f for f in html_files if not f.endswith('index.html')]))
    
    articles = []
    article_map = {}  # Group by base_name
    
    for file_path in html_files:
        try:
            meta = extract_article_metadata(file_path)
            
            # Group bilingual articles together
            base_name = meta['base_name']
            if base_name not in article_map:
                article_map[base_name] = {}
            
            article_map[base_name][meta['lang']] = meta
            print(f"   ✅ Article ({meta['lang'].upper()}): {meta['title']} ({meta['date']})")
        except Exception as e:
            print(f"   ⚠️ Error in {os.path.basename(file_path)}: {e}")
    
    # Convert grouped articles to combined entries
    for base_name, versions in article_map.items():
        # Use English version as primary if available
        primary = versions.get('en', next(iter(versions.values())))
        
        # If we have both languages, store both filenames
        if 'en' in versions and 'ar' in versions:
            primary['file_en'] = versions['en']['file']
            primary['file_ar'] = versions['ar']['file']
            primary['has_bilingual'] = True
        else:
            primary['has_bilingual'] = False
            primary['file_en'] = primary['file']
            primary['file_ar'] = primary['file']
        
        articles.append(primary)
    
    # Sort by date (newest first)
    articles.sort(key=lambda x: x['date'], reverse=True)
    print(f"   📄 Total articles: {len(articles)}")
    
    # ----- Walkthroughs from CSV -----
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
    print(f"   → {len(articles)} articles (bilingual: {sum(1 for a in articles if a.get('has_bilingual'))})")
    print(f"   → {len(walkthroughs)} walkthroughs")
    print(f"   → Saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    build_manifest()