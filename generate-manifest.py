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

def extract_bilingual_metadata(file_path):
    """
    Extract bilingual metadata from article file.
    Returns dict with en/ar titles and excerpts.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    filename = os.path.basename(file_path)
    
    # Check if this is a bilingual file (has both content-en and content-ar)
    has_content_en = soup.find(id='contentEn') is not None
    has_content_ar = soup.find(id='contentAr') is not None
    
    # For bilingual single-file articles
    if has_content_en and has_content_ar:
        # Extract English title
        title_en_elem = soup.find(id='postTitleEn')
        title_en = title_en_elem.text.strip() if title_en_elem else filename.replace('.html', '').replace('_', ' ').title()
        
        # Extract Arabic title
        title_ar_elem = soup.find(id='postTitleAr')
        title_ar = title_ar_elem.text.strip() if title_ar_elem else title_en
        
        # Extract English excerpt (first paragraph from content-en)
        content_en = soup.find(id='contentEn')
        excerpt_en = ''
        if content_en:
            first_p = content_en.find('p')
            if first_p:
                excerpt_en = first_p.text.strip()
        
        # Extract Arabic excerpt (first paragraph from content-ar)
        content_ar = soup.find(id='contentAr')
        excerpt_ar = ''
        if content_ar:
            first_p = content_ar.find('p')
            if first_p:
                excerpt_ar = first_p.text.strip()
        
        # Clean up excerpts
        excerpt_en = ' '.join(excerpt_en.split())[:160]
        if len(excerpt_en) >= 157:
            excerpt_en = excerpt_en[:157] + '...'
        
        excerpt_ar = ' '.join(excerpt_ar.split())[:160]
        if len(excerpt_ar) >= 157:
            excerpt_ar = excerpt_ar[:157] + '...'
        
        # Get category from English badge
        type_elem = soup.find('span', class_='post-type-badge')
        if not type_elem:
            type_elem = soup.find(id='postTypeEn')
        category_raw = type_elem.text.strip().upper() if type_elem else 'GUIDE'
        
        category_map = {'REVIEW': 'REVIEW', 'GUIDE': 'GUIDE', 'NEWS': 'NEWS', 'WALKTHROUGH': 'WALKTHROUGH', 'ARTICLE': 'GUIDE'}
        category = category_map.get(category_raw, 'GUIDE')
        
        # Get date
        date_elem = soup.find('span', class_='post-date')
        if not date_elem:
            date_elem = soup.find(id='postDateEn')
        if date_elem:
            try:
                date_obj = datetime.strptime(date_elem.text.strip(), '%B %d, %Y')
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except:
                formatted_date = datetime.now().strftime('%Y-%m-%d')
        else:
            formatted_date = datetime.now().strftime('%Y-%m-%d')
        
        return {
            'title_en': title_en,
            'title_ar': title_ar,
            'excerpt_en': excerpt_en or 'Click to read this article on PixelZone.',
            'excerpt_ar': excerpt_ar or 'انقر لقراءة هذا المقال على بيكسل زون.',
            'category': category,
            'date': formatted_date,
            'file': filename,
            'is_bilingual': True
        }
    
    # For single-language files (fallback to old method)
    else:
        # Title
        title_elem = soup.find(id='postTitle')
        if not title_elem:
            title_elem = soup.find(id='postTitleEn')
        title = title_elem.text.strip() if title_elem else filename.replace('.html', '').replace('_', ' ').title()
        
        # Category
        type_elem = soup.find(id='postType')
        if not type_elem:
            type_elem = soup.find('span', class_='post-type-badge')
        category_raw = type_elem.text.strip().upper() if type_elem else 'GUIDE'
        category_map = {'REVIEW': 'REVIEW', 'GUIDE': 'GUIDE', 'NEWS': 'NEWS', 'WALKTHROUGH': 'WALKTHROUGH', 'ARTICLE': 'GUIDE'}
        category = category_map.get(category_raw, 'GUIDE')
        
        # Date
        date_elem = soup.find(id='postDate')
        if not date_elem:
            date_elem = soup.find('span', class_='post-date')
        if date_elem:
            try:
                date_obj = datetime.strptime(date_elem.text.strip(), '%B %d, %Y')
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except:
                formatted_date = datetime.now().strftime('%Y-%m-%d')
        else:
            formatted_date = datetime.now().strftime('%Y-%m-%d')
        
        # Excerpt
        body = soup.find(class_='post-body')
        if body:
            first_p = body.find('p')
            excerpt = first_p.text.strip() if first_p else ''
        else:
            excerpt = ''
        
        excerpt = ' '.join(excerpt.split())[:160]
        if len(excerpt) >= 157:
            excerpt = excerpt[:157] + '...'
        if not excerpt:
            excerpt = 'Click to read this article on PixelZone.'
        
        # Detect language from filename
        lang = 'ar' if '-ar.' in filename or filename.endswith('-ar.html') else 'en'
        
        return {
            'title_en': title if lang == 'en' else '',
            'title_ar': title if lang == 'ar' else '',
            'excerpt_en': excerpt if lang == 'en' else '',
            'excerpt_ar': excerpt if lang == 'ar' else '',
            'category': category,
            'date': formatted_date,
            'file': filename,
            'is_bilingual': False,
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

def merge_bilingual_articles(articles_list):
    """Merge bilingual articles that are in separate files"""
    merged = {}
    
    for article in articles_list:
        if article.get('is_bilingual'):
            # Single file with both languages
            base_name = article['file'].replace('.html', '')
            merged[base_name] = article
        else:
            # Separate files: detect base name by removing -en or -ar
            filename = article['file']
            base_name = filename.replace('-en.html', '').replace('-ar.html', '')
            
            if base_name not in merged:
                merged[base_name] = {
                    'title_en': '',
                    'title_ar': '',
                    'excerpt_en': '',
                    'excerpt_ar': '',
                    'category': article['category'],
                    'date': article['date'],
                    'file_en': '',
                    'file_ar': '',
                    'is_bilingual': True
                }
            
            lang = article.get('lang', 'en')
            if lang == 'en':
                merged[base_name]['title_en'] = article['title_en']
                merged[base_name]['excerpt_en'] = article['excerpt_en']
                merged[base_name]['file_en'] = article['file']
            else:
                merged[base_name]['title_ar'] = article['title_ar']
                merged[base_name]['excerpt_ar'] = article['excerpt_ar']
                merged[base_name]['file_ar'] = article['file']
    
    # Convert to list and clean up
    result = []
    for base_name, data in merged.items():
        # Use English as primary if Arabic missing
        if not data.get('title_en'):
            data['title_en'] = data.get('title_ar', 'Untitled')
        if not data.get('excerpt_en'):
            data['excerpt_en'] = data.get('excerpt_ar', '')
        
        # Determine which file to use as default
        data['file'] = data.get('file_en', data.get('file_ar', base_name + '.html'))
        
        result.append(data)
    
    return result

def build_manifest():
    print("🔍 Scanning for articles...")
    
    # Find all article HTML files
    pattern = os.path.join(ARTICLES_DIR, '*.html')
    html_files = glob(pattern)
    html_files.extend(glob(os.path.join(ARTICLES_DIR, '**', '*.html'), recursive=True))
    html_files = list(set([f for f in html_files if not f.endswith('index.html')]))
    
    articles_raw = []
    for file_path in html_files:
        try:
            meta = extract_bilingual_metadata(file_path)
            articles_raw.append(meta)
            if meta.get('is_bilingual'):
                print(f"   ✅ Bilingual article: {meta.get('title_en', 'Unknown')[:40]}...")
            else:
                lang = meta.get('lang', 'en')
                print(f"   ✅ Article ({lang.upper()}): {meta.get('title_en') or meta.get('title_ar', 'Unknown')[:40]}...")
        except Exception as e:
            print(f"   ⚠️ Error in {os.path.basename(file_path)}: {e}")
    
    # Merge bilingual articles (separate files)
    articles = merge_bilingual_articles(articles_raw)
    
    # Sort by date (newest first)
    articles.sort(key=lambda x: x.get('date', '2000-01-01'), reverse=True)
    print(f"   📄 Total articles: {len(articles)}")
    
    # Walkthroughs from CSV
    walkthroughs = load_walkthroughs_from_csv(WALKTHROUGHS_CSV)
    print(f"   🎬 Walkthroughs loaded from CSV: {len(walkthroughs)}")
    
    # Save manifest
    manifest = {
        'articles': articles,
        'walkthroughs': walkthroughs,
        'youtubeChannelUrl': YOUTUBE_CHANNEL
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 Manifest generated!")
    print(f"   → {len(articles)} articles (bilingual: {sum(1 for a in articles if a.get('is_bilingual'))})")
    print(f"   → {len(walkthroughs)} walkthroughs")
    print(f"   → Saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    build_manifest()