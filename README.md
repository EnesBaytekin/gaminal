# Gaminal

Pygame tabanlı 2D oyun yapma framework'ü. JSON dosyaları ve assetler ile kod yazmadan oyun geliştirin.

## Özellikler

- **JSON Tabanlı**: Kod yazmadan sahne tasarımı
- **Component Sistemi**: Entity-Component mimarisi
- **Custom Script'ler**: Python ile oyun logic'i
- **Animasyon Desteği**: Sprite sheet + frame listesi
- **Y-Sorting**: Derinlik sıralaması
- **Asset Formatları**: PNG, JPG desteği
- **Kolay Kullanım**: Basit API, hızlı geliştirme

## Kurulum

```bash
# Virtual environment oluştur
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# veya
.venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

## Hızlı Başlangıç

### 1. Sahne Oluştur

`scene_data.json`:
```json
{
  "width": 800,
  "height": 600,
  "background_color": "#4488ff",
  "objects": [
    {
      "x": 400,
      "y": 300,
      "components": [
        {
          "type": "image",
          "file": "player.png",
          "pivot_x": "center",
          "pivot_y": "center"
        }
      ]
    }
  ]
}
```

### 2. Script Yaz (Opsiyonel)

`PlayerController.py`:
```python
import pygame
from gaminal import *

class PlayerController:
    def update(self, obj):
        app = App()
        im = InputManager()

        if im.is_pressed(pygame.K_LEFT):
            obj.x -= 200 * app.dt
        if im.is_pressed(pygame.K_RIGHT):
            obj.x += 200 * app.dt
```

### 3. Çalıştır

```python
from gaminal import *
run_app("scene_data.json")
```

## Kullanım

```bash
# Sample game'i çalıştır
cd sample-game
PYTHONPATH=/path/to/pygamer python main.py

# Kendi oyunun için
python main.py
```

## Proje Yapısı

```
my-game/
├── scene_data.json    # Sahne tanımı
├── main.py            # Entry point
├── images/            # Assetler
│   ├── player.png
│   └── enemy.png
└── scripts/           # Custom script'ler
    └── PlayerController.py
```

## Örnekler

Sample-game dizininde tam örnek bulunmaktadır.

- Hareket: WASD
- Aksiyon: Space
- Çıkış: Pencereyi kapat

## Build (Tek Dosya Executable)

Oyun projenizi **PyInstaller** ile tek bir `.exe`/ELF binary'sine derleyip başka makinelere taşıyabilirsiniz. Tüm assetler, script'ler ve framework binary'nin içine gömülür; çalıştırmak için Python kurulu olması gerekmez.

### 1. Build aracını yükle

```bash
# Virtual environment'da pygaminal + build bağımlılıklarını kur
pip install "pygaminal[build]"
# ya da geliştirme ortamında:
pip install -e ".[build]"
```

### 2. Oyun projeni build et

```bash
# Oyun dizinine git
cd /path/to/my-game

# Build'i çalıştır
pygaminal-build
```

Komut, içinde `main.py` bulunan dizini tarar, tüm assetleri tespit eder ve `build/` dizini altında tek bir executable oluşturur:

```
my-game/
├── main.py
├── scene_data.json
├── images/…
├── sounds/…
├── scripts/…
└── build/              ← oluşturulan dizin
    └── my-game         ← tek dosya executable
```

### Seçenekler

```bash
# Farklı bir dizini build et
pygaminal-build /path/to/game -n oyun-adi

# Çıktı adını değiştir
pygaminal-build -n MyGame

# Farklı çıktı dizini
pygaminal-build -o ./dist

# Yardım
pygaminal-build --help
```

### Önemli notlar

- **Script'leriniz `importlib` ile yükleniyorsa** (ör. `@PlayerMovementScript`), build aracı bunları otomatik tespit eder ve gizli import olarak ekler.
- **Built-in component'ler** (`@Hitbox`, `@Image`, `@Animation` vb.) otomatik olarak dahil edilir.
- Binary **tek dosyadır** — `build/` dizininde başka hiçbir dosya bırakılmaz.
- Çalıştırmak için binary'i herhangi bir Linux/macOS/Windows makineye kopyalayıp çalıştırmanız yeterli (pygame'in SDL kütüphaneleri dışında ek bağımlılık gerekmez).

## Dokümantasyon

Detaylı dokümantasyon için [DOCUMENTATION.md](DOCUMENTATION.md) dosyasına bakın.

## Lisans

MIT
