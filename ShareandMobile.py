import os
from glob import glob

# Folder containing your articles
articles_folder = './Articles/articles/'

# The complete enhanced code to inject (share buttons + view counter + mobile nav)
enhanced_code = '''
  <!-- VIEW COUNTER SECTION -->
  <div class="view-counter-section">
    <div class="view-counter" id="viewCounter">
      <span class="view-icon">👁️</span>
      <span id="viewCount">Loading...</span>
      <span class="view-label" id="viewLabel">views</span>
    </div>
  </div>

  <!-- SHARE BUTTONS SECTION -->
  <div class="share-section">
    <div class="glow-divider" style="margin: 2rem 0 1.5rem;"></div>
    <div class="share-title" id="shareTitle">📤 SHARE THIS ARTICLE</div>
    <div class="share-buttons">
      <button class="share-btn twitter" onclick="shareOnTwitter()">🐦 Twitter</button>
      <button class="share-btn whatsapp" onclick="shareOnWhatsApp()">📱 WhatsApp</button>
      <button class="share-btn telegram" onclick="shareOnTelegram()">✈️ Telegram</button>
      <button class="share-btn copy" onclick="copyLink()">🔗 Copy Link</button>
    </div>
  </div>
</div>

<style>
/* ============================================
   VIEW COUNTER STYLES
   ============================================ */
.view-counter-section {
  display: flex;
  justify-content: center;
  margin: 1.5rem 0 0;
}
.view-counter {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-card);
  border: 1px solid var(--border-glow);
  padding: 8px 20px;
  border-radius: 40px;
  font-family: 'Orbitron', monospace;
  font-size: 0.85rem;
  color: var(--text-main);
}
.view-icon {
  font-size: 1.1rem;
}
#viewCount {
  font-weight: 700;
  color: var(--neon-cyan);
  font-size: 1rem;
}
.view-label {
  color: var(--text-muted);
  font-size: 0.7rem;
}

/* ============================================
   SHARE BUTTONS STYLES
   ============================================ */
.share-section {
  margin: 2rem 0 1rem;
  text-align: center;
}
.share-title {
  font-family: 'Orbitron', monospace;
  font-size: 0.7rem;
  letter-spacing: 2px;
  color: var(--text-muted);
  margin-bottom: 1rem;
}
.share-buttons {
  display: flex;
  gap: 0.8rem;
  justify-content: center;
  flex-wrap: wrap;
}
.share-btn {
  font-family: 'Orbitron', monospace;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 1px;
  padding: 8px 18px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  clip-path: polygon(6px 0%, 100% 0%, calc(100% - 6px) 100%, 0% 100%);
  color: #080b14;
}
.share-btn:hover {
  transform: translateY(-2px);
  filter: brightness(0.9);
}
.share-btn.twitter { background: #1DA1F2; }
.share-btn.whatsapp { background: #25D366; }
.share-btn.telegram { background: #0088cc; }
.share-btn.copy { background: var(--neon-cyan); color: #080b14; }

/* ============================================
   MOBILE RESPONSIVE STYLES
   ============================================ */
@media (max-width: 768px) {
  /* Hamburger menu */
  .nav-links {
    position: fixed;
    top: 64px;
    left: -100%;
    width: 80%;
    max-width: 300px;
    height: calc(100vh - 64px);
    background: rgba(8, 11, 20, 0.98);
    backdrop-filter: blur(16px);
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 2rem 1rem;
    gap: 1.5rem;
    transition: left 0.3s ease;
    z-index: 1000;
    border-right: 1px solid var(--border-glow);
  }
  .nav-links.open {
    left: 0;
  }
  .nav-links a {
    font-size: 1.1rem;
    padding: 0.8rem;
    width: 100%;
    text-align: center;
  }
  /* Hamburger button */
  .hamburger {
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    background: none;
    border: none;
    padding: 8px;
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
  /* Overlay */
  .menu-overlay {
    position: fixed;
    top: 64px;
    left: 0;
    width: 100%;
    height: calc(100vh - 64px);
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: none;
  }
  .menu-overlay.open {
    display: block;
  }
  /* Adjust hero section for mobile */
  .hero {
    padding: 3rem 1rem 2rem;
  }
  .hero-title {
    font-size: clamp(1.5rem, 5vw, 2.5rem);
  }
  .hero-btns {
    flex-direction: column;
    align-items: center;
  }
  .btn-primary, .btn-secondary, .btn-discord {
    width: 100%;
    max-width: 250px;
    justify-content: center;
  }
  /* Article cards stack properly */
  .articles-grid, .wt-grid, .games-grid {
    grid-template-columns: 1fr;
  }
  /* Larger touch targets */
  .filter-btn, .page-btn, .lang-btn {
    padding: 10px 16px;
    min-height: 44px;
  }
  .search-input {
    font-size: 16px; /* Prevents zoom on iOS */
  }
  /* Better spacing */
  .post-body {
    padding: 0 1rem 3rem;
  }
  .post-hero {
    padding: 2rem 1rem 2rem;
  }
}

@media (min-width: 769px) {
  .hamburger, .menu-overlay {
    display: none;
  }
}

[dir="rtl"] .nav-links {
  left: auto;
  right: -100%;
}
[dir="rtl"] .nav-links.open {
  left: auto;
  right: 0;
  border-right: none;
  border-left: 1px solid var(--border-glow);
}
[dir="rtl"] .share-buttons {
  flex-direction: row-reverse;
}
</style>

<script>
// ============================================
// VIEW COUNTER (localStorage based)
// ============================================
function initViewCounter() {
  const articleKey = 'view_' + window.location.pathname.replace(/\\//g, '_');
  let views = localStorage.getItem(articleKey);
  
  if (!views) {
    views = 1;
    localStorage.setItem(articleKey, views);
  } else {
    views = parseInt(views) + 1;
    localStorage.setItem(articleKey, views);
  }
  
  const viewCountSpan = document.getElementById('viewCount');
  if (viewCountSpan) {
    viewCountSpan.textContent = views.toLocaleString();
  }
  
  // Update label based on language
  const lang = localStorage.getItem('pixelzoneLang') || 'en';
  const viewLabel = document.getElementById('viewLabel');
  if (viewLabel) {
    viewLabel.textContent = lang === 'ar' ? 'مشاهدة' : 'views';
  }
}

// ============================================
// SHARE FUNCTIONS
// ============================================
const currentUrl = encodeURIComponent(window.location.href);
const currentTitle = encodeURIComponent(document.title);

function shareOnTwitter() {
  window.open(`https://twitter.com/intent/tweet?text=${currentTitle}&url=${currentUrl}`, '_blank', 'width=550,height=420');
}

function shareOnWhatsApp() {
  window.open(`https://wa.me/?text=${currentTitle}%20${currentUrl}`, '_blank', 'width=550,height=420');
}

function shareOnTelegram() {
  window.open(`https://t.me/share/url?url=${currentUrl}&text=${currentTitle}`, '_blank', 'width=550,height=420');
}

async function copyLink() {
  try {
    await navigator.clipboard.writeText(window.location.href);
    const copyBtn = document.querySelector('.share-btn.copy');
    const originalText = copyBtn.textContent;
    copyBtn.textContent = '✓ COPIED!';
    copyBtn.style.background = '#39ff14';
    setTimeout(() => {
      copyBtn.textContent = originalText;
      copyBtn.style.background = 'var(--neon-cyan)';
    }, 2000);
  } catch (err) {
    alert('Press Ctrl+C to copy the link');
  }
}

// ============================================
// MOBILE HAMBURGER MENU
// ============================================
function initMobileMenu() {
  const nav = document.querySelector('nav');
  const navLinks = document.querySelector('.nav-links');
  const langToggle = document.querySelector('.lang-toggle');
  
  // Don't add if already exists
  if (document.querySelector('.hamburger')) return;
  
  // Create hamburger button
  const hamburger = document.createElement('button');
  hamburger.className = 'hamburger';
  hamburger.setAttribute('aria-label', 'Menu');
  hamburger.innerHTML = '<span></span><span></span><span></span>';
  
  // Create overlay
  const overlay = document.createElement('div');
  overlay.className = 'menu-overlay';
  
  // Insert hamburger before lang-toggle
  if (langToggle) {
    nav.insertBefore(hamburger, langToggle);
  } else {
    nav.appendChild(hamburger);
  }
  document.body.appendChild(overlay);
  
  function toggleMenu() {
    navLinks.classList.toggle('open');
    hamburger.classList.toggle('open');
    overlay.classList.toggle('open');
    document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
  }
  
  hamburger.addEventListener('click', toggleMenu);
  overlay.addEventListener('click', toggleMenu);
  
  // Close menu when clicking a link
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      hamburger.classList.remove('open');
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

// ============================================
// BILINGUAL SUPPORT FOR SHARE TITLE
// ============================================
function updateShareTitle() {
  const lang = localStorage.getItem('pixelzoneLang') || 'en';
  const shareTitle = document.getElementById('shareTitle');
  if (shareTitle) {
    shareTitle.textContent = lang === 'ar' ? '📤 شارك هذا المقال' : '📤 SHARE THIS ARTICLE';
  }
}

// Listen for language changes
const originalSetLang = window.setLang;
if (typeof originalSetLang === 'function') {
  window.setLang = function(lang) {
    originalSetLang(lang);
    updateShareTitle();
    const viewLabel = document.getElementById('viewLabel');
    if (viewLabel) {
      viewLabel.textContent = lang === 'ar' ? 'مشاهدة' : 'views';
    }
  };
}

// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', function() {
  initViewCounter();
  initMobileMenu();
  updateShareTitle();
});
</script>'''

