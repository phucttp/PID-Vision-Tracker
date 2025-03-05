# 🎯 Hệ Thống Cân Bằng Vật Thể Dựa Trên PID 🎯

## 📌 Giới Thiệu
Hệ thống này sử dụng PID (**Proportional-Integral-Derivative**) để cân bằng một vật thể trên mặt phẳng động.
Camera điện thoại thông minh được dùng để theo dõi vị trí vật thể theo thời gian thực, sau đó gửi dữ liệu về vi điều khiển qua **UART** để điều chỉnh động cơ servo.

📷 **Camera → Xử lý hình ảnh → Tính toán lỗi PID → Điều khiển servo**

🔹 **Lưu ý:** Mô hình học máy chỉ được sử dụng để xác nhận xem vật thể có đang cân bằng hay không. Việc điều khiển hệ thống hoàn toàn do thuật toán **PID** đảm nhiệm.

## 🚀 Tính Năng Chính
✅ Theo dõi vật thể theo thời gian thực bằng **OpenCV**.  
✅ Điều khiển **PID** linh hoạt, giúp hệ thống đạt trạng thái cân bằng nhanh chóng.  
✅ Kết nối với **vi điều khiển** qua **UART** để phản hồi ngay lập tức.  
✅ **PID Tuning "bằng cơm"** – tinh chỉnh từng tham số để đạt hiệu suất tối ưu.  

---

## 🛠️ Yêu Cầu Hệ Thống

### 🔌 Phần Cứng
- **Máy tính chạy Windows 10**.
- **Camera điện thoại thông minh** để theo dõi vật thể (ưu tiên kết nối có dây để giảm độ trễ).
- **Vi điều khiển** (ESP32, Arduino, STM32, ...) kết nối qua **UART**.
- **Động cơ servo** để điều chỉnh mặt phẳng cân bằng.

### 💻 Phần Mềm
Cài đặt các thư viện cần thiết trên **Python**:

```bash
pip install opencv-python numpy matplotlib joblib pyserial
```

---

## 🎮 Cách Sử Dụng

### 1️⃣ Kết nối camera điện thoại với máy tính
Sử dụng **IVCam** (Android) hoặc **DroidCam** để truyền video.

### 2️⃣ Chạy mô hình đã huấn luyện
```python
from joblib import load
model = load("random_forest_model.joblib")
```

### 3️⃣ Mở cổng UART với vi điều khiển
```python
import serial
ser = serial.Serial('COM7', baudrate=115200, timeout=0)
```

### 4️⃣ Chạy chương trình chính
```bash
python main.py
```

### 5️⃣ Điều chỉnh thông số PID bằng phím tắt
| Phím | Chức năng |
|------|-----------|
| W/A/S/D | Di chuyển cửa sổ theo dõi |
| 1-4 | Thay đổi điểm đặt (**setpoint**) |
| F | Bật/tắt khu vực theo dõi |
| Q | Thoát chương trình |

---

## 🎛️ PID Tuning "Bằng Cơm"

Chỉnh **PID** theo cách "cảm nhận" hệ thống từng bước như sau:

🔹 **Bước 1**: Chỉnh **Kp** – tăng dần cho đến khi hệ thống phản hồi nhanh nhưng không dao động mạnh.  
🔹 **Bước 2**: Chỉnh **Kd** – thêm vào để giảm dao động, tránh rung lắc.  
🔹 **Bước 3**: Chỉnh **Ki** – thêm vào nếu có sai số dư, nhưng đừng quá cao kẻo bị trễ.  

🔥 **Tip "Cơm"**: Nếu bị dao động quá mức, tắt một pha (**Kd hoặc Ki**) rồi chỉnh lại từ đầu!

Ví dụ thông số **PID** chuẩn bị chạy:
```python
PID_params = {
    'x': {'kp': 2.5, 'ki': 0.2, 'kd': 45},
    'y': {'kp': 2.5, 'ki': 0.2, 'kd': 45}
}
```

---

## 📸 Hình Ảnh & Video
📌 Thêm ảnh chụp màn hình hệ thống tại đây  
📌 Thêm video demo quá trình cân bằng PID  

---

## 📜 Giấy Phép
Dự án được cấp phép theo **MIT License**.

