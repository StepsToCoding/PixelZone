import os
from glob import glob
from datetime import datetime

SITEMAP_PATH = './sitemap.xml'
BASE_URL = 'https://stepstocoding.github.io/PixelZone'

def generate_sitemap():
    urls = []
    
    # Main pages
    main_pages = [
        ('/', 'daily', 1.0),
        ('/index.html', 'daily', 1.0),
        ('/Articles/index.html', 'weekly', 0.9),
        ('/Games/index.html', 'weekly', 0.8),
        ('/Walkthroughs/index.html', 'weekly', 0.8),
    ]
    
    for path, freq, priority in main_pages:
        urls.append({
            'loc': f'{BASE_URL}{path}',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': freq,
            'priority': priority
        })
    
    # Articles
    article_files = glob('./Articles/articles/*.html')
    for file_path in article_files:
        filename = os.path.basename(file_path)
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')
        urls.append({
            'loc': f'{BASE_URL}/Articles/articles/{filename}',
            'lastmod': mod_time,
            'changefreq': 'monthly',
            'priority': 0.7
        })
    
    # Games play page
    if os.path.exists('./Games/play.html'):
        urls.append({
            'loc': f'{BASE_URL}/Games/play.html',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': 0.6
        })
    
    # Generate XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"✅ Sitemap generated with {len(urls)} URLs")
    print(f"📍 Location: {SITEMAP_PATH}")
    print(f"🌐 Base URL: {BASE_URL}")

if __name__ == '__main__':
    generate_sitemap()