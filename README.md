# S.E.N.T.I.N.E.L. (System for Ecliptic & Near-Earth Trajectory Intercept Logic)

ระบบตรรกะการสกัดกั้นวงโคจจรใกล้โลกและระนาบสุริยวิถี

## คำอธิบายย่อ
S.E.N.T.I.N.E.L. เป็นโครงการต้นแบบสำหรับการวิเคราะห์และวางแผนการสกัดกั้นวัตถุที่เข้าใกล้โลก (Near-Earth Objects) และการประเมินเส้นทางที่สัมพันธ์กับระนาบสุริยวิถี (ecliptic plane)

วัตถุประสงค์หลัก:
- วิเคราะห์ข้อมูลวงโคจรและเทเลเมทรี
- ประเมินความเสี่ยงการชน/เข้าใกล้
- สร้างแผนการสกัดกั้น (intercept) แบบตรรกะและให้คะแนนทางเลือก

(เอกสารนี้เป็น README ขั้นต้น — ปรับแต่งตามโมดูลและข้อมูลภายในโปรเจกต์จริงได้)

## คุณสมบัติ (Features)
- นำเข้าข้อมูลวงโคจร (ephemeris / TLE / telemetry)
- คำนวณจุดตัดแนวพิสัยกับระนาบสุริยวิถี
- ประเมินพารามิเตอร์ความเสี่ยงและเวลา/ตำแหน่งที่เหมาะสมสำหรับการสกัดกั้น
- ส่งออกแผนการและรายงานสรุป

## สัญญา/Contract (inputs, outputs, errors)
- Inputs: ไฟล์ระบุตำแหน่ง/เวลาของวัตถุ (เช่น TLE, SPICE kernels, CSV telemetry)
- Outputs: แผนการสกัดกั้นในรูปแบบ JSON/CSV, รายงานความเสี่ยง (human-readable)
- Error modes: ข้อมูลไม่ครบ/ไม่สมเหตุผล, ข้อจำกัดการคำนวณ (convergence), ข้อมูลเสียหาย

## ข้อพิจารณา/Edge cases
- ข้อมูลขาดช่วง (missing epochs) — ต้องมีการแทรก/ประมาณ
- วัตถุที่มีวงโคจรไม่แน่นอน (high uncertainty) — ต้องระบุระดับความเชื่อมั่น
- กรณีเวลาคำนวณยาวหรือตัวแบบไม่คงที่ — ต้องมี timeout/approximation

## ติดตั้ง (Installation)
โปรเจกต์นี้เขียนเป็น Python (ตัวอย่าง) — ปรับให้ตรงกับสภาพแวดล้อมจริงของคุณ

PowerShell (Windows):

```powershell
# สร้าง virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # ถ้ามีไฟล์ requirements.txt
```

ถ้าโปรเจกต์ยังไม่มีไฟล์ dependences ให้เพิ่มรายการที่จำเป็น เช่น numpy, scipy, astropy, poliastro, pandas ฯลฯ ตามความจำเป็น

## การใช้งานอย่างเร็ว (Quick start)
สมมติว่ามีไฟล์ `main.py` เป็นจุดเริ่มต้น:

```powershell
# รันสคริปต์หลัก
python .\main.py --help

# หรือรันด้วยอินพุตตัวอย่าง
python .\main.py --input sample_ephemeris.csv --mode analyze
```

ปรับคำสั่งใช้งานตาม CLI ที่โปรเจกต์กำหนดไว้

## รูปแบบข้อมูล (Data formats)
แนะนำให้รองรับอย่างน้อย:
- CSV: epoch, ra/dec หรือ position vectors
- TLE: 2-line element sets
- SPICE kernels หรือ JSON telemetry

ตัวอย่าง JSON output (แผนการสกัดกั้น):

```json
{
  "object_id": "2025AB",
  "risk_score": 0.87,
  "intercept_windows": [
    {"start": "2026-01-02T12:00:00Z", "end": "2026-01-02T18:00:00Z", "delta_v": 0.45}
  ]
}
```

## สถาปัตยกรรมโดยสังเขป (Architecture)
- data/ : ตัวประมวลผลและ parser สำหรับรูปแบบข้อมูลต่างๆ
- core/ : อัลกอริทึมคำนวณวงโคจร, โมดูลประเมินความเสี่ยง
- planner/ : ตัวสร้างและประเมินแผนการสกัดกั้น
- cli/ : ส่วนติดต่อบรรทัดคำสั่ง
- tests/ : ชุดทดสอบหน่วย

(ปรับโครงสร้างตามโค้ดในโปรเจกต์จริง)

## การทดสอบ (Testing)
- สร้าง unit tests สำหรับ:
  - parser ของข้อมูลวงโคจร
  - คำนวณจุดตัดและการประมาณตำแหน่ง
  - อัลกอริทึมการให้คะแนนความเสี่ยง

ตัวอย่างการรันทดสอบด้วย pytest:

```powershell
pip install pytest
pytest -q
```

## แนวทางการพัฒนาเพิ่มเติม
- เพิ่มการรองรับ SPICE/NAIF kernels เพื่อความแม่นยำสูง
- เพิ่มโมดูล uncertainty propagation (covariance) สำหรับคำนวณความไม่แน่นอน
- สร้าง CI (GitHub Actions) รัน lint และ unit tests

## การมีส่วนร่วม (Contributing)
ยินดีรับ PR และ issue สำหรับบั๊กหรือฟีเจอร์ใหม่ โปรดแนบตัวอย่างข้อมูลและคำอธิบายการทำซ้ำ

## ใบอนุญาต (License)
ระบุใบอนุญาตที่ต้องการ เช่น MIT

---

ถ้าต้องการ ฉันสามารถปรับ README ให้สั้นลง/ยาวขึ้น แปลเป็นภาษาอังกฤษทั้งหมด หรือเพิ่มส่วนที่เฉพาะเจาะจงกับโค้ดในโปรเจกต์ของคุณ (เช่น API ของ `main.py`) — บอกฉันได้เลยว่าต้องการแบบไหน