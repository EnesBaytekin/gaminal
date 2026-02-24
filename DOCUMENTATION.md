# PyGamer Framework Documentation

Pygame tabanlı 2D oyun yapma framework'ü. JSON + assetler ile oyun geliştirme.

## Proje Yapısı

```
pygamer/
├── pygaminal/                     # Core engine
│   ├── __init__.py               # run_app() fonksiyonu
│   ├── app.py                    # Singleton: Ana oyun döngüsü
│   ├── scene.py                  # Singleton: Sahne yönetimi
│   ├── object.py                 # Entity-Component System
│   ├── component.py              # Base Component
│   ├── script_component.py       # Universal component loader
│   ├── components/               # Built-in component script'leri
│   │   ├── ImageComponent.py    # Sprite çizim
│   │   ├── AnimationComponent.py # Animasyon çizim
│   │   └── YSortComponent.py    # Y eksenine göre depth sorting
│   ├── image.py                  # PNG/JPG yükleme
│   ├── animation.py              # Animasyon sistemi
│   ├── screen.py                 # Singleton: Pygame Surface yönetimi
│   ├── input_manager.py          # Singleton: Input handling
│   └── util.py                   # Yardımcı fonksiyonlar
└── sample-game/                  # Örnek oyun
    ├── scene_data.json           # Sahne tanımı
    ├── main.py                   # Entry point
    ├── MovementScript.py         # Custom script
    └── images/                   # Assetler (PNG)
```

## Core Sınıflar

### App (Singleton)
Ana uygulama yöneticisi.

```python
from pygaminal import App
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
from pygaminal import Screen
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
from pygaminal import InputManager
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
from pygaminal import Scene

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
from pygaminal import Object

obj = Object(x, y)
obj.add_component(component)
obj.kill()  # Objeyi yok et (sahneden sil)
```

**Property'ler:**
- `x`, `y` - Pozisyon
- `dead` - Öldü mü?
- `depth` - Çizim derinliği (YSortComponent ile otomatik)

**Metodlar:**
- `add_component(component, explicit_name=None)` - Component ekle
- `get_component(name)` - İsmi verilen component'i al
- `get_components(file_name)` - Tüm aynı türdeki component'leri al

## Component Sistemi

### Uniform Component Yapısı

Tüm component'ler **aynı format**ta script dosyalarıdır. Built-in component'ler ve user script'ler arasında fark yoktur.

#### Built-in Component'ler
Framework ile birlikte gelen component'ler. `@` prefix'i ile kullanılır:

```json
{"file": "@ImageComponent", "args": [...]}
{"file": "@AnimationComponent", "args": [...]}
{"file": "@YSortComponent", "args": []}
```

#### User-Defined Component'ler
Kullanıcının yazdığı script'ler. Dosya adı ile kullanılır:

```json
{"file": "MovementScript", "args": [200]}
{"file": "MyScript", "args": []}
```

### Component Script Formatı

Her component script'i aynı yapıdadır - **inheritance gerekmez**:

```python
# MyComponent.py
class MyComponent:
    def __init__(self, arg1, arg2=None):
        # Constructor
        self.value = arg1

    def update(self, obj):
        # Her frame çağrılır
        obj.x += 100 * app.dt

    def draw(self, obj):
        # Çizim anında çağrılır (opsiyonel)
        pass
```

### Built-in Component'ler

#### ImageComponent
Tek frame çizim.

```python
# JSON
{
  "file": "@ImageComponent",
  "name": "body",  // Optional
  "args": ["player.png", "center", "end"]
}
```

**Args:**
1. `image_or_path` - Image objesi veya dosya yolu
2. `pivot_x` - "center", "end", veya pixel değeri
3. `pivot_y` - "center", "end", veya pixel değeri

#### AnimationComponent
Animasyon çizim.

```python
# JSON
{
  "file": "@AnimationComponent",
  "args": [{
    "file": "walk.png",
    "frame_width": 32,
    "frame_height": 32,
    "frames": [0, 1, 2, 3],
    "speed": 10,
    "loop": true
  }]
}
```

**Args:**
- Animasyon data dict'i:
  - `file` - Sprite sheet dosya yolu
  - `frame_width` - Frame genişliği
  - `frame_height` - Frame yüksekliği
  - `frames` - Frame listesi (opsiyonel)
  - `speed` - Animasyon hızı
  - `loop` - Döngü mü?

#### YSortComponent
Y pozisyonuna göre depth ayarlama (derinlik sıralaması için).

```python
// JSON
{
  "file": "@YSortComponent",
  "args": []
}
```

## JSON Formatı

### Uniform Component Formatı

Tüm component'ler aynı formattadır:

```json
{
  "file": "ComponentName",      // Zorunlu: Component dosyası
  "name": "my_component",       // Opsiyonel: Unique isim
  "args": [arg1, arg2, ...]     // Opsiyonel: Constructor argümanları
}
```

### Component Kuralları

1. **`file`** - Zorunlu
   - `@` ile başlarsa → Built-in component (`@ImageComponent`)
   - `@` yoksa → User script (`MovementScript`)

2. **`name`** - Opsiyonel
   - Verilirse → Bu isimle eklenir
   - Verilmezse → Otomatik isim (`ImageComponent`, `ImageComponent2`, ...)

