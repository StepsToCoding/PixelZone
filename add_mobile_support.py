import os
from glob import glob

# Complete CSS to add (including mobile styles)
FULL_CSS = '''
  /* MOBILE RESPONSIVE STYLES */
  @media (max-width: 768px) {
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
    
    .articles-grid, .wt-grid, .games-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }
    
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
    
    .controls {
      flex-direction: column;
    }
    
    .search-wrap {
      max-width: 100%;
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
    
    .share-buttons {
      gap: 0.5rem;
    }
    
    .share-btn {
      font-size: 0.6rem;
      padding: 6px 12px;
    }
  }
  
  [dir="rtl"] .nav-links {
    left: auto;
    right: -100%;
    border-right: none;
    border-left: 1px solid var(--border-glow);
  }
  
  [dir="rtl"] .nav-links.open {
    left: auto;
    right: 0;
  }'''

# Hamburger HTML to add inside nav
HAMBURGER_HTML = '''
  <button class="hamburger" aria-label="Menu">
    <span></span>
    <span></span>
    <span></span>
  </button>
  <div class="menu-overlay"></div>'''

# Hamburger JavaScript
HAMBURGER_JS = '''
<script>
// Mobile Hamburger Menu
(function() {
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');
  const overlay = document.querySelector('.menu-overlay');
  
  if (!hamburger || !navLinks) return;
  
  function toggleMenu() {
    navLinks.classList.toggle('open');
    hamburger.classList.toggle('open');
    if (overlay) overlay.classList.toggle('open');
    document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
  }
  
  hamburger.addEventListener('click', toggleMenu);
  if (overlay) overlay.addEventListener('click', toggleMenu);
  
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      hamburger.classList.remove('open');
      if (overlay) overlay.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
})();
</script>'''

def fix_file(file_path, is_root=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 1. Add CSS styles to <style> tag
    if '@media (max-width: 768px)' not in content:
        if '</style>' in content:
            content = content.replace('</style>', f'{FULL_CSS}\n</style>')
            modified = True
            print(f"   ✅ Added CSS styles")
    
    # 2. Add hamburger HTML inside nav (after lang-toggle or before closing nav)
    if '.hamburger' not in content and 'hamburger' not in content:
        if '</nav>' in content:
            content = content.replace('</nav>', f'{HAMBURGER_HTML}\n</nav>')
            modified = True
            print(f"   ✅ Added hamburger HTML")
    
    # 3. Add hamburger JavaScript before </body>
    if 'querySelector(.hamburger)' not in content and 'initMobileMenu' not in content:
        if '</body>' in content:
            content = content.replace('</body>', f'{HAMBURGER_JS}\n</body>')
            modified = True
            print(f"   ✅ Added hamburger JavaScript")
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("=" * 60)
    print("🔧 FORCE FIX - Adding Mobile Menu to ALL Pages")
    print("=" * 60)
    
    # Main pages
    main_pages = [
        'index.html',
        'Games/index.html',
        'Articles/index.html',
        'Walkthroughs/index.html',
    ]
    
    # Find all articles
    articles = glob('./Articles/articles/*.html')
    
    print(f"\n📁 Main pages: {len(main_pages)}")
    print(f"📁 Articles: {len(articles)}")
    print("-" * 60)
    
    fixed = 0
    
    # Fix main pages
    for file_path in main_pages:
        if os.path.exists(file_path):
            print(f"\n📄 {file_path}")
            if fix_file(file_path):
                fixed += 1
                print(f"   ✅ Fixed!")
        else:
            print(f"\n⚠️ {file_path} not found")
    
    # Fix articles
    for file_path in articles:
        print(f"\n📄 {os.path.basename(file_path)}")
        if fix_file(file_path):
            fixed += 1
            print(f"   ✅ Fixed!")
    
    print("\n" + "=" * 60)
    print(f"🎉 Fixed {fixed} file(s).")
    print("=" * 60)
    print("\n📱 Now test on your phone - refresh the page (Ctrl+F5)")
    print("   The hamburger menu should appear on ALL pages!")

if __name__ == '__main__':
    main()