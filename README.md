# S.E.N.T.I.N.E.L. (v4.6 - PyVista Stable)

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/numpy-required-orange.svg" alt="NumPy">
  <img src="https://img.shields.io/badge/matplotlib-required-green.svg" alt="Matplotlib">
  <img src="https://img.shields.io/badge/skyfield-required-blue.svg" alt="Skyfield">
  <img src="https://img.shields.io/badge/pyvista-required-blue.svg" alt="PyVista">
  <img src="https://img.shields.io/github/stars/MarkeloPuangpoo/S.E.N.T.I.N.E.L.?style=social" alt="GitHub stars">
</p>

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

**[ 3D ASTRODYNAMICS KERNEL (PYVISTA) ]**

*ระบบตรรกะการสกัดกั้นวงโคจรใกล้โลกและระนาบสุริยวิถี*

 </div>


## 📡 ภาพรวมระบบ

**S.E.N.T.I.N.E.L. (v4.6)** คือระบบจำลองวงโคจรดาราศาสตร์แบบ N-Body 3 มิติ ที่ใช้ **`Skyfield`** ในการดึงข้อมูลตำแหน่งโลกและจัดการเวลา และใช้ **NumPy** ในการแปลง Orbital Elements 3 มิติที่ผู้ใช้ป้อน ให้เป็น State Vector (ตำแหน่งและความเร็ว 3D) เพื่อใช้เป็นจุดเริ่มต้นในการจำลอง

ผลลัพธ์การจำลองจะถูกแสดงผลเป็นภาพ 3 มิติ อินเทอร์แอกทีฟเต็มรูปแบบ ด้วย **`PyVista`** Visualization Engine ให้ความรู้สึกเหมือนกำลังใช้งานหน้าจอควบคุมในศูนย์บัญชาการอวกาศ

### ✨ คุณสมบัติหลัก (PyVista Edition)

  - 🪐 **Element-to-State Vector Conversion** - แปลงองค์ประกอบวงโคจร 3 มิติ (a, e, i, node, peri, M) ที่ป้อน ให้เป็นเวกเตอร์เริ่มต้น `[x,y,z]` และ `[vx,vy,vz]` โดยใช้ NumPy
  - 🌍 **การจำลอง N-Body 3 มิติ** - คำนวณแรงโน้มถ่วงระหว่างดวงอาทิตย์, โลก (ดึงตำแหน่งจาก `Skyfield`), และเป้าหมาย
  - 🎯 **การตรวจจับจุดเข้าใกล้ที่สุด (CPA)** - วิเคราะห์และแสดงผลระยะทางขั้นต่ำใน 3 มิติ
  - ⚠️ **ระบบเตือนภัยการชน** - ตรวจจับและแจ้งเตือนการชนโดยตรง
  - 📊 **การแสดงผลแบบ PyVista 3D HUD** - กราฟิก 3 มิติ อินเทอร์แอกทีฟเต็มรูปแบบ (หมุน/ซูม/แพน) พร้อมเอฟเฟกต์ Sci-Fi
  - 🔬 **การตรวจสอบความแม่นยำ 3D** - คำนวณ Elements กลับจาก State Vector หลังการจำลอง เพื่อตรวจสอบความเสถียร
  - 🎨 **Interface แบบ Terminal Matrix** - UI สีสันพร้อมเอฟเฟกต์พิเศษ

### หน้าจออินเทอร์เฟซ (Terminal Interface)

### ผลลัพธ์ PyVista 3D (Interactive Visualization)

*(**คำแนะนำ:** คุณต้องอัปโหลดภาพของคุณเอง (เช่น ใน imgur.com) แล้วเอาลิงก์มาใส่แทนที่ URL ด้านบน)*


## 🚀 การติดตั้ง

### ความต้องการของระบบ

```bash
Python 3.7 หรือสูงกว่า
NumPy
Skyfield
PyVista  <-- (ใหม่!)
# PyVista อาจต้องการ backend เพิ่มเติม (เช่น PyQt5) หากยังไม่มี:
# pip install pyqt5
```

### ขั้นตอนการติดตั้ง

1.  **Clone repository**

    ```bash
    git clone https://github.com/yourusername/sentinel.git
    cd sentinel
    ```

2.  **ติดตั้ง dependencies (สำคัญ)**

    ```bash
    pip install numpy skyfield pyvista
    # หาก PyVista มีปัญหาในการแสดงผล ลองติดตั้ง PyQt5:
    # pip install pyqt5
    ```

3.  **รันโปรแกรม**

    ```bash
    python main.py
    ```

    *(ครั้งแรกที่รัน Skyfield จะดาวน์โหลดไฟล์ `de421.bsp` (ประมาณ 17MB) โดยอัตโนมัติ ต้องใช้อินเทอร์เน็ต)*


## 💻 วิธีการใช้งาน (v4.6)

### การเริ่มต้น

ระบบจะขอข้อมูล **Orbital Elements 3 มิติ** (ซึ่งคุณสามารถหาได้จาก NASA JPL):

