# PyGamer Framework Documentation

Pygame tabanlı 2D oyun yapma framework'ü. JSON + assetler ile oyun geliştirme.

## Proje Yapısı

```
pygamer/
├── pygaminal/                     # Core engine
│   ├── __init__.py               # run_app() fonksiyonu
│   ├── app.py                    # Singleton: Ana oyun döngüsü
│   ├── scene.py                  # Sahne yönetimi
│   ├── object.py                 # Entity-Component System
│   ├── component.py              # Base Component
│   ├── script_component.py       # Universal component loader
│   ├── components/               # Built-in component script'leri
│   │   ├── Image.py              # Sprite çizim
│   │   ├── Animation.py          # Animasyon çizim
│   │   ├── YSort.py              # Y eksenine göre depth sorting
│   │   ├── Hitbox.py             # Çarpışma kutuları
│   │   ├── Movability.py         # Hareket + collision
│   │   ├── BackgroundMusic.py    # Arka plan müziği
│   │   └── SoundEffect.py        # Ses efektleri
│   ├── screen.py                 # Singleton: Pygame Surface yönetimi
│   ├── input_manager.py          # Singleton: Input handling (keyboard, mouse, joystick)
│   ├── audio_manager.py          # Singleton: Audio yönetimi
│   └── util.py                   # Yardımcı fonksiyonlar
└── sample-game/                  # Örnek oyun
    ├── scene_data.json           # Sahne tanımı
    ├── main.py                   # Entry point
    ├── PlayerMovementScript.py   # Custom script
    ├── images/                   # Assetler (PNG)
    └── sounds/                   # Audio dosyaları
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
Input yönetimi - Keyboard, Mouse, Joystick desteği.

```python
from pygaminal import InputManager
import pygame

im = InputManager()
im.update()  # Frame başı çağrılır (otomatik)

# Klavye
if im.is_pressed(pygame.K_w):  # Basılı mı
if im.is_just_pressed(pygame.K_SPACE):  # Just basıldı mı
if im.is_released(pygame.K_a):  # Bırakıldı mı

# Mouse
mx, my = im.get_mouse_position()
if im.is_mouse_pressed(1):  # Sol tık basılı
if im.is_mouse_just_pressed(3):  # Sağ tık just basıldı

# Joystick/Gamepad
if im.is_joystick_connected(0):
    axis_x = im.get_axis(0, 0)  # Sol stick X
    axis_y = im.get_axis(1, 0)  # Sol stick Y
    if im.get_button_pressed(0, 0):  # A button
        print("A pressed")
```

**Joystick Metotları:**
- `get_joystick_count()` - Bağlı joystick sayısı
- `is_joystick_connected(joystick_id)` - Bağlı mı?
- `get_joystick_name(joystick_id)` - Joystick adı
- `get_axis(axis_index, joystick_id)` - Axis değeri (-1.0 ile 1.0)
- `get_button_pressed(button_index, joystick_id)` - Buton basılı mı?
- `get_button_just_pressed(button_index, joystick_id)` - Buton just basıldı mı?
- `get_hat(hat_index, joystick_id)` - D-pad değeri

**Axis Index'leri (Xbox controller):**
- 0: Sol stick X
- 1: Sol stick Y
- 2: Sağ stick X
- 3: Sağ stick Y

**Button Index'leri (Xbox controller):**
- 0: A, 1: B, 2: X, 3: Y
- 4: Left Bumper, 5: Right Bumper
- 6: Back, 7: Start
- 8: Left Stick, 9: Right Stick

### AudioManager (Singleton)
Ses ve müzik yönetimi.

```python
from pygaminal import AudioManager

audio = AudioManager()

# Müzik kontrolü
audio.play_music("bgm.mp3", loop=True, fade_in=2.0, volume=0.7)
audio.stop_music(fade_out=1.0)
audio.pause_music()
audio.resume_music()
audio.is_music_playing()

# Ses seviyesi
audio.set_music_volume(0.5)
audio.set_sfx_volume(0.8)
```

### Scene
Objeleri tutan konteyner. **Performans için dict-based storage.**

```python
from pygaminal import Scene

