import os
from glob import glob
import re

# Folders to process
folders = [
    '.',                           # Root (index.html)
    './Articles',                  # Articles page
    './Games',                     # Games page
    './Walkthroughs',              # Walkthroughs page
    './Articles/articles',         # Individual articles
]

# Mobile CSS link to add to <head>
MOBILE_CSS_LINK = '<link rel="stylesheet" href="../mobile.css">\n  '
ROOT_MOBILE_CSS = '<link rel="stylesheet" href="mobile.css">\n  '

# Hamburger menu HTML to add to nav
HAMBURGER_HTML = '''
  <!-- Hamburger Menu Button -->
  <button class="hamburger" id="hamburger" aria-label="Menu">
    <span></span>
    <span></span>
    <span></span>
  </button>
  
  <!-- Menu Overlay -->
  <div class="menu-overlay" id="menuOverlay"></div>'''

# JavaScript for hamburger menu (add before closing body)
HAMBURGER_JS = '''
<script>
// Mobile Hamburger Menu
function initMobileMenu() {
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.querySelector('.nav-links');
  const overlay = document.getElementById('menuOverlay');
  
  if (!hamburger || !navLinks) return;
  
  function toggleMenu() {
    navLinks.classList.toggle('open');
    hamburger.classList.toggle('open');
    if (overlay) overlay.classList.toggle('open');
    document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
  }
  
  hamburger.addEventListener('click', toggleMenu);
  if (overlay) {
    overlay.addEventListener('click', toggleMenu);
  }
  
  // Close menu when clicking a link
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      hamburger.classList.remove('open');
      if (overlay) overlay.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initMobileMenu);
} else {
  initMobileMenu();
}
</script>'''