```
...SYSTEM BOOT COMPLETE. 3D KERNEL ENGAGED.
...Loading JPL Ephemeris...
[ OK         ] JPL Kernel 'de421.bsp' loaded.
[ OK         ] Timescale initialized.
...AWAITING COMMAND.


INPUT TARGET DESIGNATION: 2025 UG4
  > INPUT TARGET MASS (kg) [DEFAULT 1e10]: 1e10
  > INPUT PLOT TAG (e.g., red, cyan): red

(All angles in DEGREES, distances in AU)
  > q (Perihelion distance) (AU): 0.52456
  > e (Eccentricity): 0.80712
  > i (Inclination) (deg): 10.633
  > node (Long. of Asc. Node) (deg): 26.701
  > peri (Argument of Perihelion) (deg): 100.497
  > M (Mean Anomaly at Epoch) (deg): 349.468

... [STATE VECTORS LOCKED (T=NOW)] ...
[ LOCKED     ] Calculated Semi-major (a): 2.7231 AU
[ LOCKED     ] HOME Pos [X,Y,Z]: 0.18, 0.97, -0.00 AU
[ LOCKED     ] TARGET Pos [X,Y,Z]: 0.53, 0.05, 0.03 AU

INPUT SIMULATION DURATION (YEARS): 10
```

### พารามิเตอร์อินพุต (3D)

| พารามิเตอร์      | คำอธิบาย                               | หน่วย |
| :--------------- | :------------------------------------- | :---- |
| **Designation** | ชื่อวัตถุเป้าหมาย (สำหรับตั้งชื่อ)        | -     |
| **Mass** | มวลของวัตถุ                           | kg    |
| **Color** | สีในกราฟ                               | -     |
| **q (Perihelion)**| ระยะใกล้ดวงอาทิตย์ที่สุด                 | AU    |
| **e (Eccentricity)**| ความรีของวงโคจร (0-1)                 | -     |
| **i (Inclination)**| ความเอียงของวงโคจร                      | deg   |
| **node (Longitude)**| ลองจิจูดของโหนดขึ้น                     | deg   |
| **peri (Argument)**| อาร์กิวเมนต์ของเพริฮีเลียน               | deg   |
| **M (Mean Anomaly)**| มุมโคจรเฉลี่ย (ณ เวลาปัจจุบัน)          | deg   |
| **Duration** | ระยะเวลาจำลอง                           | ปี    |

*(ค่า `a` (Semi-major axis) จะถูกคำนวณอัตโนมัติจาก `q` และ `e`)*

### แหล่งข้อมูลสำหรับ 3D Elements

คุณสามารถหาค่าเหล่านี้ได้จาก **NASA JPL Small-Body Database**:

1.  ไปที่: [https://ssd.jpl.nasa.gov/tools/sbdb\_lookup.html](https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html)
2.  ค้นหาวัตถุ (เช่น `Bennu` หรือ `(2025 UG4)`)
3.  ดูที่ตาราง **"Orbital Elements"** และป้อนค่า `e`, `q`, `i`, `node` (RAAN), `peri` (arg of peri), `M`


## 📊 การแปลผลลัพธ์ (PyVista 3D)

### 1\. ข้อมูลการคำนวณเริ่มต้น

`[ LOCKED ] TARGET Pos [X,Y,Z]: 0.53, 0.05, 0.03 AU`

  - นี่คือตำแหน่ง 3 มิติ *เริ่มต้น* ของวัตถุ (เทียบกับดวงอาทิตย์) ที่คำนวณได้จาก Elements ที่คุณป้อน ณ เวลาปัจจุบัน

### 2\. รายงานการประเมินภัย (3D)

```
Simulation Result: [NO IMPACT DETECTED] (Within 10yr window)

  > Min. Distance (MOID): 1,234,567.8 km
  > (Equiv. 0.008253 AU)
  > (Equiv. 3.21 Lunar Distances [LD])
  > Event Epoch:          T+1234.5 days (or 3.38 years)
```

  - **MOID (Min. Distance)**: คือระยะห่าง 3 มิติ ที่สั้นที่สุดที่พบระหว่างการจำลอง

### 3\. การตรวจสอบความถูกต้อง (3D)

```
  > Semi-major axis (a): 2.7231 AU
  > Eccentricity (e):    0.8071
  > Inclination (i):     10.6330 deg
  > Perihelion (q):      0.5246 AU
  > Aphelion (Q):        4.9217 AU
```

  - ค่าเหล่านี้ ณ **สิ้นสุด** การจำลอง ควรใกล้เคียงกับค่าเริ่มต้น หากเบี่ยงเบนมาก อาจเกิดจากความคลาดเคลื่อนสะสม (ลองลด `dt`) หรือวัตถุถูกแรงรบกวนมาก


## 🔬 หลักการทางฟิสิกส์ (v4.6)

### สมการหลักที่ใช้

**1. Element-to-State-Vector Conversion (NumPy)**

  - **Kepler's Equation (แก้สมการเชิงตัวเลข)**
    ```
    M = E - e·sin(E)
    ```
  - **Orbital Plane -\> Perifocal Coordinates**
  - **Rotation Matrices (Perifocal -\> Ecliptic J2000)**

**2. Skyfield (ดึงตำแหน่งโลก)**

  - `(planets['earth'] - planets['sun']).at(t)`: คำนวณ State Vector ของโลก เทียบกับดวงอาทิตย์ ณ เวลา `t`

**3. N-Body & Integration**

  - **Newton's Law of Gravitation (3D Vector)**
    ```
    a_vec = GM/r³ · r_vec
    ```
  - **Euler-Cromer Integration (3D Vector)**
    ```
    v(t+Δt) = v(t) + a(t)·Δt
    r(t+Δt) = r(t) + v(t+Δt)·Δt
    ```


## ⚙️ การปรับแต่งขั้นสูง

### ปรับความละเอียดการคำนวณ

แก้ไขค่า `dt` ใน source code:

```python
# ความละเอียดสูง (ช้ากว่า แต่แม่นกว่า)
# dt = 60 * 60 * 6  # 6 ชั่วโมง

# ความละเอียดกลาง (Default)
dt = 60 * 60 * 12  # 12 ชั่วโมง
```

### เพิ่มวัตถุ 3 มิติอื่นๆ

1.  หา 3D Elements ของวัตถุนั้นๆ (q, e, i, node, peri, M)
2.  ใช้ฟังก์ชัน `classical_elements_to_state()` เพื่อหา `pos_new`, `vel_new`
3.  สร้าง `CelestialBody` ใหม่ และเพิ่มเข้า `bodies` list:

<!-- end list -->

```python
# ตัวอย่าง: เพิ่มดาวอังคาร (ค่าสมมติ)
q_mars = 1.381; e_mars = 0.093; i_mars = 1.85; ...
pos_mars, vel_mars = classical_elements_to_state(q_mars/(1-e_mars), e_mars, i_mars, ...)

mars_body = CelestialBody(
    name="MARS", mass=6.417e23, color='orangered',
    x_pos=pos_mars[0], y_pos=pos_mars[1], z_pos=pos_mars[2],
    x_vel=vel_mars[0], y_vel=vel_mars[1], z_vel=vel_mars[2]
)
bodies.append(mars_body)
```


## 🐛 การแก้ปัญหา

### ปัญหาที่พบบ่อย

**1. โปรแกรมช้ามาก**

  - ลด simulation duration
  - เพิ่มค่า `dt` (timestep) - อาจลดความแม่นยำ
  - ลองปิด Anti-Aliasing ใน PyVista (Section 9)

**2. ผลลัพธ์ไม่ถูกต้อง / วัตถุหลุดวงโคจร**

  - ตรวจสอบหน่วยอินพุต (ต้องเป็น AU และ Degrees)
  - ตรวจสอบ `q > 0` และ `0 <= e < infinity` (ปกติ e ควร \< 2 สำหรับวัตถุในระบบสุริยะ)
  - ลดค่า `dt` เพื่อความแม่นยำ (เช่น `60*60*6`)
  - ตรวจสอบค่า `MIN_DISTANCE` และ `MAX_ACCELERATION` อาจต้องปรับหากวัตถุเข้าใกล้กันมากๆ

**3. หน้าต่าง PyVista ไม่ขึ้น / แครช**

  - ตรวจสอบว่าติดตั้ง `pyvista` และ `pyqt5` (หรือ backend อื่น) ครบถ้วน
  - ตรวจสอบ Error message ในเทอร์มินัล อาจบอกสาเหตุได้
  - ลองอัปเดตไดรเวอร์การ์ดจอ


## 📚 ข้อมูลอ้างอิง

  - **NASA JPL Small-Body Database**: [https://ssd.jpl.nasa.gov/](https://ssd.jpl.nasa.gov/)
  - **Fundamentals of Astrodynamics** - Bate, Mueller, White (สำหรับสูตรแปลง Elements)
  - **PyVista Documentation**: [https://docs.pyvista.org/](https://docs.pyvista.org/)
  - **Skyfield Documentation**: [https://rhodesmill.org/skyfield/](https://rhodesmill.org/skyfield/)


## 🤝 การมีส่วนร่วม

หากต้องการปรับปรุงระบบ:

1.  Fork โครงการนี้
2.  สร้าง Feature Branch (`git checkout -b feature/CoolFeature`)
3.  Commit การเปลี่ยนแปลง (`git commit -m 'Add CoolFeature'`)
4.  Push ไปยัง Branch (`git push origin feature/CoolFeature`)
5.  เปิด Pull Request


## ⚖️ License

Pondet Puangpoo


## 🙏 กิตติกรรมประกาศ

พัฒนาโดย **Pondet Puangpoo**

พิเศษขอบคุณ:

  - NASA JPL สำหรับฐานข้อมูล orbital elements และ Ephemeris data (ผ่าน Skyfield)
  - ทีมพัฒนา Skyfield และ PyVista สำหรับ Library ที่ยอดเยี่ยม
  - ชุมชน Python และ NumPy


## 📞 ติดต่อ

  - **Email**: puangpoo.colamark@gmail.com


<div align="center">

```
"Through simulation, we glimpse the cosmic ballet."

```

**⭐ Star โปรเจกต์นี้ถ้าคุณชอบ\!**

</div>