scene = Scene()
scene.add_object(obj)  # Obje ekle (next frame'de aktif)
scene.update()  # Tüm objeleri update et
scene.draw()  # Tüm objeleri depth'e göre çiz
```

**Storage:**
- `scene.objects = {name: Object}` - Dict storage, O(1) lookup
- `scene._tags = {tag: [Object]}` - Tag index, O(1) lookup

**Property'ler:**
- `width`, `height` - Sahne boyutu
- `background_color` - Hex color string
- `background_image` - Dosya yolu

**Metodlar:**
- `add_object(obj)` - Obje ekle (next frame'de aktif olur)
- `remove_object(obj)` - Obje sil (next frame'de silinir)
- `get_object(name)` - İsmi verilen objeyi al - **O(1)**
- `get_objects_by_tag(tag)` - Tag'e göre tüm objeleri al - **O(1)**
- `get_all_objects()` - Tüm objeleri al

### Object
Entity-Component mimarisi. **Her obje unique isme sahiptir.**

```python
from pygaminal import Object

obj = Object(x, y, name="player", tags=["hero", "main"], depth=0)
obj.kill()  # Objeyi yok et (next frame'de silinir)
```

**Property'ler:**
- `name` - Unique isim (auto-generated veya explicit)
- `tags` - Tag set'i (set of strings)
- `x`, `y` - Pozisyon
- `depth` - Çizim derinliği (düşük = arkada, yüksek = önde)
- `dead` - Öldü mü?

**Metodlar:**
- `add_tag(tag)` - Tag ekle
- `remove_tag(tag)` - Tag sil
- `has_tag(tag)` - Tag kontrolü
- `kill()` - Next frame'de sil
- `add_component(component, explicit_name=None)` - Component ekle
- `get_component(name)` - Component al
- `get_components(file_name)` - Aynı türdeki tüm component'leri al

## Objeleri Yönetme

### Depth Sistemi
Objeler `depth` değerine göre çizilir:

```python
# Zemin (arkada)
floor = Object(100, 100, depth=-10)

// Duvarlar
wall = Object(100, 100, depth=0)

// Karakterler (önde)
player = Object(100, 100, depth=10)

// UI (en üstte)
ui = Object(100, 100, depth=100)
```

JSON'da:
```json
{
  "x": 100,
  "y": 100,
  "depth": 10,
  "name": "player",
  ...
}
```

### Name Sistemi
Her objenin unique bir ismi vardır:

```python
# Explicit name
obj = Object(100, 100, name="player")

# Auto-generated name
obj = Object(100, 100)  # name = "object_0"
obj = Object(200, 200)  # name = "object_1"

# Name conflicts → auto-numbering
obj1 = Object(100, 100, name="box")
obj2 = Object(200, 200, name="box")  # → "box_2"
obj3 = Object(300, 300, name="box")  # → "box_3"
```

### Tag Sistemi
Objeleri gruplamak için tags kullanın:

```python
# Create with tags
player = Object(100, 100, name="player", tags=["hero", "controllable"])
enemy = Object(200, 200, tags=["enemy", "flying"])

# Add/remove tags
enemy.add_tag("poisoned")
enemy.remove_tag("flying")

# Check tag (immediate - works same-frame)
if enemy.has_tag("poisoned"):
    take_damage()
```

### Objeleri Erişme

**By Name - Tek obje:**
```python
player = scene.get_object("player")
player.x += 100
```

**By Tag - Liste:**
```python
# Tüm düşmanları al
enemies = scene.get_objects_by_tag("enemy")
for enemy in enemies:
    enemy.x -= 50

# Tüm mermileri al
bullets = scene.get_objects_by_tag("bullet")
for bullet in bullets:
    bullet.x += 200 * app.dt
```

### Runtime Objeler Oluşturma

**Bullet spawn:**
```python
# Script'te
def shoot(self, obj):
    bullet = Object(obj.x, obj.y, tags=["bullet", "player_owned"])
    scene.add_object(bullet)
    # Next frame'de sahnede aktif olur
```

**Particle effect:**
```python
def create_explosion(self, x, y):
    particle = Object(x, y, tags=["effect", "explosion"])
    scene.add_object(particle)