def add_mobile_css_and_menu(file_path, is_root=False):
    """Add mobile CSS link and hamburger menu to HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'mobile.css' in content and 'hamburger' in content:
        print(f"⏭️ Skipping {file_path} (already has mobile support)")
        return False
    
    modified = False
    
    # 1. Add mobile.css link to <head>
    css_link = ROOT_MOBILE_CSS if is_root else MOBILE_CSS_LINK
    if 'mobile.css' not in content:
        # Find </head> or before </title>
        if '</head>' in content:
            content = content.replace('</head>', f'  {css_link}</head>')
            modified = True
        elif '</title>' in content:
            content = content.replace('</title>', f'</title>\n  {css_link}')
            modified = True
    
    # 2. Add hamburger menu inside nav (after logo, before lang-toggle)
    if 'hamburger' not in content and 'class="hamburger"' not in content:
        # Find the nav closing tag or find lang-toggle
        if 'class="lang-toggle"' in content:
            # Insert hamburger before lang-toggle
            content = content.replace(
                '<div class="lang-toggle">',
                f'{HAMBURGER_HTML}\n  <div class="lang-toggle">'
            )
            modified = True
        elif '</nav>' in content:
            # Insert before closing nav
            content = content.replace(
                '</nav>',
                f'{HAMBURGER_HTML}\n</nav>'
            )
            modified = True
    
    # 3. Add hamburger JavaScript before closing body
    if HAMBURGER_JS.strip() not in content and 'initMobileMenu' not in content:
        if '</body>' in content:
            content = content.replace('</body>', f'{HAMBURGER_JS}\n</body>')
            modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def find_html_files():
    """Find all HTML files to process"""
    html_files = []
    
    for folder in folders:
        if not os.path.exists(folder):
            print(f"⚠️ Folder not found: {folder}")
            continue
        
        # Find index.html or any html file
        if folder == '.':
            # Root folder - only index.html
            if os.path.exists('./index.html'):
                html_files.append(('./index.html', True))
        elif folder == './Articles/articles':
            # Individual article files
            for f in glob(os.path.join(folder, '*.html')):
                html_files.append((f, False))
        else:
            # Other folders - look for index.html
            index_path = os.path.join(folder, 'index.html')
            if os.path.exists(index_path):
                html_files.append((index_path, False))
    
    return html_files

def main():
    print("=" * 50)
    print("🔧 PixelZone Mobile Support Installer")
    print("=" * 50)
    
    # First, create mobile.css file
    mobile_css_content = '''/* ============================================
   PIXELZONE - MOBILE RESPONSIVE STYLES
   (Auto-generated - edit this file to customize)
   ============================================ */

@media (max-width: 768px) {
  /* Navigation */
  nav {
    padding: 0 1rem;
  }
  
  .nav-links {
    position: fixed;
    top: 64px;
    left: -100%;
    width: 75%;
    max-width: 280px;
    height: calc(100vh - 64px);
    background: rgba(8, 11, 20, 0.98);
    backdrop-filter: blur(16px);
    flex-direction: column;
    padding: 2rem 1rem;
    gap: 1.5rem;
    transition: left 0.3s ease;
    z-index: 1000;
    border-right: 1px solid var(--border-glow);
  }
  
  .nav-links.open {
    left: 0;
  }
  
  .hamburger {
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    background: none;
    border: none;
    padding: 10px;
    z-index: 1001;
  }
  
  .hamburger span {
    width: 25px;
    height: 2px;
    background: var(--neon-cyan);
    transition: all 0.3s ease;
  }
  
  .hamburger.open span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
  }
  
  .hamburger.open span:nth-child(2) {
    opacity: 0;
  }
  
  .hamburger.open span:nth-child(3) {
    transform: rotate(-45deg) translate(5px, -5px);
  }
  
  .menu-overlay {
    position: fixed;
    top: 64px;
    left: 0;
    width: 100%;
    height: calc(100vh - 64px);
    background: rgba(0, 0, 0, 0.6);
    z-index: 999;
    display: none;
  }
  
  .menu-overlay.open {
    display: block;
  }
  
  /* Grids become single column */
  .articles-grid, .wt-grid, .games-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  /* Hero section */
  .hero {
    padding: 2rem 1rem;
  }
  
  .hero-btns {
    flex-direction: column;
    align-items: center;
  }
  
  .btn-primary, .btn-secondary, .btn-discord {
    width: 100%;
    max-width: 220px;
    justify-content: center;
  }
  
  /* Filters */
  .controls {
    flex-direction: column;
  }
  
  .search-wrap {
    max-width: 100%;
  }
  
  .search-input {
    font-size: 16px;
  }
  
  .filter-group {
    justify-content: center;
  }
  
  .sort-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .results-info {
    margin-left: 0;
    text-align: center;
  }
  
  /* Article post */
  .post-hero {
    padding: 2rem 1rem;
  }
  
  .post-body {
    padding: 0 1rem 3rem;
  }
  
  .review-score-box {
    flex-direction: column;
    text-align: center;
  }
  
  .pro-con-box {
    grid-template-columns: 1fr;
  }
  
  /* Share buttons */
  .share-buttons {
    gap: 0.5rem;
  }
  
  .share-btn {
    font-size: 0.6rem;
    padding: 6px 12px;
  }
}

/* RTL mobile fixes */
@media (max-width: 768px) {
  [dir="rtl"] .nav-links {
    left: auto;
    right: -100%;
    border-right: none;
    border-left: 1px solid var(--border-glow);
  }
  
  [dir="rtl"] .nav-links.open {
    left: auto;
    right: 0;
  }
  
  [dir="rtl"] .results-info {
    margin-right: 0;
  }
}'''
    
    # Create mobile.css in root
    with open('mobile.css', 'w', encoding='utf-8') as f:
        f.write(mobile_css_content)
    print("✅ Created mobile.css")
    
    # Find all HTML files
    html_files = find_html_files()
    print(f"\n📁 Found {len(html_files)} HTML file(s) to process\n")
    
    updated_count = 0
    for file_path, is_root in html_files:
        if add_mobile_css_and_menu(file_path, is_root):
            updated_count += 1
            print(f"✅ Updated: {file_path}")
    
    print(f"\n🎉 Done! Updated {updated_count} file(s).")
    print("\n📱 Test on your phone or use Chrome DevTools (F12 → Toggle Device Toolbar)")

if __name__ == '__main__':
    main()