3. **`args`** - Opsiyonel
   - Component constructor'ına geçilecek parametreler

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
          "file": "@ImageComponent",
          "name": "body",
          "args": ["images/player.png", "center", "end"]
        },
        {
          "file": "MovementScript",
          "args": [200]
        },
        {
          "file": "@YSortComponent",
          "args": []
        }
      ]
    },
    {
      "x": 300,
      "y": 150,
      "components": [
        {
          "file": "@AnimationComponent",
          "args": [{
            "file": "images/explosion.png",
            "frame_width": 32,
            "frame_height": 32,
            "frames": [0, 1, 2, 3],
            "speed": 10,
            "loop": false
          }]
        }
      ]
    }
  ]
}
```

## Multiple Components

Aynı objeye birden fazla aynı türden component eklenebilir:

### Auto-Naming (isim verilmezse)

```json
{
  "components": [
    {"file": "@ImageComponent", "args": ["layer1.png"]},
    {"file": "@ImageComponent", "args": ["layer2.png"]},
    {"file": "@ImageComponent", "args": ["layer3.png"]}
  ]
}
```

Sonuç: `ImageComponent`, `ImageComponent2`, `ImageComponent3`

### Explicit Naming (isim verilirse)

```json
{
  "components": [
    {"file": "@ImageComponent", "name": "shadow", "args": ["shadow.png"]},
    {"file": "@ImageComponent", "name": "body", "args": ["body.png"]},
    {"file": "@ImageComponent", "name": "glow", "args": ["glow.png"]}
  ]
}
```

Sonuç: `shadow`, `body`, `glow`

### Component Erişimi

```python
# Tek component (unique name ile)
comp = obj.get_component("body")

// Tüm aynı türdeki component'ler
images = obj.get_components("@ImageComponent")  // List of components
scripts = obj.get_components("MovementScript")   // List of components
```

## Image & Animation

### Image
Resim yükleme.

```python
from pygaminal import Image

img = Image.from_file("sprite.png")
// img.width, img.height
```

### Animation
Animasyon sistemi.

**Sprite Sheet:**
```python
from pygaminal import Animation

anim = Animation.from_sprite_sheet(
    "sprite.png",
    frame_width=32,
    frame_height=32,
    frames=[0, 1, 2, 3],  // Optional, None = tüm frame'ler
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

## Script Yazma

### Script Template

```python
import pygame
from pygaminal import *

class MyScript:
    def __init__(self, arg1, arg2=None):
        // Constructor, JSON args'dan değer alır
        self.value = arg1

    def update(self, obj):
        // Her frame çağrılır
        app = App()
        im = InputManager()

        // Input
        if im.is_pressed(pygame.K_SPACE):
            // Aksiyon
            pass

        // Hareket
        obj.x += 100 * app.dt

        // Obje yaratma
        new_obj = Object(100, 100)
        scene = app.get_current_scene()
        scene.add_object(new_obj)

        // Obje yok etme
        if obj.x > 800:
            obj.kill()

    def draw(self, obj):
        // Opsiyonel: Custom drawing
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
from pygaminal import *
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
          "file": "@ImageComponent",
          "args": ["player.png", "center", "end"]
        },
        {
          "file": "PlayerController",
          "args": []
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
from pygaminal import *

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
pygame.K_a, pygame.K_b, ...  // Harfler
pygame.K_0, pygame.K_1, ...  // Rakamlar
pygame.K_SPACE               // Space
pygame.K_ESCAPE              // Escape
pygame.K_RETURN              // Enter
pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN  // Yön tuşları
```

## Tips

1. **Delta Time Kullan**: Her zaman `app.dt` ile çarparak hareket ettir
2. **Pivot**: Karakter için `"center"`, zemin objeleri için `"end"` kullan
3. **Depth Sorting**: YSortComponent ekle, objeler otomatik sıralanır
4. **Animasyon**: Sprite sheet kullan, performans için
5. **Cleanup**: Biten objeleri `object.kill()` ile yok et
6. **Cooldowns**: `app.now` kullanarak rate limiting yap
7. **Multiple Components**: Aynı objeye birden fazla ImageComponent ekleyebilirsin (shadow, body, glow)
8. **Component Naming**: Önemli component'lere explicit name ver, diğerlerini auto-name bırak

## Component Best Practices

### Built-in Kullan
Mümkünse built-in component'leri kullan:

```json
{"file": "@ImageComponent", "args": ["player.png", "center", "end"]}
```

### Custom Script Yaz
Özel logic için script yaz:

```python
// EnemyAI.py
class EnemyAI:
    def __init__(self, patrol_range=100):
        self.patrol_range = patrol_range
        self.start_x = 0

    def update(self, obj):
        app = App()
        // Patrol logic
        if obj.x > self.start_x + self.patrol_range:
            obj.x -= 100 * app.dt
        elif obj.x < self.start_x:
            obj.x += 100 * app.dt
```

```json
{"file": "EnemyAI", "args": [150]}
```

### Component Reuse
İyi yazılmış bir script'i built-in yap:
1. Script'i `pygaminal/components/` dizinine kopyala
2. JSON'da `@` prefix ile kullan

## Sahne Yönetimi

```python
// Sahne değiştirme
app.set_scene("level2")

// Sahne'den obje silme
object.kill()

// Scene objelerine erişim
scene = app.get_current_scene()
for obj in scene.objects:
    // Objeleri gez
    pass
```

## Gelişmiş Özellikler

### Custom Rendering (Script)
```python
def draw(self, obj):
    screen = Screen()
    // Custom drawing logic
    screen.draw_circle(obj.x, obj.y, 10, (255, 0, 0))
```

### Multiple Components
```python
// Birden fazla ImageComponent
obj.get_components("@ImageComponent")  // [shadow, body, glow]

// Birden fazla aynı script
obj.get_components("AttackScript")  // [melee, ranged]
```

### Object Communication
```python
// Script'ten diğer objeye erişim
scene = app.get_current_scene()
for other_obj in scene.objects:
    if other_obj != obj:
        // İletişim
        distance = ((obj.x - other_obj.x)**2 + (obj.y - other_obj.y)**2)**0.5
        if distance < 50:
            // Çarpışma vb.
            pass
```
