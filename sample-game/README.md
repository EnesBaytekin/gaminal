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
