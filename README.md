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

## Dokümantasyon

Detaylı dokümantasyon için [DOCUMENTATION.md](DOCUMENTATION.md) dosyasına bakın.

## Lisans

MIT
