import os
import re
import shutil
from glob import glob
from datetime import datetime

ARTICLES_DIR = './Articles/articles/'
# List the articles you want to fix (excluding the already fixed BlockBlast and RE2-Monsters)
FILES_TO_FIX = [
    'RE2-Remastered-Review.html',
    'RE3-Monsters.html',
    'RE4-Monsters.html',
    'SM-Villains.html',
    # Add any other article names here
]

# Path to the already corrected article (used as a template for navbar and scripts)
TEMPLATE_FILE = os.path.join(ARTICLES_DIR, 'RE2-Monsters.html')  # the one we just fixed

def extract_template_parts(template_path):
    """Extract navbar, scripts, and footer from the fixed article."""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Navbar
    nav_match = re.search(r'<nav>.*?</nav>', content, re.DOTALL)
    if not nav_match:
        raise Exception("Could not find navbar in template")
    navbar = nav_match.group(0)

    # Scripts (from the first <script> to the last </script>)
    script_matches = re.findall(r'<script>.*?</script>', content, re.DOTALL)
    if not script_matches:
        raise Exception("Could not find scripts in template")
    scripts = '\n'.join(script_matches)

    # Footer
    footer_match = re.search(r'<footer>.*?</footer>', content, re.DOTALL)
    footer = footer_match.group(0) if footer_match else ''

    return navbar, scripts, footer

def fix_article(file_path, navbar, scripts, footer):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Backup
    backup_dir = './Articles/backup_final_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, os.path.basename(file_path))
    shutil.copy2(file_path, backup_path)
    print(f"   Backup saved: {backup_path}")

    # 2. Replace navbar
    content = re.sub(r'<nav>.*?</nav>', '', content, flags=re.DOTALL)
    # Insert new navbar after <body>
    content = re.sub(r'(<body[^>]*>)', r'\1\n' + navbar, content)

    # 3. Ensure Arabic title and content are preserved (they are already there)
    # No need to modify contentEn/contentAr – they remain untouched.

    # 4. Remove all existing scripts and add new ones
    content = re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL)
    # Insert scripts before </body>
    content = re.sub(r'(</body>)', scripts + r'\n\1', content)

    # 5. Ensure footer is present (replace any existing footer)
    content = re.sub(r'<footer>.*?</footer>', footer, content, flags=re.DOTALL)

    # 6. Add view counter and share buttons if missing
    if 'view-counter-section' not in content:
        # Find the end of contentEn div
        en_end = re.search(r'(</div>\s*<div class="post-body" id="contentAr")', content)
        if en_end:
            insert_point = en_end.start()
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

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"❌ Template file not found: {TEMPLATE_FILE}")
        print("Please ensure RE2-Monsters.html is fixed and available.")
        return

    print("📖 Extracting template parts from RE2-Monsters.html ...")
    navbar, scripts, footer = extract_template_parts(TEMPLATE_FILE)
    print("✅ Extraction successful.\n")

    for filename in FILES_TO_FIX:
        file_path = os.path.join(ARTICLES_DIR, filename)
        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {filename} – skipping")
            continue
        print(f"🔧 Fixing: {filename}")
        fix_article(file_path, navbar, scripts, footer)
        print(f"   Done.\n")

    print("🎉 All specified articles have been updated.")
    print("⚠️ Please test each one on your live site before pushing.")

if __name__ == '__main__':
    main()