# Game Engine Mimarisi - Dil Bağımsız Tasarım Referansı

## Sürüm Bilgisi

- **Sürüm:** 1.0.0
- **Kaynak Proje:** PyGamer (Gaminal) v0.1.4
- **Tarih:** 2026-03-20
- **Amaç:** Bu döküman, Entity-Component-System (ECS) mimarisine dayalı, 2D oyun geliştirme motorlarının kavramsal tasarımını sunar. Dil bağımsızdır ve herhangi bir programlama dilinde uygulanabilir.

---

## İçindekiler

1. [Genel Bakış](#1-genel-bakış)
2. [Temel Tasarım Prensipleri](#2-temel-tasarı-prensipleri)
3. [Sistem Mimarisi](#3-sistem-mimarisi)
4. [Veri Formatları](#4-veri-formatları)
5. [Nesne Türleri ve Sorumlulukları](#5-nesne-türleri-ve-sorumlulukları)
6. [Etkileşim Desenleri](#6-etkileşim-desenleri)
7. [Rendering Pipeline](#7-rendering-pipeline)
8. [Input Sistemi](#8-input-sistemi)
9. [Audio Sistemi](#9-audio-sistemi)
10. [Collision Sistemi](#10-collision-sistemi)
11. [Performans Optimizasyonları](#11-performans-optimizasyonları)
12. [UML Diyagramları](#12-uml-diyagramları)
13. [Uygulama Kontrol Listesi](#13-uygulama-kontrol-listesi)

---

## 1. Gen Bakış

### 1.1 Temel Kavram

Bu motor, **Entity-Component-System (ECS)** mimarisi kullanır. Bu mimaride:

- **Entity (Varlık):** Sadece veri taşıyan konteyner (ID, pozisyon, etiketler)
- **Component (Bileşen):** Tek bir davranışı temsil eden modül
- **System (Sistem):** Entity'leri ve Component'leri koordine eden döngü

### 1.2 Özellikler

| Özellik | Açıklama |
|---------|----------|
| **2D Rendering** | Sprite tabanlı 2D grafik |
| **ECS Mimarisi** | Modüler ve yeniden kullanılabilir bileşenler |
| **JSON-Driven** | Declarative sahne tanımları |
| **Collision Detection** | AABB (Axis-Aligned Bounding Box) çarpışma |
| **Input Abstraction** | Klavye, fare, gamepad desteği |
| **Audio Management** | Müzik ve SFX çalma |
| **Depth Sorting** | Z-sıralaması ile pseudo-3D derinlik |
| **Object Pooling**** | Opsiyonel nesne havuzu (eklenti) |
| **Hot-Reloading**** | Opsiyonel asset yeniden yükleme (eklenti) |

### 1.3 Teknik Hedefler

```
┌────────────────────────────────────────────────────────────┐
│                     TEKNİK HEDEFLER                         │
├────────────────────────────────────────────────────────────┤
│ Kolay öğrenım eğrisi                                        │
│ Minimum boilerplate kod                                     │
│ Hızlı iterasyon (JSON ile)                                  │
│ Genişletilebilir component sistemi                          │
│ Platform bağımsız çalışma                                   │
│ Yüksek performans (60 FPS hedefi)                          │
└────────────────────────────────────────────────────────────┘
```

---

## 2. Temel Tasarım Prensipleri

### 2.1 Singleton Pattern

**Amaç:** Global state yönetimi için tek örnek

**Uygulama Alanları:**
- Application (Ana döngü)
- Screen/Display (Rendering surface)
- InputManager (Input state)
- AudioManager (Audio state)

**Implementasyon Şablonu:**
```pseudocode
class Singleton:
    _instance = null
    _lock = null

    function getInstance():
        if _instance is null:
            _lock.acquire()
            if _instance is null:
                _instance = new Singleton()
            _lock.release()
        return _instance
```

**Thread Safety:**
- Çok thread'li ortamlarda lock kullanın
- Double-checked locking pattern'i uygulayın

### 2.2 Composition Over Inheritance

**Amaç:** Kalıtım yerine bileşim kullanarak esneklik sağla

**Kötü Örnek (Kalıtım):**
```
GameObject → MovableGameObject → FlyingMovableGameObject
         → StaticGameObject      → DestructibleStaticGameObject
```

**İyi Örnek (Bileşim):**
```
GameObject + [MovementComponent, FlightComponent, HealthComponent]
GameObject + [RenderComponent, CollisionComponent]
```

**Avantajları:**
- Runtime'da davranış ekle/çıkar
- Kod yeniden kullanımı
- Test edilebilirlik
- Bakım kolaylığı

### 2.3 Declarative over Imperative

**Amaç:** Veri ve mantığı ayır

**JSON (Declarative):**
```json
{
  "position": {"x": 100, "y": 200},
  "components": [
    {"type": "Render", "asset": "player.png"},
    {"type": "Movement", "speed": 200}
  ]
}
```

**Kod (Imperative):**
```python
# Sadece davranış tanımla
class MovementComponent:
    def update(self, entity):
        # Hareket mantığı
```

**Avantajları:**
- Görsel editör desteği
- Non-programmer dostu
- Versiyon kontrolü kolay
- Asset pipeline entegrasyonu

### 2.4 Deferred Updates Pattern

**Amaç:** İterasyon sırasında koleksiyon değişikliklerini önle

**Problem:**
```
for entity in scene.entities:
    if entity.should_die:
        scene.remove(entity)  # ❌ Collection modified error
```

**Çözüm:**
```
for entity in scene.entities:
    if entity.should_die:
        scene.pending_removals.add(entity)

# Frame sonunda uygula
scene.apply_pending_updates()
```

**Kuyruk Türleri:**
- `pending_additions`: Yeni entity'ler
- `pending_removals`: Silinecek entity'ler
- `pending_tag_changes`: Etiket değişiklikleri

---

## 3. Sistem Mimarisi

### 3.1 Genel Yapı

```
┌─────────────────────────────────────────────────────────────────┐
│                         APPLICATION                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    MAIN GAME LOOP                           │ │
│  │                                                            │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐          │ │
│  │  │   INPUT    │→ │   UPDATE   │→ │   RENDER   │          │ │
│  │  │  MANAGER   │  │   PHASE    │  │   PHASE    │  Repeat  │ │
│  │  └────────────┘  └────────────┘  └────────────┘          │ │
│  │                                                      ↓      │ │
│  │                                                ┌─────────┐  │ │
│  │                                                │  SYNC   │  │ │
│  │                                                └─────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  scenes: Map<String, Scene>                                     │
│  current_scene: Scene                                           │
│  delta_time: Float                                              │
│  target_fps: Integer                                            │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Core Subsystems

#### 3.2.1 Application (Main Loop)

**Sorumluluklar:**
- Ana oyun döngüsü
- Sahne yönetimi
- FPS kontrolü
- Delta time hesaplama
- Alt sistem koordinasyonu

**State:**
```
- width: Integer              // Ekran genişliği
- height: Integer             // Ekran yüksekliği
- title: String               // Pencere başlığı
- running: Boolean            // Döngü durumu
- target_fps: Integer         (60)
- current_time: Float         // Saniye cinsinden
- delta_time: Float           // Frame süresi (saniye)
- clock: Clock                // Zamanlayıcı
- scenes: Map<String, Scene>  // Sahne havuzu
- current_scene_name: String  // Aktif sahne
```

**Metotlar:**
```
+ init(width, height, title)
+ add_scene(name, scene)
+ set_scene(name)
+ get_current_scene() -> Scene
+ stop()
+ run()  // Ana döngüyü başlat
```

**Game Loop Pseudocode:**
```
function run():
    while running:
        # 1. Input Phase
        input_manager.update()
        process_events()

        # 2. Update Phase
        scene = get_current_scene()
        scene.update(delta_time)

        # 3. Render Phase
        screen.clear()
        scene.draw()
        screen.refresh()

        # 4. Sync Phase
        clock.tick(target_fps)
        delta_time = clock.get_delta()
```

#### 3.2.2 Scene Manager

**Sorumluluklar:**
- Entity konteyneri
- O(1) entity lookup
- O(1) tag lookup
- Depth sorting

**State:**
```
- objects: Map<String, Entity>           // Name → Entity
- tags: Map<String, List<Entity>>        // Tag → [Entities]
- pending_additions: List<Entity>        // Eklenecekler
- pending_removals: List<Entity>         // Silinecekler
- pending_tag_changes: List<Change>      // Tag değişiklikleri
- width: Integer
- height: Integer
- background_color: Color
- background_image: Image
```

**Metotlar:**
```
+ add_object(entity)
+ remove_object(entity)
+ get_object(name) -> Entity
+ get_objects_by_tag(tag) -> List<Entity>
+ get_all_objects() -> List<Entity>
+ update()
+ draw()
+ _apply_pending_updates()
```

**Data Structures:**

```pseudocode
# Hash tablo based lookup (O(1))
objects: {
    "player": Entity(100, 200),
    "enemy_1": Entity(300, 400),
    "wall_5": Entity(500, 100)
}

# Tag index (O(1) lookup)
tags: {
    "enemy": [enemy_1, enemy_2, enemy_3],
    "collidable": [wall_1, wall_2, player],
    "bullet": [bullet_1, bullet_2, bullet_3]
}

# Pending updates queue
pending_additions: [new_entity_1, new_entity_2]
pending_removals: [dead_entity_1, dead_entity_2]
pending_tag_changes: [
    {entity: e1, action: ADD, tag: "dead"},
    {entity: e2, action: REMOVE, tag: "active"}
]
```

**Update Phase:**
```pseudocode
function update():
    # 1. Update all entities
    for entity in objects.values():
        entity.update()

    # 2. Apply pending changes
    _apply_pending_updates()
```

**Draw Phase:**
```pseudocode
function draw():
    # 1. Sort by depth
    sorted_entities = sort_by_depth(objects.values())

    # 2. Draw in order
    for entity in sorted_entities:
        entity.draw()
```

**Apply Pending Updates:**
```pseudocode
function _apply_pending_updates():
    # 1. Remove dead entities
    for entity in pending_removals:
        # Remove from objects map
        objects.remove(entity.name)
        # Remove from all tag indices
        for tag in entity.tags:
            tags[tag].remove(entity)

    # 2. Add new entities
    for entity in pending_additions:
        objects[entity.name] = entity
        for tag in entity.tags:
            tags[tag].add(entity)

    # 3. Apply tag changes
    for change in pending_tag_changes:
        if change.action == ADD:
            tags[change.tag].add(change.entity)
        elif change.action == REMOVE:
            tags[change.tag].remove(change.entity)

    # 4. Clear queues
    pending_additions.clear()
    pending_removals.clear()
    pending_tag_changes.clear()
```

#### 3.2.3 Entity (Object)

**Sorumluluklar:**
- Pozisyon ve metadata taşıma
- Component konteyneri
- Lifecycle yönetimi

**State:**
```
- name: String                    // Unique identifier
- x: Float                        // Position X
- y: Float                        // Position Y
- depth: Integer                  // Render depth (z-index)
- tags: Set<String>               // Etiketler
- components: Map<String, Component>
- dead: Boolean                   // Marked for deletion
- pending_tag_adds: Set<String>
- pending_tag_removes: Set<String>
```

**Metotlar:**
```
+ add_tag(tag)
+ remove_tag(tag)
+ has_tag(tag) -> Boolean
+ kill()
+ add_component(component, name)
+ get_component(name) -> Component
+ get_components(type) -> List<Component>
+ update()
+ draw()
```

**Name Generation:**
```pseudocode
function generate_name(base_name):
    if objects[base_name] is null:
        return base_name

    # Auto-generate suffix
    counter = 2
    while true:
        new_name = base_name + "_" + counter
        if objects[new_name] is null:
            return new_name
        counter += 1

# Examples:
# "box" → "box"
# "box" → "box_2"
# "box" → "box_3"
```

**Component Management:**
```pseudocode
function add_component(component, explicit_name):
    if explicit_name is not null:
        name = explicit_name
    else:
        # Auto-generate based on type
        base_name = component.type_name
        name = _generate_component_name(base_name)

    components[name] = component

function _generate_component_name(base_name):
    counter = 1
    while true:
        if counter == 1:
            name = base_name
        else:
            name = base_name + counter

        if components[name] is null:
            return name
        counter += 1
```

**Update Phase:**
```pseudocode
function update():
    if dead:
        return

    for component in components.values():
        component.update(this)
```

**Draw Phase:**
```pseudocode
function draw():
    if dead:
        return

    for component in components.values():
        component.draw(this)
```

#### 3.2.4 Component System

**Sorumluluklar:**
- Tekil davranışları kapsüle et
- Entity state'ini oku/modify et
- Opsiyonel rendering

**Interface:**
```pseudocode
interface Component:
    function init(args)           // Constructor
    function update(entity)       // Frame update
    function draw(entity)         // Render (optional)
```

**Built-in Component Types:**

| Component | Açıklama | Durum |
|-----------|----------|-------|
| **Image** | Statik sprite render | Zorunlu |
| **Animation** | Sprite sheet animasyonu | Opsiyonel |
| **Hitbox** | Collision box tanımı | Opsiyonel |
| **Movability** | Collision-aware hareket | Opsiyonel |
| **YSort** | Y-based depth sorting | Opsiyonel |
| **BackgroundMusic** | Müzik çalma | Opsiyonel |
| **SoundEffect** | SFX çalma | Opsiyonel |

**Component Loader:**
```pseudocode
class ComponentLoader:
    function load(type_name, args):
        if type_name starts_with "@":
            # Built-in component
            component_type = BUILTIN_PREFIX + type_name[1:]
        else:
            # User script
            component_type = load_script(type_name)

        return create_instance(component_type, args)
```

### 3.3 Rendering Subsystem

#### 3.3.1 Screen/Display

**Sorumluluklar:**
- Display surface yönetimi
- Clear/Draw/Flip işlemleri
- Background yönetimi

**State:**
```
- surface: DisplaySurface
- width: Integer
- height: Integer
- background_color: Color
- background_image: Image
```

**Metotlar:**
```
+ init(width, height)
+ set_background_color(color)
+ set_background_image(path)
+ clear()
+ blit(image, x, y)
+ refresh()
```

**Rendering Modes:**
```
Mode 1: Color Background
- clear(): surface.fill(background_color)

Mode 2: Image Background
- clear(): Draw scaled background_image

Mode 3: None (Transparent)
- clear(): Do nothing or fill with (0,0,0,0)
```

#### 3.3.2 Depth Sorting

**Amaç:** Doğru render sırası (arkadan öne)

**Algoritma:**
```pseudocode
function sort_by_depth(entities):
    return entities.sort((a, b) => a.depth - b.depth)

# Lower depth = drawn first (background)
# Higher depth = drawn last (foreground)
```

**Tipik Depth Değerleri:**
```
-100 to -10:  Background layer (sky, mountains)
-10 to 0:     Ground tiles
0 to 100:     Objects on ground
100:          Characters
100+:         UI overlay
```

**YSort Component:**
```pseudocode
function update(entity):
    entity.depth = entity.y
    # Lower Y = further away = drawn first
```

### 3.4 Input Subsystem

#### 3.4.1 Input Manager

**Sorumluluklar:**
- Input state takibi
- Event processing
- Multi-device destek

**State:**
```
# Keyboard
- pressed_keys: Set<KeyCode>
- just_pressed_keys: Set<KeyCode>
- released_keys: Set<KeyCode>

# Mouse
- mouse_x: Integer
- mouse_y: Integer
- pressed_mouse_buttons: Set<Button>
- just_pressed_mouse_buttons: Set<Button>
- released_mouse_buttons: Set<Button>

# Joystick/Gamepad
- joysticks: Map<Integer, Joystick>
- joystick_axes: Map<Integer, List<Float>>
- joystick_buttons: Map<Integer, Set<Button>>
- joystick_hats: Map<Integer, List<HatPosition>>
```

**Input States:**
```
┌─────────────────────────────────────────────────┐
│              INPUT STATE MACHINE                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  RELEASED ──(PRESS)──> PRESSED                  │
│     ▲                     │                     │
│     │                  (HOLD)                   │
│     │                     ▼                     │
│  RELEASED <──(RELEASE)── JUST_PRESSED           │
│                        │                       │
│                      (1 frame)                 │
│                        ▼                       │
│                     PRESSED                    │
└─────────────────────────────────────────────────┘
```

**Update Phase:**
```pseudocode
function update():
    # Clear frame-specific state
    just_pressed_keys.clear()
    released_keys.clear()
    just_pressed_mouse_buttons.clear()
    released_mouse_buttons.clear()

    # Process events
    for event in events:
        if event.type == KEY_DOWN:
            if event.key not in pressed_keys:
                just_pressed_keys.add(event.key)
            pressed_keys.add(event.key)

        elif event.type == KEY_UP:
            pressed_keys.remove(event.key)
            released_keys.add(event.key)

        elif event.type == MOUSE_MOVE:
            mouse_x = event.x
            mouse_y = event.y

        elif event.type == MOUSE_BUTTON_DOWN:
            if event.button not in pressed_mouse_buttons:
                just_pressed_mouse_buttons.add(event.button)
            pressed_mouse_buttons.add(event.button)

        elif event.type == MOUSE_BUTTON_UP:
            pressed_mouse_buttons.remove(event.button)
            released_mouse_buttons.add(event.button)

        # Joystick events...
```

**Query Metotları:**
```pseudocode
# Keyboard
function is_pressed(key) -> Boolean
function is_just_pressed(key) -> Boolean
function is_released(key) -> Boolean

# Mouse
function get_mouse_position() -> (x, y)
function is_mouse_pressed(button) -> Boolean
function is_mouse_just_pressed(button) -> Boolean
function is_mouse_released(button) -> Boolean

# Joystick
function get_joystick_count() -> Integer
function is_joystick_connected(id) -> Boolean
function get_axis(axis_index, joystick_id) -> Float  // -1.0 to 1.0
function get_button_pressed(button_index, joystick_id) -> Boolean
function get_button_just_pressed(button_index, joystick_id) -> Boolean
function get_hat(hat_index, joystick_id) -> (x, y)  // D-pad
```

**Joystick Mapping (Standard Xbox Controller):**
```
Axes:
  0: Left stick X
  1: Left stick Y
  2: Right stick X
  3: Right stick Y

Buttons:
  0: A, 1: B, 2: X, 3: Y
  4: Left Bumper, 5: Right Bumper
  6: Back, 7: Start
  8: Left Stick, 9: Right Stick

Hats:
  0: D-pad (x: -1/0/1, y: -1/0/1)
```

### 3.5 Audio Subsystem

#### 3.5.1 Audio Manager

**Sorumluluklar:**
- Music playback (streaming)
- SFX playback (pre-loaded)
- Volume kontrolü
- Fade effects

**State:**
```
- music_volume: Float           (0.0 to 1.0)
- sfx_volume: Float             (0.0 to 1.0)
- current_music: String         // File path
- music_loop: Boolean
- music_fade_timer: Float
```

**Audio Types:**

| Type | Description | Channels | Format | Use Case |
|------|-------------|----------|--------|----------|
| **Music** | Streaming | 1 | MP3, OGG | Background music |
| **SFX** | Pre-loaded | 8-32 | WAV, OGG | Sound effects |

**Music API:**
```pseudocode
function play_music(file_path, loop=true, fade_in=0.0, volume=null)
function stop_music(fade_out=0.0)
function pause_music()
function resume_music()
function is_music_playing() -> Boolean
function set_music_volume(volume)  // 0.0 to 1.0
```

**SFX API:**
```pseudocode
class SoundEffect:
    function init(file_path, volume=1.0)
    function play(volume=null)
    function stop()
    function pause()
    function resume()
    function is_playing() -> Boolean
    function set_volume(volume)

# Global SFX volume
function set_sfx_volume(volume)
function get_sfx_volume() -> Float
```

**Volume Calculation:**
```
final_sfx_volume = sound_effect.base_volume * audio_manager.sfx_volume
```

---

## 4. Veri Formatları

### 4.1 Scene JSON Format

**Dosya Uzantısı:** `.json`

**Tam Yapı:**
```json
{
  "width": 800,
  "height": 600,
  "background_color": "#2a2a3a",
  "background_image": "assets/bg.png",
  "objects": [
    {
      "x": 400,
      "y": 300,
      "name": "player",
      "tags": ["hero", "controllable"],
      "depth": 10,
      "components": [
        {
          "file": "@Hitbox",
          "name": "body",
          "args": [[-16, -16, 32, 32]]
        },
        {
          "file": "@Image",
          "args": ["player.png", "center", "center"]
        }
      ]
    }
  ]
}
```

**Alan Açıklamaları:**

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `width` | Integer | Hayır | Sahne genişliği (pixel) |
| `height` | Integer | Hayır | Sahne yüksekliği (pixel) |
| `background_color` | String | Hayır | Hex color veya RGB |
| `background_image` | String | Hayır | Resim dosya yolu |
| `objects` | Array | Evet | Obje tanımları |

### 4.2 Entity JSON Format

**Format 1: Inline Definition:**
```json
{
  "x": 100.5,
  "y": 200.3,
  "name": "player",
  "tags": ["hero", "friendly"],
  "depth": 10,
  "components": [...]
}
```

**Format 2: External Reference:**
```json
{
  "file": "objects/player.obj",
  "x": 400,
  "y": 300
}
```

**Alan Açıklamaları:**

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `x` | Float | Evet | Pozisyon X |
| `y` | Float | Evet | Pozisyon Y |
| `name` | String | Hayır | Unique identifier |
| `tags` | Array<String> | Hayır | Etiket listesi |
| `depth` | Integer | Hayır | Render depth (default: 0) |
| `components` | Array | Hayır* | Component listesi |
| `file` | String | Hayır* | `.obj` dosya yolu |

*`components` veya `file`'den biri zorunlu

### 4.3 Component JSON Format

**Uniform Yapı:**
```json
{
  "file": "ComponentName",
  "name": "optional_unique_name",
  "args": [arg1, arg2, ...]
}
```

**Alan Açıklamaları:**

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `file` | String | Evet | Component tipi |
| `name` | String | Hayır | Unique component name |
| `args` | Array | Hayır | Constructor argümanları |

**Component Tip Konvansiyonları:**
```
@Prefix  → Built-in component
no prefix → User script

Örnekler:
"@Image"      → Built-in Image component
"@Animation"  → Built-in Animation component
"PlayerScript" → User script: PlayerScript.py
```

**Örnekler:**
```json
// Built-in - Image
{
  "file": "@Image",
  "args": ["player.png", "center", "center"]
}

// Built-in - Animation
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

// Built-in - Hitbox
{
  "file": "@Hitbox",
  "args": [[-16, -16, 32, 32]]
}

// User script
{
  "file": "PlayerMovementScript",
  "args": [200, true]
}
```

### 4.4 .obj File Format

**Amaç:** Yeniden kullanılabilir obje template'leri

**Dosya Uzantısı:** `.obj`

**Format:** Entity JSON (x ve y olmadan)

**Örnek - player.obj:**
```json
{
  "name": "player",
  "tags": ["hero", "controllable"],
  "depth": 10,
  "components": [
    {
      "file": "@Hitbox",
      "args": [[-16, -16, 32, 32]]
    },
    {
      "file": "@Movability",
      "args": [200, ["collidable", "wall"]]
    },
    {
      "file": "@Image",
      "args": ["images/player.png", "center", "center"]
    },
    {
      "file": "PlayerMovementScript",
      "args": [200]
    }
  ]
}
```

**Kullanım (scene_data.json):**
```json
{
  "file": "objects/player.obj",
  "x": 400,
  "y": 300
}
```

**Kurallar:**
- `.obj` dosyaları `x` ve `y` içeremez
- Scene referansı `file`, `x`, `y` içermeli
- Aynı `.obj` birden fazla kez kullanılabilir

### 4.5 Animation Data Format

**Sprite Sheet Tanımı:**
```json
{
  "file": "walk.png",
  "frame_width": 32,
  "frame_height": 32,
  "frames": [0, 1, 2, 3],
  "speed": 10,
  "loop": true
}
```

**Alan Açıklamaları:**

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `file` | String | Evet | Sprite sheet dosya yolu |
| `frame_width` | Integer | Evet | Çerçeve genişliği (pixel) |
| `frame_height` | Integer | Evet | Çerçeve yüksekliği (pixel) |
| `frames` | Array<Integer> | Hayır | Frame index'leri (default: all) |
| `speed` | Float | Hayır | Animasyon hızı çarpanı (default: 1.0) |
| `loop` | Boolean | Hayır | Döngü (default: true) |

**Frame Indexing:**
```
Sprite sheet (4x2 frames, each 32x32):
┌────┬────┬────┬────┐
│ 0  │ 1  │ 2  │ 3  │  Row 0
├────┼────┼────┼────┤
│ 4  │ 5  │ 6  │ 7  │  Row 1
└────┴────┴────┴────┘

"frames": [0, 1, 2, 3]  → Frames 0-3
"frames": null          → All frames (0-7)
```

### 4.6 Hitbox Data Format

**Formatlar:**

```json
// Single rect
{
  "file": "@Hitbox",
  "args": [[-16, -16, 32, 32]]
}

// Multiple rects
{
  "file": "@Hitbox",
  "args": [[-10, -10, 20, 20], [5, 5, 10, 10]]
}

// Named hitboxes (future)
{
  "file": "@Hitbox",
  "args": {
    "body": [-16, -16, 32, 32],
    "attack": [10, -5, 15, 15]
  }
}
```

**Rect Format:** `[offset_x, offset_y, width, height]`

- `offset_x`, `offset_y`: Entity merkezine göre offset
- `width`, `height`: Collision box boyutları

---

## 5. Nesne Türleri ve Sorumlulukları

### 5.1 Core Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    SINGLETON MANAGERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Application  │  │ InputManager │  │ AudioManager │     │
│  │  (Main Loop) │  │  (Input)     │  │  (Audio)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐                                          │
│  │    Screen    │                                          │
│  │  (Display)   │                                          │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ manages
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       SCENE MANAGER                         │
├─────────────────────────────────────────────────────────────┤
│  - Multiple scenes support                                  │
│  - Entity lifecycle management                              │
│  - Tag-based querying                                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ contains
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       ENTITY                                │
├─────────────────────────────────────────────────────────────┤
│  Properties:                                                │
│  - name, x, y, depth, tags                                  │
│  - components: Map<String, Component>                       │
│                                                             │
│  Responsibilities:                                          │
│  - Position management                                      │
│  - Component container                                      │
│  - Tag management                                           │
│  - Lifecycle control (kill)                                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ contains
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    COMPONENTS                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │   Image    │  │ Animation  │  │  Hitbox    │          │
│  │ (Render)   │  │ (Animate)  │  │(Collision) │          │
│  └────────────┘  └────────────┘  └────────────┘          │
│                                                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │Movability  │  │   YSort    │  │   Audio    │          │
│  │ (Movement) │  │ (Depth)    │  │ (Sound)    │          │
│  └────────────┘  └────────────┘  └────────────┘          │
│                                                             │
│  ┌─────────────────────────────────────┐                  │
│  │      User Scripts (Custom)           │                  │
│  │  - MovementScript                   │                  │
│  │  - AIScript                         │                  │
│  │  - HealthScript                     │                  │
│  └─────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Sorumluluk Matrisi

| Nesne | State Yönetimi | Logic | Rendering | Input | Audio | Collision |
|-------|----------------|-------|-----------|-------|-------|-----------|
| **Application** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Scene** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Entity** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Component** | ❌ | ✅ | ✅* | ✅* | ✅* | ✅* |
| **InputManager** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **AudioManager** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Screen** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

\* İsteğe bağlı (component tipine bağlı)

### 5.3 Data Flow

```
┌──────────────────────────────────────────────────────────┐
│                    DATA FLOW DIAGRAM                     │
└──────────────────────────────────────────────────────────┘

1. INITIALIZATION
   User Code → JSON Loader → Scene → Entities → Components

2. GAME LOOP (per frame)
   ┌────────────────────────────────────────────────────┐
   │                                                    │
   │  Input Events                                      │
   │       ↓                                            │
   │  InputManager.update() ──────────────────┐         │
   │                                          │         │
   │  Scene.update()                          │         │
   │       ↓                                  │         │
   │  For each entity:                        │         │
   │       ↓                                  │         │
   │      For each component:                 │         │
   │           ↓                              │         │
   │          component.update(entity)        │         │
   │           ↓                              │         │
   │          [Query InputManager] ───────────┘         │
   │           ↓                                          │
   │          [Modify entity state]                       │
   │                                                      │
   │  Scene._apply_pending_updates()                      │
   │       ↓                                              │
   │  [Add/remove entities, apply tag changes]            │
   │                                                      │
   │  Screen.clear()                                      │
   │       ↓                                              │
   │  Scene.draw()                                        │
   │       ↓                                              │
   │  [Sort entities by depth]                            │
   │       ↓                                              │
   │  For each entity (sorted):                           │
   │       ↓                                              │
   │      For each component:                             │
   │           ↓                                          │
   │          component.draw(entity)                      │
   │           ↓                                          │
   │          [Render to Screen]                          │
   │                                                      │
   │  Screen.refresh()                                    │
   │                                                      │
   └────────────────────────────────────────────────────┘
```

---

## 6. Etkileşim Desenleri

### 6.1 Component-Entity İletişimi

**Pattern:** Component, Entity'yi parametre olarak alır

```pseudocode
class MovementComponent:
    function update(entity):
        # Entity state'ini oku
        current_x = entity.x
        current_y = entity.y

        # State'i değiştir
        entity.x = current_x + speed * delta_time
        entity.y = current_y + speed * delta_time
```

**Avantajları:**
- Basit ve anlaşılır
- Component'ler state tutmaz
- Kolay test edilebilir

### 6.2 Component-Component İletişimi

**Pattern:** Entity üzerinden diğer component'lere erişim

```pseudocode
class AnimationControllerScript:
    function update(entity):
        # Diğer component'i al
        movement = entity.get_component("MovementComponent")
        animation = entity.get_component("AnimationComponent")

        # İletişim kur
        if movement.is_moving:
            animation.play("walk")
        else:
            animation.play("idle")
```

**Alternatif Pattern (Event-based):**
```pseudocode
class HealthComponent:
    function take_damage(amount):
        current_health -= amount

        # Event dispatch
        entity.dispatch_event("on_damage", amount)

class DamageFlashComponent:
    function on_damage(entity, amount):
        flash_animation.play()
```

### 6.3 Entity-Scene İletişimi

**Pattern:** Scene, entity lookup sağlar

```pseudocode
class EnemyAIScript:
    function update(entity):
        scene = Application.get_current_scene()

        # İsme göre bul
        player = scene.get_object("player")

        # Tag'e göre bul
        enemies = scene.get_objects_by_tag("enemy")

        # Tüm entity'leri al
        all_objects = scene.get_all_objects()
```

**Lookup Performansı:**
```
get_object(name):        O(1) - Hash lookup
get_objects_by_tag(tag): O(1) - Tag index lookup
get_all_objects():       O(n) - Full iteration
```

### 6.4 Singleton Erişim

**Pattern:** Global instance accessor

```pseudocode
# Herhangi bir component'ten
app = Application.getInstance()
scene = app.get_current_scene()

im = InputManager.getInstance()
if im.is_pressed(KEY_SPACE):
    jump()

audio = AudioManager.getInstance()
audio.play_music("bgm.mp3")
```

### 6.5 Cross-Scene Communication

**Pattern 1: Direct Access**
```pseudocode
# Scene switching
app = Application.getInstance()
app.set_scene("game_over")
```

**Pattern 2: Event Bus (Advanced)**
```pseudocode
# Event dispatch
EventBus.dispatch("player_died", {score: 100})

# Event listen (different scene)
EventBus.on("player_died", function(data):
    show_game_over(data.score)
)
```

**Pattern 3: Shared State**
```pseudocode
# Global state manager
GameState.set("high_score", 1000)

# Different scene
score = GameState.get("high_score")
```

---

## 7. Rendering Pipeline

### 7.1 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   RENDERING PIPELINE                        │
└─────────────────────────────────────────────────────────────┘

1. CLEAR PHASE
   Screen.clear()
   ├─ if background_color: surface.fill(background_color)
   └─ if background_image: draw scaled background_image

2. SORT PHASE
   Scene.draw()
   └─ entities = sort_by_depth(entities)

3. DRAW PHASE
   for entity in entities (depth-sorted):
       for component in entity.components:
           component.draw(entity)

4. PRESENT PHASE
   Screen.refresh()
   └─ display.flip()
```

### 7.2 Component Drawing Order

**Entity içindeki component sırası:**

```pseudocode
components = {
    "shadow": ShadowImageComponent,
    "body": AnimationComponent,
    "equipment": WeaponImageComponent,
    "effect": ParticleComponent
}

# Draw order: shadow → body → equipment → effect
```

**Depth hierarchy:**
```
Depth -100:     Background image
Depth -50:      Distant mountains
Depth -10:      Ground tiles
Depth 0-100:    Objects (YSort or manual)
Depth 100:      Characters
Depth 200:      Foreground objects
Depth 1000:     UI overlay
```

### 7.3 Render Batching (Optional Optimization)

**Amaç:** Draw call sayısını azalt

**Stratejiler:**

1. **Static Batching:**
   ```
   Aynı texture'dan tüm statik objeleri tek draw call'da render et
   ```

2. **Dynamic Batching:**
   ```
   Frame'de aynı texture'a sahip dynamic objeleri grupla
   ```

3. **Z-Order Batching:**
   ```
   Depth'e göre grupla, her depth için batch oluştur
   ```

---

## 8. Input Sistemi

### 8.1 Input State Machine

```
                    ┌──────────────┐
                    │   RELEASED   │
                    └──────┬───────┘
                           │
                         PRESS
                           │
                           ▼
                    ┌──────────────┐
                    │ JUST_PRESSED │
                    │  (1 frame)   │
                    └──────┬───────┘
                           │
                         HOLD
                           │
                           ▼
                    ┌──────────────┐
                    │   PRESSED    │◄─────────┐
                    └──────┬───────┘          │
                           │                 │
                         RELEASE             │
                           │                 │
                           ▼                  │
                    ┌──────────────┐          │
                    │  RELEASED    │──────────┘
                    └──────────────┘    HOLD (continue)
```

### 8.2 Input Mapping (Optional)

**Amaç:** Key mapping abstraction

**Implementasyon:**
```pseudocode
class InputMap:
    actions: Map<String, List<InputCode>>

    function bind(action_name, input_codes):
        actions[action_name] = input_codes

    function is_action_pressed(action_name):
        for code in actions[action_name]:
            if input_manager.is_pressed(code):
                return true
        return false

# Usage
input_map.bind("jump", [KEY_SPACE, KEY_UP, JOY_BTN_0])
input_map.bind("shoot", [KEY_Z, MOUSE_BTN_1, JOY_BTN_2])

# In game
if input_map.is_action_pressed("jump"):
    player.jump()
```

---

## 9. Audio Sistemi

### 9.1 Audio Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AUDIO SYSTEM                             │
└─────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │ AudioManager    │
                    │  (Singleton)    │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     ┌────────────────┐            ┌────────────────┐
     │ Music Channel  │            │  SFX Channels  │
     │  (Streaming)   │            │  (Pre-loaded)  │
     │                │            │                │
     │ - 1 track max  │            │ - 8-32 channels│
     │ - Fade in/out  │            │ - Overlap OK   │
     └────────────────┘            └────────────────┘
```

### 9.2 Volume Architecture

```
                    Master Volume (AudioManager)
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
     Music Volume                   SFX Volume
            │                             │
    ┌───────┴───────┐           ┌─────────┴─────────┐
    ▼               ▼           ▼                   ▼
Track1          Track2      SFX1                SFX2
Vol × 0.8      Vol × 0.6   Vol × 1.0          Vol × 0.9
```

**Final Volume Formülü:**
```
Music:  final_vol = track_volume × music_volume
SFX:    final_vol = sfx_base_volume × sfx_volume
```

---

## 10. Collision Sistemi

### 10.1 Collision Detection

**Hitbox Component:**
```pseudocode
class HitboxComponent:
    rects: List<Rect>

    function get_world_rects(entity):
        world_rects = []
        for rect in rects:
            world_rect = Rect(
                entity.x + rect.offset_x,
                entity.y + rect.offset_y,
                rect.width,
                rect.height
            )
            world_rects.add(world_rect)
        return world_rects
```

**Collision Check:**
```pseudocode
function check_collision(entity1, entity2):
    hitbox1 = entity1.get_component("Hitbox")
    hitbox2 = entity2.get_component("Hitbox")

    if not hitbox1 or not hitbox2:
        return false

    rects1 = hitbox1.get_world_rects(entity1)
    rects2 = hitbox2.get_world_rects(entity2)

    for rect1 in rects1:
        for rect2 in rects2:
            if rect1.intersects(rect2):
                return true

    return false
```

### 10.2 Collision-Aware Movement

**Movability Component:**
```pseudocode
class MovabilityComponent:
    speed: Float
    collidable_tags: List<String>

    function move_x(entity, dx):
        # Multi-step movement
        max_step = 10
        steps = max(1, abs(dx) / max_step)
        step_distance = dx / steps

        for i in 0..steps:
            if not _move_x_step(entity, step_distance):
                return false  # Blocked
        return true

    function _move_x_step(entity, step_x):
        # Try move
        old_x = entity.x
        entity.x += step_x

        # Check collision
        if _check_collision(entity):
            entity.x = old_x  # Revert
            return false
        return true

    function _check_collision(entity):
        scene = Application.get_current_scene()

        for tag in collidable_tags:
            others = scene.get_objects_by_tag(tag)
            for other in others:
                if other != entity:
                    if check_collision(entity, other):
                        return true
        return false
```

---

## 11. Performans Optimizasyonları

### 11.1 Data Structures

**O(1) Lookups:**
```
objects: Map<String, Entity>
tags: Map<String, List<Entity>>
components: Map<String, Component>
```

**Avoid O(n) operations:**
```
❌ for entity in all_entities:
       if entity.tags.contains("enemy"):
           ...

✅ enemies = scene.get_objects_by_tag("enemy")
    for entity in enemies:
        ...
```

### 11.2 Culling (Optional)

**Frustum Culling:**
```pseudocode
function draw():
    camera_rect = get_camera_rect()

    for entity in entities:
        if not entity.bounds.intersects(camera_rect):
            continue  # Skip off-screen entities

        entity.draw()
```

**Distance Culling:**
```pseudocode
function update():
    player = scene.get_object("player")

    for entity in entities:
        distance = calculate_distance(player, entity)

        if distance < update_threshold:
            entity.update()
```

### 11.3 Object Pooling (Optional)

**Pattern:**
```pseudocode
class ObjectPool:
    pool: Queue<Entity>

    function acquire():
        if pool.is_empty():
            return create_new_entity()
        return pool.dequeue()

    function release(entity):
        entity.reset()
        pool.enqueue(entity)

# Usage
pool = ObjectPool()
bullet = pool.acquire()
# ... use bullet ...
pool.release(bullet)
```

---

## 12. UML Diyagramları

### 12.1 Class Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         APPLICATION                         │
├─────────────────────────────────────────────────────────────┤
│ - scenes: Map<String, Scene>                               │
│ - current_scene_name: String                               │
│ - delta_time: Float                                        │
│ - target_fps: Integer                                      │
├─────────────────────────────────────────────────────────────┤
│ + init(width, height, title): void                         │
│ + add_scene(name, scene): void                             │
│ + set_scene(name): void                                    │
│ + get_current_scene(): Scene                               │
│ + run(): void                                              │
│ + stop(): void                                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ 1..*
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                          SCENE                              │
├─────────────────────────────────────────────────────────────┤
│ - objects: Map<String, Entity>                             │
│ - tags: Map<String, List<Entity>>                          │
│ - pending_additions: List<Entity>                          │
│ - pending_removals: List<Entity>                           │
│ - width: Integer                                           │
│ - height: Integer                                          │
├─────────────────────────────────────────────────────────────┤
│ + add_object(entity): void                                 │
│ + remove_object(entity): void                              │
│ + get_object(name): Entity                                │
│ + get_objects_by_tag(tag): List<Entity>                   │
│ + update(): void                                           │
│ + draw(): void                                             │
│ - _apply_pending_updates(): void                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ 1..*
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                          ENTITY                             │
├─────────────────────────────────────────────────────────────┤
│ - name: String                                             │
│ - x: Float                                                 │
│ - y: Float                                                 │
│ - depth: Integer                                           │
│ - tags: Set<String>                                        │
│ - components: Map<String, Component>                       │
│ - dead: Boolean                                            │
├─────────────────────────────────────────────────────────────┤
│ + add_tag(tag): void                                       │
│ + remove_tag(tag): void                                    │
│ + has_tag(tag): Boolean                                    │
│ + kill(): void                                             │
│ + add_component(component, name): void                     │
│ + get_component(name): Component                          │
│ + update(): void                                           │
│ + draw(): void                                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ 1..*
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       COMPONENT                            │
├─────────────────────────────────────────────────────────────┤
│ # instance: Any                                            │
├─────────────────────────────────────────────────────────────┤
│ + update(entity): void                                     │
│ + draw(entity): void                                       │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
          ┌───────────────┼───────────────┐
          │               │               │
┌─────────────────┐ ┌────────────┐ ┌────────────┐
│     Image       │ │ Animation  │ │  Hitbox    │
├─────────────────┤ ├────────────┤ ├────────────┤
│ - pivot_x       │ │ - speed    │ │ - rects    │
│ - pivot_y       │ │ - loop     │ │            │
│ - image         │ │ - frames   │ │            │
├─────────────────┤ ├────────────┤ ├────────────┤
│ + draw(entity)  │ │+draw(ent)  │ │+get_world_ │
└─────────────────┘ └────────────┘ │ │rects(ent) │
                                     └────────────┘
```

### 12.2 Sequence Diagram - Game Loop

```
    ┌──────┐    ┌──────────┐    ┌──────────┐    ┌────────┐
    │ App  │    │InputMgr  │    │  Scene   │    │ Screen │
    └──┬───┘    └────┬─────┘    └────┬─────┘    └───┬────┘
       │             │               │              │
       │ run()       │               │              │
       ├─────────────┼───────────────┼──────────────┤
       │             │               │              │
       │ update()    │               │              │
       ├────────────→│               │              │
       │             │ process events│              │
       │             │<──────────────┤              │
       │◄────────────┤               │              │
       │             │               │              │
       │ update()    │               │              │
       ├────────────────────────────→│              │
       │             │               │              │
       │             │               │ for entity: │
       │             │               │   update()  │
       │             │               ├──────────────┤
       │             │               │              │
       │             │               │ apply_pending│
       │             │               ├──────────────┤
       │◄────────────────────────────┤              │
       │             │               │              │
       │ clear()     │               │              │
       ├──────────────────────────────────────────→│
       │◄──────────────────────────────────────────┤
       │             │               │              │
       │ draw()      │               │              │
       ├────────────────────────────→│              │
       │             │               │              │
       │             │               │ sort entities│
       │             │               │              │
       │             │               │ for entity: │
       │             │               │   draw()    │
       │             │               ├──────────────┤
       │             │               │              │
       │◄────────────────────────────┤              │
       │             │               │              │
       │ refresh()   │               │              │
       ├──────────────────────────────────────────→│
       │◄──────────────────────────────────────────┤
       │             │               │              │
       │ tick()      │               │              │
       ├────────────→│               │              │
       │◄────────────┤               │              │
       │             │               │              │
       └─────────────┴───────────────┴──────────────┘
                    repeat
```

---

## 13. Uygulama Kontrol Listesi

### 13.1 Minimum Viable Product (MVP)

**Core Systems:**
- [ ] Application singleton (main loop)
- [ ] Scene manager (entity container)
- [ ] Entity class (position, components)
- [ ] Component loader (built-in + user scripts)
- [ ] Input manager (keyboard + mouse)
- [ ] Screen/Display manager
- [ ] JSON scene loader

**Rendering:**
- [ ] Image component (sprite rendering)
- [ ] Depth sorting
- [ ] Background color/image

**Components:**
- [ ] Hitbox component (collision boxes)
- [ ] Movability component (collision-aware movement)

**Data Formats:**
- [ ] Scene JSON format
- [ ] Entity JSON format
- [ ] Component JSON format
- [ ] .obj template format

### 13.2 Full Feature Set

**Input:**
- [ ] Joystick/gamepad support
- [ ] Input mapping system
- [ ] Multi-touch (mobile)

**Audio:**
- [ ] Audio manager singleton
- [ ] Background music component
- [ ] Sound effect component
- [ ] Fade in/out effects
- [ ] Volume control

**Advanced Rendering:**
- [ ] Animation component (sprite sheets)
- [ ] YSort component (depth sorting)
- [ ] Camera system
- [ ] Particle system
- [ ] Render batching

**Collision:**
- [ ] Multiple hitboxes per entity
- [ ] Named hitboxes
- [ ] Spatial partitioning (quadtree)
- [ ] Collision groups/layers

**Performance:**
- [ ] Object pooling
- [ ] Frustum culling
- [ ] Distance culling
- [ ] Lazy loading

**Editor/Tools:**
- [ ] Visual scene editor
- [ ] Component inspector
- [ ] Profiler
- [ ] Debug renderer (hitboxes, etc.)

**Advanced Features:**
- [ ] Event bus system
- [ ] Asset hot-reloading
- [ ] Save/load system
- [ ] Localization
- [ ] Multiplatform support

### 13.3 Implementation Language Checklist

**C++ Implementation Considerations:**
- Use smart pointers (shared_ptr, unique_ptr)
- RAII for resource management
- Template-based component system
- STL containers (unordered_map, vector)
- Memory pool for entities

**C# Implementation Considerations:**
- Use properties instead of fields
- Interface-based component system
- LINQ for queries
- Garbage collection awareness
- Structs for small data types

**JavaScript/TypeScript Implementation:**
- Class-based or prototype-based
- Event loop optimization
- Typed arrays for performance
- Web Workers for multithreading
- Canvas or WebGL rendering

**Rust Implementation Considerations:**
- Ownership system for entity references
- Trait-based component system
- HashMap for lookups
- Zero-cost abstractions
- Compile-time safety

**Java Implementation Considerations:**
- Interface for components
- Generic types
- Garbage collection tuning
- ByteBuffer for asset loading
- Thread pools

---

## Appendix A: Terminoloji

| Terim | Açıklama |
|-------|----------|
| **ECS** | Entity-Component-System mimarisi |
| **Entity** | Oyun nesnesi, veri konteyneri |
| **Component** | Tekil davranış, modül |
| **System** | Entity ve Component koordinatörü |
| **Scene** | Entity konteyneri, sahne |
| **Singleton** | Tek örnek pattern'i |
| **Hitbox** | Collision box, çarpışma kutusu |
| **Pivot** | Dönüş/çekim merkezi noktası |
| **Depth** | Z-index, render derinliği |
| **YSort** | Y pozisyonuna göre derinlik sıralaması |
| **Tag** | Entity etiketi, kategorilendirme |
| **Delta Time** | Frame süresi (saniye) |
| **FPS** | Frames Per Second |
| **AABB** | Axis-Aligned Bounding Box |

---

## Appendix B: Best Practices

### Component Design
1. **Single Responsibility:** Her component tek bir işi yapsın
2. **Stateless:** Component'ler minimum state tutsun
3. **Reusable:** Farklı entity'lerde çalışabilmeli
4. **Testable:** Bağımsız test edilebilir olmalı

### Scene Organization
1. **Use .obj files:** Yeniden kullanılabilir template'ler
2. **Tag strategy:** Konsistant etiketlendirme
3. **Depth ranges:** Net derinlik aralıkları
4. **External assets:** Asset'leri JSON'dan ayır

### Performance
1. **O(1) lookups:** Hash tablo kullanımı
2. **Avoid per-frame allocation:** Object pooling
3. **Batch rendering:** Draw call optimizasyonu
4. **Lazy loading:** İhtiyaç duyulduğunda yükle

### Code Quality
1. **Clear naming:** Anlaşılır isimlendirme
2. **Documentation:** API dokümantasyonu
3. **Error handling:** Robust hata yönetimi
4. **Logging:** Debug loglama sistemi

---

## Appendix C: Example Implementations

### Example 1: Simple Movement Script

```pseudocode
class MovementScript:
    speed: Float

    function init(speed):
        this.speed = speed

    function update(entity):
        im = InputManager.getInstance()
        app = Application.getInstance()

        dx = im.is_pressed(KEY_D) - im.is_pressed(KEY_A)
        dy = im.is_pressed(KEY_S) - im.is_pressed(KEY_W)

        entity.x += dx * speed * app.delta_time
        entity.y += dy * speed * app.delta_time
```

### Example 2: Collision Detection

```pseudocode
class ProjectileScript:
    speed: Float
    direction: Vector

    function update(entity):
        app = Application.getInstance()
        scene = app.get_current_scene()

        # Move
        entity.x += direction.x * speed * app.delta_time
        entity.y += direction.y * speed * app.delta_time

        # Check collision
        enemies = scene.get_objects_by_tag("enemy")
        for enemy in enemies:
            if check_collision(entity, enemy):
                enemy.kill()
                entity.kill()
                break
```

### Example 3: Animation Controller

```pseudocode
class AnimationControllerScript:
    function update(entity):
        movement = entity.get_component("MovementComponent")
        animation = entity.get_component("AnimationComponent")

        if movement.is_moving:
            if movement.direction == "up":
                animation.set_animation("walk_up")
            elif movement.direction == "down":
                animation.set_animation("walk_down")
            elif movement.direction == "left":
                animation.set_animation("walk_left")
            elif movement.direction == "right":
                animation.set_animation("walk_right")
        else:
            animation.set_animation("idle")
```

---

**Döküman Sonu**

Bu döküman, 2D oyun motorlarının soyut mimarisini dil bağımsız şekilde sunar. Buradaki prensipler ve tasarımlar Python, C++, C#, Java, JavaScript, Rust veya herhangi başka bir dilde uygulanabilir.

Referans Implementasyon: [PyGamer/Gaminal v0.1.4]
Licence: MIT
