# PyGamer Framework Documentation

Pygame tabanlı 2D oyun yapma framework'ü. JSON + assetler ile oyun geliştirme.

## Proje Yapısı

```
pygamer/
├── gaminal/                    # Core engine
│   ├── __init__.py            # run_app() fonksiyonu
│   ├── app.py                 # Singleton: Ana oyun döngüsü
│   ├── scene.py               # Singleton: Sahne yönetimi
│   ├── object.py              # Entity-Component System
│   ├── component.py           # Base Component
│   ├── image.py               # PNG/JPG yükleme
│   ├── image_component.py    # Sprite çizim
│   ├── animation.py           # Animasyon sistemi
│   ├── animation_component.py # Animasyon çizim
│   ├── custom_component.py   # Python script entegrasyonu
│   ├── ysort_component.py    # Y eksenine göre depth sorting
│   ├── screen.py              # Singleton: Pygame Surface yönetimi
│   ├── input_manager.py       # Singleton: Input handling
│   └── util.py                # Yardımcı fonksiyonlar
└── sample-game/               # Örnek oyun
    ├── scene_data.json        # Sahne tanımı
    ├── main.py                # Entry point
    ├── MovementScript.py      # Custom script
    ├── ExplosionScript.py     # Custom script
    ├── explosion.obj          # Object template
    └── images/                # Assetler (PNG)
```

## Core Sınıflar

### App (Singleton)
Ana uygulama yöneticisi.

```python
from gaminal import App
app = App()
app.init(width=800, height=600, title="My Game")
app.run()
```

**Özellikler:**
- `width`, `height`, `title` - Pencere ayarları
- `now` - Şu anki zaman (saniye)
- `dt` - Delta time (frame arası geçen süre)
- `target_fps` - FPS limiti (default: 60)

**Metodlar:**
- `add_scene(name, scene)` - Sahne ekle
- `set_scene(name)` - Aktif sahneyi değiştir
- `get_current_scene()` - Aktif sahne
- `stop()` - Oyunu durdur

### Screen (Singleton)
Render yüzeyi.

```python
from gaminal import Screen
screen = Screen()
screen.init(800, 600)
screen.set_background_color("#3366ff")
screen.set_background_image("bg.png")
screen.clear()  # Arka planı çiz
screen.blit(image, x, y)  # Image çiz
screen.refresh()  # Display güncelle
```

### InputManager (Singleton)
Input yönetimi.

```python
from gaminal import InputManager
import pygame

im = InputManager()
im.update()  # Frame başı çağır

# Key kontrolü
if im.is_pressed(pygame.K_w):  # Basılı mı
if im.is_just_pressed(pygame.K_SPACE):  # Just basıldı mı
if im.is_released(pygame.K_a):  # Bırakıldı mı
```

### Scene
Objeleri tutan konteyner.

```python
from gaminal import Scene

scene = Scene()
scene.add_object(obj)  # Obje ekle
scene.update()  # Tüm objeleri update et
scene.draw()  # Tüm objeleri çiz
```

**Property'ler:**
- `width`, `height` - Sahne boyutu
- `background_color` - Hex color string
- `background_image` - Dosya yolu

### Object
Entity-Component mimarisi.

```python
from gaminal import Object

obj = Object(x, y)
obj.add_component("image", image_component)
obj.add_component("custom", custom_component)
obj.kill()  # Objeyi yok et (sahneden sil)
```

**Property'ler:**
- `x`, `y` - Pozisyon
- `dead` - Öldü mü?
- `depth` - Çizim derinliği (YSortComponent ile otomatik)

### Image
Resim yükleme.

```python
from gaminal import Image

img = Image.from_file("sprite.png")
# img.width, img.height
```

### Animation
Animasyon sistemi.

**Sprite Sheet:**
```python
from gaminal import Animation

anim = Animation.from_sprite_sheet(
    "sprite.png",
    frame_width=32,
    frame_height=32,
    frames=[0, 1, 2, 3],  # Optional, None = tüm frame'ler
    speed=10,
    loop=True
)
```

**Frame Listesi:**
```python
anim = Animation.from_files([
    "idle_0.png",
    "idle_1.png",
    "idle_2.png"
], speed=5, loop=False)
```

**Metodlar:**
- `start()` - Animasyonu başlat
- `get_frame()` - Şu anki frame'i al
- `is_over()` - Bitti mi?

## Component'ler

### ImageComponent
Tek frame çizim.

```python
from gaminal import Image, ImageComponent

img = Image.from_file("player.png")
comp = ImageComponent(img)
comp.set_pivot("center", "end")  # Pivot noktası
# "center", "end" veya pixel değeri
```

### AnimationComponent
Animasyon çizim.

```python
from gaminal import Animation, AnimationComponent

anim = Animation.from_sprite_sheet("walk.png", 32, 32, speed=8)
comp = AnimationComponent(anim)
comp.set_pivot("center", "end")
```

### CustomComponent
Python script entegrasyonu.

Script dosyası (`MovementScript.py`):
```python
import pygame
from gaminal import *

class MovementScript:
    def __init__(self):
        self.speed = 200

    def update(self, object):
        app = App()
        im = InputManager()

        if im.is_pressed(pygame.K_d):
            object.x += self.speed * app.dt
        if im.is_pressed(pygame.K_a):
            object.x -= self.speed * app.dt
```

### YSortComponent
Y pozisyonuna göre depth ayarlama (derinlik sıralaması için).

```python
from gaminal import YSortComponent
obj.add_component("ysort", YSortComponent())
```

## JSON Formatı

### Sahne Dosyası (scene_data.json)

