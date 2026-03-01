# Sample Game - PyGamer Collision System Demo

Bu sample game, PyGamer'ın tüm yeni componentlerini ve özelliklerini göstermek için hazırlanmıştır.

## Nasıl Çalıştırılır

```bash
cd sample-game
PYTHONPATH=.. python3 main.py
```

Veya otomatik test için:
```bash
PYTHONPATH=.. python3 visual_test.py
```

## Kontroller

### Player 1 (WASD)
- **W**: Yukarı hareket
- **A**: Sol hareket
- **S**: Aşağı hareket
- **D**: Sağ hareket
- Hız: 200 px/saniye

### Player 2 (Ok Tuşları)
- **↑**: Yukarı hareket
- **←**: Sol hareket
- **↓**: Aşağı hareket
- **→**: Sağ hareket
- Hız: 150 px/saniye

## Oyun İçindeki Objeler

### Karakterler (Players)
1. **player** - WASD tuşları ile kontrol edilir
2. **player2** - Ok tuşları ile kontrol edilir

### Kutular (Boxes)
- **box1**, **box2**
- "collidable" tag'ine sahip sabit objeler
- Player'lar çarparsa durur (collision blocking)

### Duvarlar (Walls)
- **wall_left**, **wall_right**, **wall_top**
- Player'ların geçemediği engeller
- Tamamen çarpışmaya dayalı

### Hareketli Engel (Moving Obstacle)
- **moving_obstacle**
- Sol-sağ giden otomatik kutu
- Player'lar çarparsa durur

### Dekorasyonlar (Decorations)
- Ağaçlar ve kuleler (çarpışma yok, üzerinden geçilebilir)

### Efektler (Effects)
- Animasyonlu efektler

## Collision Sistemi

### Hitbox Component
Her objeye çarpışma kutusu ekler:
```json
{
  "file": "@Hitbox",
  "args": [[offset_x, offset_y, width, height]]
}
```

**Parametreler:**
- `offset_x`, `offset_y`: Objeye göre konum
- `width`, `height`: Kutu boyutları

### Movability Component
Objelerin hareketi ve çarpışma kontrolü:
```json
{
  "file": "@Movability",
  "args": [speed, ["collidable", "wall"]]
}
```

**Parametreler:**
- `speed`: Hareket hızı (pixels/second)
- `collidables`: Çarpışacağı tag listesi

**Özellikler:**
1. **Collision Blocking**: Çarpışan objelerden geçilmez
2. **Multi-Step Movement**: Büyük hareketler 10px adımlara bölünür
3. **Tag-Based Filtering**: Sadece belirtilen tag'lere çarpışır

## Test Senaryoları

1. **Duvar Testi**: Duvara doğru koş
   - Tam kenarda durur
   - İçine girmez

2. **Kutu Testi**: Kutulara çarp
   - Kutular sabit kalır
   - Üzerlerinden geçilemez

## Ses ve Müzik Sistemi

Tüm sesler ve müzikler **objeler üzerinden** yönetilir. Scene'de doğrudan müzik ayarı yok.

### BackgroundMusic Component

Arka plan müziği çalmak için objeye eklenir:

```json
{
  "x": 0,
  "y": 0,
  "name": "bg_music_player",
  "tags": [],
  "components": [
    {
      "file": "@BackgroundMusic",
      "args": ["sounds/music.ogg", true, 1.0, 0.6]
    }
  ]
}
```

**Parametreler:**
- `music_file`: Müzik dosyası (mp3, ogg, vb.)
- `loop`: Döngü çalsın mı? (true/false)
- `fade_in`: Fade-in süresi (saniye)
- `volume`: Ses seviyesi (0.0 - 1.0)

**Kod ile kullanım:**
```python
# Component'ten al
bg_music = obj.get_component("BackgroundMusic")

# Kontrol
bg_music.play()
bg_music.stop(fade_out=2.0)
bg_music.pause()
bg_music.resume()
bg_music.set_volume(0.5)
```

### SoundEffect Component

Objelere ses efekti eklemek için:

```json
{
  "file": "@SoundEffect",
  "args": ["footstep.wav", 1.0, false, false]
}
```

**Parametreler:**
- `sound_path`: Ses dosyası (wav, ogg)
- `volume`: Ses seviyesi (0.0 - 1.0)
- `auto_play`: Obje oluşturulunca otomatik çal
- `loop`: Döngü çal

**Kod ile kullanım:**
```python
# Component'ten ses al
sound = obj.get_component("SoundEffect")

# Çal
sound.play(volume=0.8)

# Durdur
sound.stop()
sound.pause()
sound.resume()

# Ses seviyesi
sound.set_volume(0.5)
```

### Örnek Kullanım

**Arka plan müziği için obje:**
```json
{
  "x": 0,
  "y": 0,
  "name": "music_player",
  "components": [
    {
      "file": "@BackgroundMusic",
      "args": ["music/dungeon.mp3", true, 3.0, 0.6]
    }
  ]
}
```

**Objede ses efekti:**
```python
# PlayerMovementScript'te
if dx != 0 and not sound.is_playing():
    sound.play()  # Yürürken adım sesi

if input_manager.is_just_pressed(pygame.K_SPACE):
    jump_sound.play()  # Zıplama sesi
```
