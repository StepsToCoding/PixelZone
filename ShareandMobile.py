import os
from glob import glob

articles_folder = './Articles/articles/'

# Fixed JavaScript with proper view counter
JS_FIXED = '''
<script>
// ============================================
// VIEW COUNTER - FIXED VERSION
// ============================================
function initViewCounter() {
    console.log("Initializing view counter...");
    
    // Get unique key for this article
    let path = window.location.pathname;
    let articleKey = 'view_' + path.replace(/\\//g, '_').replace(/[^a-zA-Z0-9_]/g, '_');
    
    // Get or increment view count
    let views = localStorage.getItem(articleKey);
    if (!views) {
        views = 1;
    } else {
        views = parseInt(views) + 1;
    }
    localStorage.setItem(articleKey, views);
    
    // Update all view counter displays
    let viewSpans = document.querySelectorAll('.view-count-display');
    console.log("Found " + viewSpans.length + " view counter(s)");
    viewSpans.forEach(function(span) {
        span.textContent = views.toLocaleString();
    });
    
    // Update language for view label
    let lang = localStorage.getItem('pixelzoneLang') || 'en';
    let labels = document.querySelectorAll('.view-label');
    labels.forEach(function(label) {
        label.textContent = lang === 'ar' ? 'مشاهدة' : 'views';
    });
}

// ============================================
// SHARE FUNCTIONS
// ============================================
function shareOnTwitter() {
    let url = encodeURIComponent(window.location.href);
    let title = encodeURIComponent(document.title);
    window.open('https://twitter.com/intent/tweet?text=' + title + '&url=' + url, '_blank', 'width=550,height=420');
}

function shareOnWhatsApp() {
    let url = encodeURIComponent(window.location.href);
    let title = encodeURIComponent(document.title);
    window.open('https://wa.me/?text=' + title + '%20' + url, '_blank', 'width=550,height=420');
}

function shareOnTelegram() {
    let url = encodeURIComponent(window.location.href);
    let title = encodeURIComponent(document.title);
    window.open('https://t.me/share/url?url=' + url + '&text=' + title, '_blank', 'width=550,height=420');
}

async function copyLink() {
    try {
        await navigator.clipboard.writeText(window.location.href);
        let copyBtn = document.querySelector('.share-btn.copy');
        let originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ COPIED!';
        copyBtn.style.background = '#39ff14';
        setTimeout(function() {
            copyBtn.textContent = originalText;
            copyBtn.style.background = 'var(--neon-cyan)';
        }, 2000);
    } catch(err) {
        alert('Press Ctrl+C to copy the link');
    }
}

// Run when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initViewCounter);
} else {
    initViewCounter();
}
</script>'''

# View counter HTML with correct class names
VIEW_COUNTER_HTML = '''
  <div class="view-counter-section">
    <div class="view-counter">
      <span class="view-icon">👁️</span>
      <span class="view-count-display">0</span>
      <span class="view-label">views</span>
    </div>
  </div>'''

SHARE_BUTTONS_HTML = '''
  <div class="share-section">
    <div class="glow-divider" style="margin: 2rem 0 1.5rem;"></div>
    <div class="share-title">📤 SHARE THIS ARTICLE</div>
    <div class="share-buttons">
      <button class="share-btn twitter" onclick="shareOnTwitter()">🐦 Twitter</button>
      <button class="share-btn whatsapp" onclick="shareOnWhatsApp()">📱 WhatsApp</button>
      <button class="share-btn telegram" onclick="shareOnTelegram()">✈️ Telegram</button>
      <button class="share-btn copy" onclick="copyLink()">🔗 Copy Link</button>
    </div>
  </div>'''

def fix_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    filename = os.path.basename(file_path)
    print(f"\n📄 {filename}")
    
    # Remove old JavaScript and add new fixed version
    if 'initViewCounter' in content:
        # Remove old script block
        import re
        content = re.sub(r'<script>.*?initViewCounter.*?</script>', '', content, flags=re.DOTALL)
        print("   ✅ Removed old JavaScript")
    
    # Add new JavaScript before </body>
    if '</body>' in content:
        content = content.replace('</body>', JS_FIXED + '\n</body>')
        modified = True
        print("   ✅ Added fixed JavaScript")
    
    # Ensure view counter HTML is in English section
    if 'contentEn' in content and 'view-count-display' not in content.split('contentEn')[1].split('contentAr')[0] if 'contentAr' in content else True:
        # Find where to insert
        if 'contentEn' in content:
            en_part = content.split('contentEn')[1]
            if 'contentAr' in en_part:
                en_end = en_part.split('contentAr')[0]
                last_div = en_end.rfind('</div>')
                if last_div != -1:
                    insert_pos = content.find('contentEn') + last_div + 7
                    content = content[:insert_pos] + f'\n\n{VIEW_COUNTER_HTML}\n{SHARE_BUTTONS_HTML}\n' + content[insert_pos:]
                    modified = True
                    print("   ✅ Added view counter to English section")
    
    # Ensure in Arabic section
    if 'contentAr' in content and 'view-count-display' not in content.split('contentAr')[1].split('<footer>')[0]:
        ar_part = content.split('contentAr')[1]
        footer_pos = ar_part.find('<footer>') if '<footer>' in ar_part else ar_part.find('</div>')
        if footer_pos != -1:
            insert_pos = content.find('contentAr') + footer_pos
            content = content[:insert_pos] + f'\n\n{VIEW_COUNTER_HTML}\n{SHARE_BUTTONS_HTML}\n' + content[insert_pos:]
            modified = True
            print("   ✅ Added view counter to Arabic section")
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   ✨ Article fixed!")
    else:
        print("   ⏭️ No changes needed")
    
    return modified

def main():
    print("=" * 60)
    print("🔧 Fixing View Counter - 'Loading' Issue")
    print("=" * 60)
    
    files = glob(os.path.join(articles_folder, '*.html'))
    
    if not files:
        print(f"\n❌ No articles found in {articles_folder}")
        return
    
    print(f"\n📁 Found {len(files)} article(s)")
    
    updated_count = 0
    for file_path in files:
        if fix_article(file_path):
            updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"🎉 Done! Fixed {updated_count} article(s).")
    print("=" * 60)
    print("\n📝 Refresh your article page - view counter should now show a number!")

if __name__ == '__main__':
    main()