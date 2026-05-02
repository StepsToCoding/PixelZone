import os
import re
from glob import glob

articles_folder = './Articles/articles/'

# Components to add
VIEW_COUNTER_HTML = '''
  <div class="view-counter-section">
    <div class="view-counter">
      <span class="view-icon">👁️</span>
      <span class="view-count-display">Loading...</span>
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

STYLES = '''
.view-counter-section{display:flex;justify-content:center;margin:1.5rem 0 0}
.view-counter{display:inline-flex;align-items:center;gap:8px;background:var(--bg-card);border:1px solid var(--border-glow);padding:8px 20px;border-radius:40px;font-family:Orbitron,monospace;font-size:.85rem;color:var(--text-main)}
.view-icon{font-size:1.1rem}
.view-count-display{font-weight:700;color:var(--neon-cyan);font-size:1rem}
.view-label{color:var(--text-muted);font-size:.7rem}
.share-section{margin:2rem 0 1rem;text-align:center}
.share-title{font-family:Orbitron,monospace;font-size:.7rem;letter-spacing:2px;color:var(--text-muted);margin-bottom:1rem}
.share-buttons{display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap}
.share-btn{font-family:Orbitron,monospace;font-size:.7rem;font-weight:600;letter-spacing:1px;padding:8px 18px;border:none;cursor:pointer;clip-path:polygon(6px 0%,100% 0%,calc(100%-6px)100%,0%100%);color:#080b14}
.share-btn:hover{transform:translateY(-2px);filter:brightness(.9)}
.share-btn.twitter{background:#1DA1F2}
.share-btn.whatsapp{background:#25D366}
.share-btn.telegram{background:#0088cc}
.share-btn.copy{background:var(--neon-cyan);color:#080b14}'''

JS = '''
<script>
function initViewCounter(){let k="view_"+location.pathname.replace(/\\//g,"_"),v=localStorage.getItem(k);v=v?parseInt(v)+1:1;localStorage.setItem(k,v);document.querySelectorAll(".view-count-display").forEach(s=>s.textContent=v.toLocaleString());let l=localStorage.getItem("pixelzoneLang")||"en";document.querySelectorAll(".view-label").forEach(s=>s.textContent=l==="ar"?"مشاهدة":"views")}
const cu=encodeURIComponent(location.href),ct=encodeURIComponent(document.title);
function shareOnTwitter(){open(`https://twitter.com/intent/tweet?text=${ct}&url=${cu}`,"_blank","width=550,height=420")}
function shareOnWhatsApp(){open(`https://wa.me/?text=${ct}%20${cu}`,"_blank","width=550,height=420")}
function shareOnTelegram(){open(`https://t.me/share/url?url=${cu}&text=${ct}`,"_blank","width=550,height=420")}
async function copyLink(){try{await navigator.clipboard.writeText(location.href);let b=document.querySelector(".share-btn.copy"),t=b.textContent;b.textContent="✓ COPIED!";b.style.background="#39ff14";setTimeout(()=>{b.textContent=t;b.style.background="var(--neon-cyan)"},2000)}catch(e){alert("Press Ctrl+C to copy")}}
document.addEventListener("DOMContentLoaded",initViewCounter);
</script>'''

def fix_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    filename = os.path.basename(file_path)
    print(f"\n📄 {filename}")
    
    # 1. Add styles if missing
    if '.view-counter-section' not in content and '</style>' in content:
        content = content.replace('</style>', f'{STYLES}\n</style>')
        modified = True
        print("   ✅ Added CSS styles")
    
    # 2. Add share buttons to ENGLISH section
    if 'contentEn' in content and 'share-section' not in content.split('contentEn')[1].split('contentAr')[0] if 'contentAr' in content else True:
        # Find where to insert in English section
        if 'contentEn' in content:
            en_part = content.split('contentEn')[1]
            if 'contentAr' in en_part:
                en_end = en_part.split('contentAr')[0]
                # Find last closing div in English section
                last_div = en_end.rfind('</div>')
                if last_div != -1:
                    insert_pos = content.find('contentEn') + last_div + 7
                    content = content[:insert_pos] + f'\n\n{VIEW_COUNTER_HTML}\n{SHARE_BUTTONS_HTML}\n' + content[insert_pos:]
                    modified = True
                    print("   ✅ Added share buttons to English section")
    
    # 3. Add share buttons to ARABIC section
    if 'contentAr' in content and 'share-section' not in content.split('contentAr')[1].split('<footer>')[0]:
        ar_part = content.split('contentAr')[1]
        footer_pos = ar_part.find('<footer>') if '<footer>' in ar_part else ar_part.find('</div>')
        if footer_pos != -1:
            insert_pos = content.find('contentAr') + footer_pos
            content = content[:insert_pos] + f'\n\n{VIEW_COUNTER_HTML}\n{SHARE_BUTTONS_HTML}\n' + content[insert_pos:]
            modified = True
            print("   ✅ Added share buttons to Arabic section")
    
    # 4. Add JavaScript if missing
    if 'initViewCounter' not in content and '</body>' in content:
        content = content.replace('</body>', f'{JS}\n</body>')
        modified = True
        print("   ✅ Added JavaScript functions")
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   ✨ Article updated successfully!")
    else:
        print("   ⏭️ No changes needed (all features present)")
    
    return modified

def main():
    print("=" * 60)
    print("🔧 PixelZone Article Fixer - All in One")
    print("=" * 60)
    print("\nThis script will:")
    print("   • Add CSS styles for view counter & share buttons")
    print("   • Add view counter & share buttons to English section")
    print("   • Add view counter & share buttons to Arabic section")
    print("   • Add JavaScript functions for interactivity")
    print("-" * 60)
    
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
    print(f"🎉 Done! Updated {updated_count} out of {len(files)} article(s).")
    print("=" * 60)
    
    if updated_count > 0:
        print("\n📝 Next steps:")
        print("   1. Run: python generate_manifest.py")
        print("   2. Commit and push to GitHub")
        print("   3. Test an article to see share buttons and view counter!")

if __name__ == '__main__':
    main()