```json
{
  "width": 800,
  "height": 600,
  "background_color": "#222222",
  "background_image": "bg.png",
  "objects": [
    {
      "x": 100,
      "y": 200,
      "components": [
        {
          "type": "image",
          "file": "images/player.png",
          "pivot_x": "center",
          "pivot_y": "end"
        },
        {
          "type": "custom",
          "file": "MovementScript.py"
        },
        {
          "type": "ysort"
        }
      ]
    },
    {
      "x": 300,
      "y": 150,
      "components": [
        {
          "type": "animation",
          "file": "images/explosion.png",
          "frame_width": 32,
          "frame_height": 32,
          "frames": [0, 1, 2, 3],
          "speed": 10,
          "loop": false,
          "pivot_x": "center",
          "pivot_y": "center"
        },
        {
          "type": "custom",
          "file": "ExplosionScript.py",
          "args": [1.5]
        }
      ]
    }
  ]
}
```

### Object Template (.obj)

JSON formatında tekrar kullanılabilir objeler.

```json
{
  "components": [
    {
      "type": "image",
      "file": "images/box.png",
      "pivot_x": "center",
      "pivot_y": "end"
    }
  ]
}
```

Kullanım:
```python
obj = Object.from_file("box.obj", x, y)
```

## Asset Formatları

### Resimler
- PNG, JPG desteklenir
- Alpha channel (PNG) önerilir
- Pixe-based koordinatlar

### Animasyonlar
1. **Sprite Sheet**: Tek resim, grid layout
2. **Frame Listesi**: Birden fazla resim dosyası

## Script Yazma

### Script Template

```python
import pygame
from gaminal import *

class MyScript:
    def __init__(self, arg1, arg2=None):
        # Constructor, JSON args'dan değer alır
        self.value = arg1

    def update(self, object):
        # Her frame çağrılır
        app = App()
        im = InputManager()

        # Input
        if im.is_pressed(pygame.K_SPACE):
            # Aksiyon
            pass

        # Hareket
        object.x += 100 * app.dt

        # Obje yaratma
        new_obj = Object(100, 100)
        scene = app.get_current_scene()
        scene.add_object(new_obj)

        # Obje yok etme
        if object.x > 800:
            object.kill()

    def draw(self, object):
        # Opsiyonel: Custom drawing
        pass
```

### Global Nesneler
Scriptlerde her zaman erişilebilir:
- `App()` - Singleton app instance
- `InputManager()` - Singleton input manager
- `Screen()` - Singleton screen

## Çalıştırma

### Kurulum
```bash
cd /home/imns/Desktop/pygamer
python3 -m venv .venv
source .venv/bin/activate
pip install pygame
```

### Oyun Çalıştırma
```bash
cd sample-game
PYTHONPATH=/home/imns/Desktop/pygamer python main.py
```

Veya:
```python
from gaminal import *
run_app("scene_data.json")
```

## Hızlı Tutorial

### Adım 1: Sahne Oluştur

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
        },
        {
          "type": "custom",
          "file": "PlayerController.py"
        }
      ]
    }
  ]
}
```

### Adım 2: Script Yaz

`PlayerController.py`:
```python
import pygame
from gaminal import *

class PlayerController:
    def update(self, obj):
        app = App()
        im = InputManager()

        speed = 200
        if im.is_pressed(pygame.K_LEFT):
            obj.x -= speed * app.dt
        if im.is_pressed(pygame.K_RIGHT):
            obj.x += speed * app.dt
        if im.is_pressed(pygame.K_UP):
            obj.y -= speed * app.dt
        if im.is_pressed(pygame.K_DOWN):
            obj.y += speed * app.dt
```

### Adım 3: Çalıştır

```bash
PYTHONPATH=/path/to/pygamer python main.py
```

### Adım 4: Kontroller
- **Arrow Keys** - Hareket
- **Close Window** - Çıkış

## Pygame Key Constants

```python
pygame.K_a, pygame.K_b, ...  # Harfler
pygame.K_0, pygame.K_1, ...  # Rakamlar
pygame.K_SPACE               # Space
pygame.K_ESCAPE              # Escape
pygame.K_RETURN              # Enter
pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN  # Yön tuşları
```

## Tips

1. **Delta Time Kullan**: Her zaman `app.dt` ile çarparak hareket ettir
2. **Pivot**: Karakter için `"center"`, zemin objeleri için `"end"` kullan
3. **Depth Sorting**: YSortComponent ekle, objeler otomatik sıralanır
4. **Animasyon**: Sprite sheet kullan, performans için
5. **Cleanup**: Biten objeleri `object.kill()` ile yok et
6. **Cooldows**: `app.now` kullanarak rate limiting yap

## Component API

### Tüm Component'ler
```python
component.update(object)  # Her frame
component.draw(object)   # Çizim anı
```

### Custom Component
```python
# JSON
{
  "type": "custom",
  "file": "Script.py",
  "args": [arg1, arg2]  # Constructor'a geçilir
}
```

Script'te:
```python
class Script:
    def __init__(self, arg1, arg2):
        # args: Constructor parametresi
        pass
    def update(self, object):
        pass
    def draw(self, object):
        pass
```

## Sahne Yönetimi

```python
# Sahne değiştirme
app.set_scene("level2")

# Sahne'den obje silme
object.kill()

# Scene objelerine erişim
scene.objects
```

## Gelişmiş Özellikler

### Custom Rendering (Script)
```python
def draw(self, object):
    screen = Screen()
    # Custom drawing logic
```

### Multiple Animations
```python
# İki animasyon component'i aynı objede
obj.add_component("walk", walk_anim_component)
obj.add_component("idle", idle_anim_component)
```

### Object Communication
```python
# Script'ten diğer objeye erişim
scene = app.get_current_scene()
for other_obj in scene.objects:
    if other_obj != object:
        # İletişim
        pass
```
