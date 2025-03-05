# 🎯 PID-Based Object Balancing System 🎯

## 📌 Introduction
This system utilizes PID (**Proportional-Integral-Derivative**) control to balance an object on a dynamic platform. A smartphone camera tracks the object’s position in real time and sends data to a microcontroller via **UART** for servo motor adjustments.

📷 **Camera → Image Processing → PID Error Calculation → Servo Control**

## 🚀 Key Features
✅ Real-time object tracking using **OpenCV**.  
✅ Flexible **PID** control for quick system stabilization.  
✅ **UART** connection with a **microcontroller** for instant response.  
✅ **Manual PID Tuning** – fine-tune each parameter for optimal performance.  

---

## 🛠️ System Requirements
### 🔌 Hardware
- **Windows 10 PC** (as the software is primarily developed for Windows 10).
- **Smartphone camera** for object tracking (wired connection preferred to reduce latency).
- **Microcontroller** (ESP32, Arduino, STM32, etc.) connected via **UART**.
- **Servo motors** for platform adjustment.

### 💻 Software
Install the required **Python** libraries:
```bash
pip install opencv-python numpy matplotlib joblib pyserial
```

---

## 🎮 Usage Instructions
### 1️⃣ Connect the smartphone camera to the PC
Use **IVCam** (Android) or **DroidCam** for video streaming.

### 2️⃣ Load the trained model
```python
from joblib import load
model = load("random_forest_model.joblib")
```

### 3️⃣ Open UART communication with the microcontroller
```python
import serial
ser = serial.Serial('COM7', baudrate=115200, timeout=0)
```

### 4️⃣ Run the main program
```bash
python main.py
```

### 5️⃣ Adjust PID parameters using shortcut keys
| Key | Function |
|------|-----------|
| W/A/S/D | Move tracking window |
| 1-4 | Change **setpoint** |
| F | Toggle tracking area |
| Q | Exit program |

---

## 🎛️ Manual PID Tuning
Fine-tune **PID** parameters step by step:

🔹 **Step 1**: Adjust **Kp** – increase until the system responds quickly without excessive oscillations.  
🔹 **Step 2**: Adjust **Kd** – add to reduce oscillations and stabilize movements.  
🔹 **Step 3**: Adjust **Ki** – add only if there is a steady-state error but avoid high values to prevent lag.

🔥 **Tuning Tip**: If excessive oscillations occur, disable one term (**Kd or Ki**) and retune from scratch!

Example **PID** parameters:
```python
PID_params = {
    'x': {'kp': 2.5, 'ki': 0.2, 'kd': 45},
    'y': {'kp': 2.5, 'ki': 0.2, 'kd': 45}
}
```

---

## 🔧 ESP32 Firmware

### 🔹 Overview
The ESP32 firmware performs the following tasks:
- Receives object position data from the PC via UART.
- Calculates error and updates servo angles based on PID parameters.
- Controls two servo motors to maintain balance.

### 🔹 Workflow
1. Initialize ESP32, assign servo pins, and set up Serial communication.
2. Receive object position data from the PC via Serial.
3. If no object is detected, set error values to -1.
4. If valid data is received, update servo angles accordingly.
5. Repeat the loop.

### 🔹 UART Communication Format
ESP32 receives data from the PC in the format:
```
x_valuex y_value
```
- `x_value` and `y_value` represent the object's coordinates.
- If the object is not detected, ESP32 receives `"no"`.

### 🔹 ESP32 Code
```cpp
#include <Servo.h>
#include <Wire.h>

static const int servoPin1 = 16;
static const int servoPin2 = 17;
Servo servo1, servo2;

float x_error = -1, y_error = -1;
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(115200);
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  servo1.write(55);
  servo2.write(55);
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= 1) {
    previousMillis = currentMillis;
    processData();
    servo1.write(x_error);
    processData();
    servo2.write(y_error);
  }
}

void processData() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    if (input == "no") {
      x_error = -1;
      y_error = -1;
    } else {
      int separatorIndex = input.indexOf('x');
      if (separatorIndex != -1) {
        x_error = input.substring(0, separatorIndex).toInt();
        y_error = input.substring(separatorIndex + 1).toInt();
      }
    }
  }
}
```

### 🔹 Future Enhancements
- **Implement signal filtering** to reduce noise from the camera.
- **Optimize the PID algorithm** for faster response times.
- **Improve Serial communication** for efficient data handling.

---

## 📸 Images & Videos
📌 **System Images:**

 <img src="image2.jpg" alt="Top View" width="300"> <img src="image3.jpg" alt="Top View" width="300">
 
📌 **System Demo Videos:**

- Adjust balance position via keyboard
- Impressive balancing performance
- Upcoming update – Setpoint adjustment via mouse clicks
<img src="Demo2.gif" alt="Top View" width="500"> 
<img src="demo3.gif" alt="Top View" width="500"> 
<img src="demo4.gif" alt="Top View" width="500">

---

📜 License
🚀 Open-source project – Free to use for educational & commercial purposes

Created by Trần Trọng Phúc
📧 Contact: trantrongphucttp27@gmail.com

---

🔥 If you find this project useful, don't forget to **⭐ Star** the repo!  