def add_to_html(file_path):
    """Add enhanced features to a single HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if features already exist
    if 'view-counter-section' in content:
        print(f"⏭️ Skipping {os.path.basename(file_path)} (already has view counter)")
        return False
    
    # Check if share buttons already exist (legacy)
    if 'share-section' in content and 'view-counter-section' not in content:
        print(f"🔄 Upgrading {os.path.basename(file_path)} (adding view counter)")
    
    # Find where to insert the enhanced code
    insert_positions = [
        ('</div>\n\n<footer>', enhanced_code + '\n\n<footer>'),
        ('</div>\n<footer>', enhanced_code + '\n<footer>'),
    ]
    
    for search, replacement in insert_positions:
        if search in content:
            new_content = content.replace(search, replacement)
            break
    else:
        # Last resort: insert before footer
        new_content = content.replace('<footer>', enhanced_code + '\n<footer>')
    
    # Write back the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    # Find all HTML files
    html_files = glob(os.path.join(articles_folder, '*.html'))
    
    if not html_files:
        print(f"❌ No HTML files found in {articles_folder}")
        return
    
    print(f"📁 Found {len(html_files)} article(s)\n")
    
    updated_count = 0
    for file_path in html_files:
        if add_to_html(file_path):
            updated_count += 1
            print(f"✅ Updated: {os.path.basename(file_path)}")
    
    print(f"\n🎉 Done! Updated {updated_count} article(s).")
    
    if updated_count == 0:
        print("\n💡 Tip: Make sure your articles have the standard structure:")
        print("   - Closing </div> before <footer>")
        print("   - Or add them manually to your template")

if __name__ == '__main__':
    main()