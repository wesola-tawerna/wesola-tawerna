#!/usr/bin/env python3
"""
Automatycznie aktualizuje sekcję galerii w index.html na podstawie plików z assets/gallery/.

UŻYCIE:
    1. Wrzuć nowe zdjęcia do assets/gallery/
    2. Otwórz terminal w folderze projektu (tam gdzie index.html)
    3. Uruchom: python update-gallery.py
    4. Sprawdź czy wszystko OK, potem: git add index.html && git commit -m "aktualizacja galerii" && git push

ALT_MAP: dopisz tu opisy dla nowych plików, żeby były czytelne dla SEO.
"""

import json
import os
import re
import shutil
from pathlib import Path

# ── KONFIGURACJA ──
HTML_FILE = Path("index.html")
GALLERY_DIR = Path("assets/gallery")
BACKUP_FILE = Path("index.html.bak")

ALT_MAP = {
    "karkowka.jpg": "Karkówka i kiełbasa prosto z grilla w Wesołej Tawernie",
    "ognisko.png": "Ognisko i wieczorny klimat w ogródku piwnym",
    "karaoke.jpg": "Wieczór karaoke w Wesołej Tawernie",
    "sport.png": "Transmisje sportowe na dużym ekranie w ogródku piwnym",
    "lody.jpg": "Lody gałkowe z lady chłodniczej w Wesołej Tawernie",
    "wejscie.jpg": "Wejście do Wesołej Tawerny na Białołęce",
}

# ── FUNKCJE POMOCNICZE ──
def get_gallery_images():
    """Znajduje wszystkie zdjęcia w assets/gallery/ i sortuje alfabetycznie."""
    if not GALLERY_DIR.exists():
        print(f"❌ Folder {GALLERY_DIR} nie istnieje!")
        return []
    
        images = []
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.mp4", "*.webm"):
            for f in sorted(GALLERY_DIR.glob(ext)):
                images.append(f.name)
        return images

def generate_gallery_html(images):
    """Generuje bloki HTML dla galerii."""
    lines = []
    for idx, name in enumerate(images):
        alt = ALT_MAP.get(name, f"Zdjęcie z Wesołej Tawerny – {name}")
        path = f"assets/gallery/{name}"
        is_video = name.lower().endswith(('.mp4', '.webm'))
        
        # Klasy CSS
        classes = ["gallery-item"]
        if idx == 0:
            classes.append("gallery-item--feature")
        if idx >= 4:
            classes.append("gallery-hidden")
        
        class_attr = " ".join(classes)
        
        # Dla pierwszego zdjęcia większe wymiary (feature)
        w = 800 if idx == 0 else 600
        h = 600 if idx == 0 else 600
        
        if is_video:
            btn = f'''          <button class="{class_attr}" type="button" data-lightbox="{path}" aria-label="Odtwórz wideo">
            <video src="{path}" muted autoplay loop playsinline preload="metadata" width="{w}" height="{h}" aria-label="{alt}"></video>
          </button>'''
        else:
            btn = f'''          <button class="{class_attr}" type="button" data-lightbox="{path}" aria-label="Powiększ zdjęcie">
            <img src="{path}" alt="{alt}" width="{w}" height="{h}" loading="lazy">
          </button>'''
        lines.append(btn)
    
    return "\n".join(lines)

def update_html(gallery_html):
    """Wstawia wygenerowany HTML do index.html, zachowując resztę pliku."""
    if not HTML_FILE.exists():
        print(f"❌ Plik {HTML_FILE} nie istnieje!")
        return False
    
    content = HTML_FILE.read_text(encoding="utf-8")
    
    # Tworzymy backup
    shutil.copy2(HTML_FILE, BACKUP_FILE)
    print(f"💾 Kopia zapasowa: {BACKUP_FILE}")
    
    # Szukamy sekcji galerii: <div class="gallery-grid" id="gallery-grid"> ... </div>
    # Używamy regex z trybem DOTALL, żeby przechwycić wieloliniową zawartość
    pattern = re.compile(
        r'(<div class="gallery-grid" id="gallery-grid">)\s*.*?(\s*</div>)',
        re.DOTALL
    )
    
    replacement = f'\\1\n{gallery_html}\\2'
    
    new_content, count = pattern.subn(replacement, content)
    
    if count == 0:
        print("❌ Nie znaleziono sekcji gallery-grid w index.html!")
        print("   Szukam: <div class=\"gallery-grid\" id=\"gallery-grid\"> ... </div>")
        return False
    
    HTML_FILE.write_text(new_content, encoding="utf-8")
    return True

# ── GŁÓWNY PROGRAM ──
def main():
    print("🔍 Skanowanie folderu assets/gallery/...")
    images = get_gallery_images()
    
    if not images:
        print("⚠️  Nie znaleziono żadnych zdjęć w assets/gallery/")
        return
    
    print(f"📷 Znaleziono {len(images)} zdjęć:")
    for img in images:
        mark = "✓" if img in ALT_MAP else "?"
        print(f"   {mark} {img}")
    
    print("\n📝 Generowanie HTML...")
    gallery_html = generate_gallery_html(images)
    
    print("💉 Aktualizacja index.html...")
    if update_html(gallery_html):
        print(f"✅ Gotowe! Zaktualizowano {len(images)} zdjęć w galerii.")
        print(f"   Pierwsze 4 zdjęcia widoczne, reszta ukryta pod przyciskiem.")
        print(f"\n🚀 Teraz wypchnij zmiany na GitHub:")
        print(f"   git add index.html")
        print(f"   git commit -m \"aktualizacja galerii – {len(images)} zdjęcia\"")
        print(f"   git push")
        
        # Nieznane zdjęcia ostrzeżenie
        unknown = [i for i in images if i not in ALT_MAP]
        if unknown:
            print(f"\n⚠️  Brak opisu ALT dla plików: {', '.join(unknown)}")
            print(f"   Edytuj ALT_MAP w pliku update-gallery.py, żeby poprawić SEO.")
    else:
        print("❌ Coś poszło nie tak. Sprawdź czy index.html ma poprawną strukturę.")

if __name__ == "__main__":
    main()
