# S.E.N.T.I.N.E.L.

**System for Ecliptic & Near-Earth Trajectory Intercept Logic**

<div align="center">

```
███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗     
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
```

*ระบบตรรกะการสกัดกั้นวงโคจรใกล้โลกและระนาบสุริยวิถี*

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![NumPy](https://img.shields.io/badge/numpy-required-orange.svg)
![Matplotlib](https://img.shields.io/badge/matplotlib-required-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

</div>

---

## 📡 ภาพรวมระบบ

**S.E.N.T.I.N.E.L.** เป็นระบบจำลองวงโคจรดาราศาสตร์แบบ N-Body ที่ออกแบบมาเพื่อวิเคราะห์และประเมินความเสี่ยงจากวัตถุท้าทายโลก (Near-Earth Objects) ระบบใช้กลศาสตร์คลาสสิกและกฎการโคจรของเคปเลอร์ในการคำนวณวิถีโคจรแบบเรียลไทม์

### ✨ คุณสมบัติหลัก

- 🌍 **การจำลอง N-Body แบบเรียลไทม์** - คำนวณแรงโน้มถ่วงระหว่างดวงอาทิตย์ โลก และวัตถุเป้าหมาย
- 🎯 **การตรวจจับจุดเข้าใกล้ที่สุด (CPA)** - วิเคราะห์ระยะทางขั้นต่ำระหว่างวัตถุกับโลก
- ⚠️ **ระบบเตือนภัยการชน** - ตรวจจับการชนโดยตรงแบบเรียลไทม์
- 📊 **การแสดงผลแบบ Sci-Fi HUD** - กราฟิกสไตล์ห้องควบคุมอวกาศ
- 🔬 **การตรวจสอบความแม่นยำ** - วิเคราะห์องค์ประกอบวงโคจรก่อน-หลังการจำลอง
- 🎨 **Interface แบบ Terminal Matrix** - UI สีสันพร้อมเอฟเฟกต์พิเศษ

---

## 🚀 การติดตั้ง

### ความต้องการของระบบ

```bash
Python 3.7 หรือสูงกว่า
NumPy
Matplotlib
```

### ขั้นตอนการติดตั้ง

1. **Clone repository**
```bash
git clone https://github.com/yourusername/sentinel.git
cd sentinel
```

2. **ติดตั้ง dependencies**
```bash
pip install numpy matplotlib
```

3. **รันโปรแกรม**
```bash
python sentinel.py
```

---

## 💻 วิธีการใช้งาน

### การเริ่มต้น

เมื่อเริ่มโปรแกรม ระบบจะขอข้อมูลดังนี้:

```
INPUT TARGET DESIGNATION: Apophis
  > INPUT TARGET MASS (kg) [DEFAULT 1e10]: 6.1e10
  > INPUT PLOT TAG (e.g., red, cyan): red
  
--- [AWAITING ORBITAL TELEMETRY] ---
  > q (Perihelion) (AU): 0.746
  > a (Semi-major) (AU): 0.922

INPUT SIMULATION DURATION (YEARS): 10
```

### พารามิเตอร์อินพุต

| พารามิเตอร์ | คำอธิบาย | หน่วย | ตัวอย่าง |
|------------|----------|------|---------|
| **Designation** | ชื่อวัตถุเป้าหมาย | - | Apophis, Bennu |
| **Mass** | มวลของวัตถุ | kg | 6.1e10 |
| **Color** | สีในกราฟ | - | red, cyan, yellow |
| **q (Perihelion)** | ระยะใกล้ดวงอาทิตย์ที่สุด | AU | 0.746 |
| **a (Semi-major)** | แกนกึ่งเอกของวงรี | AU | 0.922 |
| **Duration** | ระยะเวลาจำลอง | ปี | 10 |

### ตัวอย่างวัตถุที่น่าสนใจ

#### 99942 Apophis
```
q: 0.746 AU
a: 0.922 AU
mass: 6.1e10 kg
```

#### 101955 Bennu
```
q: 0.897 AU
a: 1.126 AU
mass: 7.8e10 kg
```

#### 433 Eros
```
q: 1.133 AU
a: 1.458 AU
mass: 6.687e15 kg
```

---

## 📊 การแปลผลลัพธ์

### 1. ข้อมูลการคำนวณเริ่มต้น

```
--- [CALCULATION COMPLETE] ---
[ LOCKED     ] Target Velocity (q): 30.73 km/s
[ LOCKED     ] Target Period: 0.89 years
```

- **Velocity (q)**: ความเร็วที่จุด perihelion (คำนวณจาก vis-viva equation)
- **Period**: คาบการโคจรรอบดวงอาทิตย์ 1 รอบ

### 2. รายงานการประเมินภัย

```
--- [IMPACT HAZARD ASSESSMENT]: Apophis ---
Simulation Result: [NO IMPACT DETECTED]

--- [CLOSEST POINT OF APPROACH (CPA) LOG] ---
  > Min. Distance (MOID): 38,472.5 km
  > (Equiv. 0.000257 AU)
  > (Equiv. 0.10 Lunar Distances [LD])
  > Event Epoch: T+126.4 days (or 0.35 years)
```

**การแปลความหมาย:**
- **MOID < 0.05 AU** = วัตถุใกล้โลกมาก (Potentially Hazardous)
- **< 1 LD** = เข้าใกล้มากกว่าดวงจันทร์
- **< Earth Radius (6,371 km)** = ชนโลก!

### 3. การตรวจสอบความถูกต้อง

```
--- [STATE VECTOR ANALYSIS]: TARGET ---
  > Semi-major axis (a): 0.9220 AU
  > Eccentricity (e):    0.1910
  > Perihelion (q):      0.7460 AU
  > Aphelion (Q):        1.0980 AU
```

ตัวเลขควรตรงกับอินพุตเริ่มต้น หากเบี่ยงเบนมาก อาจเกิดจาก:
- Timestep ใหญ่เกินไป
- เวลาจำลองยาวเกินไป
- วัตถุถูกเหวี่ยงออกจากระบบ

---

## 🔬 หลักการทางฟิสิกส์

### สมการหลักที่ใช้

**1. Vis-viva Equation (หาความเร็ว)**
```
v² = GM(2/r - 1/a)
```

**2. Newton's Law of Gravitation (แรงโน้มถ่วง)**
```
F = G(m₁m₂)/r²
a = GM/r²
```

**3. Kepler's Third Law (คาบการโคจร)**
```
P² = a³  (เมื่อ P ในหน่วยปี, a ในหน่วย AU)
```

**4. Euler-Cromer Integration**
```
v(t+Δt) = v(t) + a(t)·Δt
r(t+Δt) = r(t) + v(t+Δt)·Δt
```

### ค่าคงที่ทางฟิสิกส์

```python
G = 6.67430e-11      # Gravitational Constant (m³ kg⁻¹ s⁻²)
M_sun = 1.989e30     # Solar Mass (kg)
AU = 1.496e11        # Astronomical Unit (m)
LD = 3.844e8         # Lunar Distance (m)
R_earth = 6.371e6    # Earth Radius (m)
```

---

## 🎯 กรณีศึกษา: Apophis 2029

ในวันที่ 13 เมษายน 2029 ดาวเคราะห์น้อย Apophis จะโฉบเข้าใกล้โลกในระยะ **31,000 กม.** (ประมาณ 0.08 LD)

### การจำลองด้วย S.E.N.T.I.N.E.L.

```python
INPUT:
  Designation: Apophis
  Mass: 6.1e10 kg
  q: 0.746 AU
  a: 0.922 AU
  Duration: 10 years

OUTPUT:
  Min Distance: ~38,000 km (0.10 LD)
  Event Time: T+126 days
  Result: NO IMPACT (ผ่านไปอย่างปลอดภัย)
```

### Visualization Output

กราฟจะแสดง:
- 🟡 ดวงอาทิตย์พร้อมเอฟเฟกต์เรืองแสง
- 🔵 วงโคจรโลก (HOME - สีฟ้า)
- 🔴 วงโคจร Apophis (TARGET - สีแดง)
- ⚡ เส้นประสีแดง: จุด CPA (ระยะใกล้ที่สุด)

---

## ⚙️ การปรับแต่งขั้นสูง

### ปรับความละเอียดการคำนวณ

แก้ไขค่า `dt` ใน source code:

```python
# ความละเอียดสูง (ช้ากว่า แต่แม่นกว่า)
dt = 60 * 60 * 6  # 6 ชั่วโมง

# ความละเอียดกลาง (Default)
dt = 60 * 60 * 12  # 12 ชั่วโมง

# ความละเอียดต่ำ (เร็วกว่า แต่อาจไม่แม่น)
dt = 60 * 60 * 24  # 1 วัน
```

### เพิ่มวัตถุท้าทายโลกอื่นๆ

```python
# เพิ่มใน bodies list
venus = CelestialBody(
    name="VENUS",
    mass=4.867e24,
    x_pos=0.723 * AU,
    y_pos=0.0,
    x_vel=0.0,
    y_vel=35020.0,
    color='orange'
)
bodies.append(venus)
```

---

## 🐛 การแก้ปัญหา

### ปัญหาที่พบบ่อย

**1. โปรแกรมช้ามาก**
- ลด simulation duration
- เพิ่มค่า `dt` (timestep)
- ใช้วัตถุน้อยลง

**2. ผลลัพธ์ไม่ถูกต้อง**
- ตรวจสอบหน่วยอินพุต (ต้องเป็น AU)
- ตรวจสอบ q < a (perihelion ต้องน้อยกว่า semi-major axis)
- ลดค่า `dt` เพื่อความแม่นยำ

**3. กราฟไม่แสดง**
- ตรวจสอบการติดตั้ง matplotlib
- ลองรันด้วย `python -m sentinel.py`

**4. IndexError ในการ plot CPA**
- เกิดจากการชนก่อนสิ้นสุด simulation
- เป็นปกติ ระบบจะแสดงข้อความ IMPACT DETECTED

---

## 📚 ข้อมูลอ้างอิง

### หนังสือและเอกสาร
- *Orbital Mechanics for Engineering Students* - Howard Curtis
- *Fundamentals of Astrodynamics* - Bate, Mueller, White
- NASA JPL Small-Body Database: https://ssd.jpl.nasa.gov/

### Databases ที่เป็นประโยชน์
- **NASA JPL**: https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html
- **Minor Planet Center**: https://www.minorplanetcenter.net/
- **NEODyS**: https://newton.spacedys.com/neodys/

---

## 🤝 การมีส่วนร่วม

หากต้องการปรับปรุงระบบ:

1. Fork โครงการนี้
2. สร้าง Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit การเปลี่ยนแปลง (`git commit -m 'Add some AmazingFeature'`)
4. Push ไปยัง Branch (`git push origin feature/AmazingFeature`)
5. เปิด Pull Request

---

## ⚖️ License

Pondet Puangpoo

---

## 🙏 กิตติกรรมประกาศ

พัฒนาโดย **Pondet Puangpoo**

พิเศษขอบคุณ:
- NASA JPL สำหรับฐานข้อมูล orbital elements
- ชุมชน Python/NumPy/Matplotlib
- นักดาราศาสตร์และนักวิทยาศาสตร์ด้านดาวเคราะห์น้อยทั่วโลก

---

## 📞 ติดต่อ

- **Email**: puangpoo.colamark@gmail.com

---

<div align="center">

```
"แม้ว่าดวงดาวจะเป็นปริศนา แต่วิทยาศาสตร์คือแสงสว่างที่นำทาง"

--- S.E.N.T.I.N.E.L. Team
```

**⭐ Star โปรเจกต์นี้ถ้าคุณชอบ!**

</div>