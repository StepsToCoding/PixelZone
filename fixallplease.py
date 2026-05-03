import os
import re
import shutil
from glob import glob
from datetime import datetime

ARTICLES_FOLDER = './Articles/articles/'
WORKING_ARTICLE = './Articles/articles/BlockBlast-TheMostPopular.html'

def extract_navbar_and_scripts(template_path):
    """Extract the navbar HTML and the entire script block from the working article."""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract navbar (from <nav> to </nav>)
    nav_match = re.search(r'<nav>.*?</nav>', content, re.DOTALL)
    if not nav_match:
        raise Exception("Could not find navbar in working article")
    navbar = nav_match.group(0)

    # Extract all script tags (there are two: one with functions, one with hamburger menu – we take both)
    scripts = re.findall(r'<script>.*?</script>', content, re.DOTALL)
    if not scripts:
        raise Exception("Could not find scripts in working article")
    # Join all scripts
    all_scripts = '\n'.join(scripts)

    # Also extract the CSS needed for bilingual navbar and mobile menu (already in the style, but we ensure it's present)
    # We'll not modify the CSS to avoid breaking; we assume the target articles already have the correct CSS
    # If not, we could also inject the CSS, but let's keep it simple.

    return navbar, all_scripts

def fix_article(file_path, navbar, scripts):
    """Replace navbar and inject scripts, preserving content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Backup
    backup_dir = './Articles/backup_surgical_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, os.path.basename(file_path))
    shutil.copy2(file_path, backup_path)
    print(f"   Backup saved to {backup_path}")

    # 2. Replace navbar
    # Remove existing navbar first
    content = re.sub(r'<nav>.*?</nav>', '', content, flags=re.DOTALL)
    # Insert new navbar right after <body>
    content = re.sub(r'(<body[^>]*>)', r'\1\n' + navbar, content)

    # 3. Remove all existing scripts (to avoid duplicates)
    content = re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL)

    # 4. Insert the combined scripts before </body>
    content = re.sub(r'(</body>)', scripts + r'\n\1', content)

    # 5. Ensure view counter and share buttons are present at the end of English content
    # Look for the view-counter-section and share-section – if missing, add them
    if 'view-counter-section' not in content:
        # Find the end of contentEn div
        en_end = re.search(r'(</div>\s*<div class="post-body" id="contentAr")', content)
        if en_end:
            insert_point = en_end.start()
            # Prepare the HTML to insert
            add_html = '''
  <div class="view-counter-section">
    <div class="view-counter">
      <span class="view-icon">👁️</span>
      <span class="view-count-display">0</span>
      <span class="view-label">views</span>
    </div>
  </div>
  <div class="share-section">
    <div class="glow-divider" style="margin: 2rem 0 1.5rem;"></div>
    <div class="share-title">📤 SHARE THIS ARTICLE</div>
    <div class="share-buttons">
      <button class="share-btn twitter">🐦 Twitter</button>
      <button class="share-btn whatsapp">📱 WhatsApp</button>
      <button class="share-btn telegram">✈️ Telegram</button>
      <button class="share-btn copy">🔗 Copy Link</button>
    </div>
  </div>
'''
            content = content[:insert_point] + add_html + content[insert_point:]

    # 6. Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    if not os.path.exists(WORKING_ARTICLE):
        print(f"❌ Working article not found: {WORKING_ARTICLE}")
        return

    print("📖 Extracting navbar and scripts from BlockBlast article...")
    navbar, scripts = extract_navbar_and_scripts(WORKING_ARTICLE)
    print("✅ Extracted successfully.")

    articles = glob(os.path.join(ARTICLES_FOLDER, '*.html'))
    # Exclude the working article itself
    articles = [a for a in articles if a != WORKING_ARTICLE]

    print(f"\n📁 Found {len(articles)} other articles.\n")
    for idx, article in enumerate(articles, 1):
        print(f"{idx}. Processing: {os.path.basename(article)}")
        fix_article(article, navbar, scripts)
        print(f"   Done.\n")

    print("🎉 All articles have been updated with the working navbar and scripts.")
    print("⚠️ Important: The CSS (styles) in your articles were not modified.")
    print("   If some styles are missing (e.g., mobile menu), manually add the CSS from BlockBlast's <style> section.")
    print("   But your BlockBlast article already contains the correct CSS, so other articles should work if they already have the same CSS.")

if __name__ == '__main__':
    main()