```

## Component Sistemi

### Component Naming Convention
Component isimlerinde **"Component" suffix'i yoktur**:

```json
{"file": "@Image", "args": [...]}        // ✅ Doğru
{"file": "@Animation", "args": [...]}    // ✅ Doğru
{"file": "@YSort", "args": []}           // ✅ Doğru

{"file": "@ImageComponent", ...}        // ❌ Yanlış (eski)
```

### Built-in Component'ler

#### Image
Tek frame sprite çizim.

```json
{
  "file": "@Image",
  "args": ["player.png", "center", "center"]
}
```

**Args:**
1. `image_or_path` - Image objesi veya dosya yolu
2. `pivot_x` - "center", "end", veya pixel değeri
3. `pivot_y` - "center", "end", veya pixel değeri

#### Animation
Animasyon çizim.

```json
{
  "file": "@Animation",
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

#### YSort
Otomatik depth sorting (y pozisyonuna göre).

```json
{
  "file": "@YSort",
  "args": []
}
```

#### Hitbox
Çarpışma kutuları tanımlama.

```json
{
  "file": "@Hitbox",
  "args": [[-16, -16, 32, 32]]
}
```

**Args:**
- `hitboxes` - Tek hitbox: `[offset_x, offset_y, width, height]`
             - Çoklu hitbox: `[[...], [...]]`
             - Dict: `{"body": [...], "attack": [...]}`

#### Movability
Hareket + collision detection.

```json
{
  "file": "@Movability",
  "args": [200, ["collidable", "wall"]]
}
```

**Args:**
1. `speed` - Hareket hızı (pixels/second)
2. `collidables` - Çarpışacağı tag listesi

**Metodlar:**
- `move_x(obj, dx)` - X ekseninde hareket (collision kontrolü ile)
- `move_y(obj, dy)` - Y ekseninde hareket (collision kontrolü ile)

#### BackgroundMusic
Arka plan müziği çalma.

```json
{
  "file": "@BackgroundMusic",
  "args": ["music/bgm.mp3", true, 2.0, 0.6]
}
```

**Args:**
1. `music_file` - Müzik dosyası (mp3, ogg, vb.)
2. `loop` - Döngü çalsın mı? (true/false)
3. `fade_in` - Fade-in süresi (saniye)
4. `volume` - Ses seviyesi (0.0 - 1.0)

**Metodlar:**
- `play()` - Çal
- `stop(fade_out)` - Durdur
- `pause()` - Pause
- `resume()` - Resume
- `set_volume(volume)` - Ses seviyesi

#### SoundEffect
Kısa ses efektleri çalma.

```json
{
  "file": "@SoundEffect",
  "args": ["footstep.wav", 1.0, false, false]
}
```

**Args:**
1. `sound_path` - Ses dosyası (wav, ogg)
2. `volume` - Ses seviyesi (0.0 - 1.0)
3. `auto_play` - Otomatik çal
4. `loop` - Döngü çal

**Metodlar:**
- `play(volume)` - Çal
- `stop()` - Durdur
- `pause()` - Pause
- `resume()` - Resume
- `set_volume(volume)` - Ses seviyesi
- `is_playing()` - Çalıyor mu?

### User-Defined Component'ler
Kullanıcının yazdığı script'ler. Dosya adı ile kullanılır:

```json
{"file": "PlayerMovementScript", "args": [200]}
{"file": "EnemyAI", "args": []}
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
        app = App()
        obj.x += 100 * app.dt

    def draw(self, obj):
        # Opsiyonel: Custom drawing
        pass
```

## Collision Sistemi

### Hitbox Kullanımı

```json
{
  "file": "@Hitbox",
  "args": [[-16, -16, 32, 32]]
}
```

### Movability ile Collision-Aware Hareket

```python
# Script'te
movability = obj.get_component("Movability")

# X hareketi (collision kontrolü ile)
movability.move_x(obj, 100 * app.dt)

# Y hareketi (collision kontrolü ile)
movability.move_y(obj, 100 * app.dt)
```

**Collision Kontrolü:**
- Movability, `collidables` listesindeki tag'lere sahip objelerle çarpışır
- Çarpışma varsa hareketi engeller
- Multi-step movement (max 10px) - tunneling önler

### Collision Detection

```python
from pygaminal.util import check_collision_by_tags

# İki obje arasında collision
if check_collision_by_tags(obj1, obj2, ["body"], ["body"]):
    print("Collision!")
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
   - `@` ile başlarsa → Built-in component (`@Image`)
   - `@` yoksa → User script (`MovementScript`)

2. **`name`** - Opsiyonel
   - Verilirse → Bu isimle eklenir
   - Verilmezse → Otomatik isim (`Image`, `Image2`, ...)

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
      "name": "player",
      "tags": ["hero", "main"],
      "depth": 10,
      "components": [
        {
          "file": "@Hitbox",
          "args": [[-16, -16, 32, 32]]
        },
        {
          "file": "@Movability",
          "args": [200, ["collidable"]]
        },
        {
          "file": "@Image",
          "name": "body",
          "args": ["images/player.png", "center", "center"]
        },
        {
          "file": "PlayerController",
          "args": [200]
        }
      ]
    },
    {
      "x": 0,
      "y": 0,
      "name": "bg_music",
      "components": [
        {
          "file": "@BackgroundMusic",
          "args": ["music/bgm.mp3", true, 2.0, 0.6]
        }
      ]
    }
  ]
}
```

## Script Yazma

### Script Template

```python
import pygame
from pygaminal import *

class MyScript:
    def __init__(self, arg1, arg2=None):
        # Constructor, JSON args'dan değer alır
        self.value = arg1

    def update(self, obj):
        # Her frame çağrılır
        app = App()
        scene = app.get_current_scene()
        im = InputManager()
        audio = AudioManager()

        # Input
        if im.is_pressed(pygame.K_SPACE):
            # Aksiyon
            pass

        # Hareket (Movability ile)
        movability = obj.get_component("Movability")
        if movability:
            movability.move_x(obj, 100 * app.dt)

        # Obje yaratma
        bullet = Object(obj.x, obj.y, tags=["bullet"])
        scene.add_object(bullet)

        # Obje yok etme
        if obj.x > 800:
            obj.kill()

        # Objelere erişim
        player = scene.get_object("player")
        enemies = scene.get_objects_by_tag("enemy")

    def draw(self, obj):
        # Opsiyonel: Custom drawing
        pass
```

### Global Nesneler
Scriptlerde her zaman erişilebilir:
- `App()` - Singleton app instance
- `InputManager()` - Singleton input manager
- `AudioManager()` - Singleton audio manager
- `Screen()` - Singleton screen
- `app.get_current_scene()` - Aktif sahne

## Örnek Script'ler

### Player Movement (Keyboard)

```python
import pygame
from pygaminal import *

class PlayerMovementScript:
    def __init__(self, speed=200):
        self.speed = speed

    def update(self, obj):
        app = App()
        im = InputManager()

        # Input direction
        dx = im.is_pressed(pygame.K_d) - im.is_pressed(pygame.K_a)
        dy = im.is_pressed(pygame.K_s) - im.is_pressed(pygame.K_w)

        # Movability ile collision-aware hareket
        movability = obj.get_component("Movability")
        if movability:
            move_distance = self.speed * app.dt
            if dx != 0:
                movability.move_x(obj, dx * move_distance)
            if dy != 0:
                movability.move_y(obj, dy * move_distance)

    def draw(self, obj):
        pass
```

### Player Movement (Gamepad)

```python
from pygaminal import *

class GamepadMovementScript:
    def __init__(self, speed=200, joystick_id=0, deadzone=0.15):
        self.speed = speed
        self.joystick_id = joystick_id
        self.deadzone = deadzone

    def update(self, obj):
        app = App()
        im = InputManager()

        if not im.is_joystick_connected(self.joystick_id):
            return

        # Left stick values
        axis_x = im.get_axis(0, self.joystick_id)
        axis_y = im.get_axis(1, self.joystick_id)

        # Apply deadzone
        if abs(axis_x) < self.deadzone:
            axis_x = 0
        if abs(axis_y) < self.deadzone:
            axis_y = 0

        # Move
        movability = obj.get_component("Movability")
        if movability:
            move_distance = self.speed * app.dt
            if axis_x != 0:
                movability.move_x(obj, axis_x * move_distance)
            if axis_y != 0:
                movability.move_y(obj, axis_y * move_distance)

    def draw(self, obj):
        pass
```

### Bullet Shooting

```python
import pygame
from pygaminal import *

class ShootingScript:
    def __init__(self, cooldown=0.5, bullet_speed=300):
        self.cooldown = cooldown
        self.bullet_speed = bullet_speed
        self.last_shot = 0

    def update(self, obj):
        app = App()
        scene = app.get_current_scene()
        im = InputManager()

        # Cooldown kontrolü
        if app.now - self.last_shot < self.cooldown:
            return

        # Ateş et
        if im.is_pressed(pygame.K_SPACE):
            bullet = Object(obj.x, obj.y, tags=["bullet"])
            scene.add_object(bullet)
            self.last_shot = app.now

            # Sound effect
            sound = obj.get_component("SoundEffect")
            if sound:
                sound.play()

    def draw(self, obj):
        pass
```

### Bullet Movement

```python
from pygaminal import *

class BulletScript:
    def __init__(self, speed=300, direction_x=1, direction_y=0):
        self.speed = speed
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update(self, obj):
        app = App()
        scene = app.get_current_scene()

        # Hareket
        obj.x += self.direction_x * self.speed * app.dt
        obj.y += self.direction_y * self.speed * app.dt

        # Ekran dışına çıktı mı?
        if obj.x > scene.width or obj.x < 0:
            obj.kill()

        # Çarpışma kontrolü
        enemies = scene.get_objects_by_tag("enemy")
        for enemy in enemies:
            # Check collision (hitbox required)
            from pygaminal.util import check_collision_by_tags
            if check_collision_by_tags(obj, enemy, ["body"], ["body"]):
                enemy.kill()
                obj.kill()
                break

    def draw(self, obj):
        pass
```

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
3. **Depth Sorting**: `obj.depth` kullan, scene otomatik sıralar
4. **Collision**: Movability component'i kullan, manuel yapma
5. **Cleanup**: Biten objeleri `obj.kill()` ile yok et
6. **Cooldowns**: `app.now` kullanarak rate limiting yap
7. **Object Names**: Önemli objelere explicit name ver (player, boss1)
8. **Tags**: Gruplar için kullan (enemy, bullet, pickup)
9. **Performance**: `get_objects_by_tag()` O(1)'dir, bolca kullanın
10. **Component Naming**: Önemli component'lere explicit name ver

## Performans Notları

### Objeler
- `get_object(name)` → **O(1)** dict lookup
- `get_objects_by_tag(tag)` → **O(1)** dict lookup
- `get_all_objects()` → **O(n)**

### Component'ler
- `get_component(name)` → **O(1)** dict lookup
- `get_components(file_name)` → **O(n)** (nadır kullanılır)

### Update Loop
- Her frame bir kere `_apply_pending_updates()` → **O(n × tags)**
- Depth sorting → **O(n log n)**

## Audio Kullanım

### Background Music
Obje üzerinden çalın:

```json
{
  "name": "music_player",
  "components": [
    {
      "file": "@BackgroundMusic",
      "args": ["music/bgm.mp3", true, 2.0, 0.6]
    }
  ]
}
```

Kod ile kontrol:
```python
bg_music = obj.get_component("BackgroundMusic")
bg_music.stop(fade_out=3.0)
bg_music.play()
```

### Sound Effects
Objeye attach edilir:

```json
{
  "name": "player",
  "components": [
    {
      "file": "@SoundEffect",
      "args": ["footstep.wav", 0.8, false, false]
    }
  ]
}
```

Script'te tetikle:
```python
sound = obj.get_component("SoundEffect")
if dx != 0 and not sound.is_playing():
    sound.play()
```

### Global Audio Kontrol
```python
audio = AudioManager()

# Music volume
audio.set_music_volume(0.5)

# SFX volume
audio.set_sfx_volume(0.8)

# Müzik kontrolü
audio.pause_music()
audio.resume_music()
audio.stop_music(fade_out=2.0)
```
