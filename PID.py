import cv2
import numpy as np
import serial
import time
import collections
import matplotlib.pyplot as plt
from joblib import load
# Đường dẫn đến mô hình đã lưu
model_path = "random_forest_model.joblib"
# Tải mô hình
loaded_model = load(model_path)

error_list_x = []
error_list_y = []

# Khởi tạo danh sách để lưu trữ các giá trị error_x
error_x_values = []
error_y_values = []
time_values = []
start_time = time.time()

# Mở cổng UART (thay đổi 'COM5' thành cổng UART thích hợp trên máy tính của bạn)
ser = serial.Serial('COM7', baudrate=115200, timeout=0)

# Khởi tạo camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Giảm độ phân giải
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Tọa độ ban đầu của hình vuông màu đỏ
square_x, square_y = 100, 100
setpoint_x, setpoint_y = 115, 115
square_center_x, square_center_y = 0, 0

# Biến để kiểm tra xem phím 'f' đã được nhấn hay chưa
draw_rectangle = False

# Định nghĩa các biến toàn cục cho PID
PID_params = {
    'x': {'error': 0, 'previous_error': 0, 'PID_i': 0, 'PID_p': 0, 'PID_d': 0, 'kp': 2.5, 'kd': 45, 'ki': 0.2, 'period': 1},
    'y': {'error': 0, 'previous_error': 0, 'PID_i': 0, 'PID_p': 0, 'PID_d': 0, 'kp': 2.5, 'kd': 45, 'ki': 0.2, 'period': 1}
}

# Giới hạn cho PID_i
INTEGRAL_MIN = -100
INTEGRAL_MAX = 90

def PID_control(axis):
    params = PID_params[axis]
    if params['error'] == -1:
        return 0

    # Tính toán PID_p
    params['PID_p'] = params['kp'] * params['error']

    # Tính toán PID_d
    params['PID_d'] = params['kd'] * ((params['error'] - params['previous_error']) / params['period'])

    # Tính toán PID_i
    if -60 < params['error'] < 60:
        params['PID_i'] += params['ki'] * params['error']
        # Giới hạn giá trị của PID_i
        if params['PID_i'] > INTEGRAL_MAX:
            params['PID_i'] = INTEGRAL_MAX
        elif params['PID_i'] < INTEGRAL_MIN:
            params['PID_i'] = INTEGRAL_MIN
    else:
        params['PID_i'] = 0

    PID_total = (params['PID_p'] + params['PID_i'] + params['PID_d']) * 0.05
    servo_angle = constrain(57 + PID_total*(-1) if axis == 'y' else 62 + PID_total, 10, 70)

    params['previous_error'] = params['error']
    return servo_angle

def constrain(value, min_value, max_value):
    return max(min_value, min(value, max_value))

# Khởi tạo cửa sổ trung bình trượt với kích thước nhỏ hơn
rolling_window = collections.deque(maxlen=1)
rolling_window1 = collections.deque(maxlen=10)

# Khởi tạo các biến dự đoán ban đầu
predicted_labels_x = []
predicted_labels_y = []

while True:
    oke = False
    # Đọc khung hình từ camera
    ret, frame = cap.read()
    
    # Chuyển đổi khung hình sang định dạng grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Áp dụng phép lọc Gaussian để làm mờ ảnh và loại bỏ nhiễu
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    if draw_rectangle:
        # Cắt phần hình ảnh trong phạm vi hình vuông
        roi = blurred_frame[square_y:square_y + 230, square_x:square_x + 230]
    else:
        roi = blurred_frame

    # Sử dụng phương pháp HoughCircles để nhận diện các hình tròn trong vùng ROI
    circles = cv2.HoughCircles(roi, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=50)
    if circles is not None:
        # Chuyển đổi tọa độ và bán kính của các hình tròn sang số nguyên
        circles = np.round(circles[0, :]).astype("int")

        # Vẽ các hình tròn được nhận diện lên khung hình gốc
        for (x, y, r) in circles:
            if r > 5 and r < 20:
                oke = True
                if draw_rectangle:
                    x += square_x
                    y += square_y
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                
                # Thêm tọa độ quả bóng vào danh sách trung bình trượt
                rolling_window.append((x, y))

                # Tính giá trị trung bình của tọa độ
                avg_x = int(np.mean([coord[0] for coord in rolling_window]))
                avg_y = int(np.mean([coord[1] for coord in rolling_window]))
                
                square_center_x = square_x + 5
                square_center_y = square_y + 5
                distance_x = avg_x - square_center_x
                distance_y = avg_y - square_center_y

                PID_params['x']['error'] = distance_x - setpoint_x
                
                error_list_x.append(PID_params['x']['error'])

                servo_angle_x = PID_control('x')

                PID_params['y']['error'] = distance_y - setpoint_y

                error_list_y.append(PID_params['y']['error'])

                servo_angle_y = PID_control('y')

                error_list_x.append(PID_params['x']['error'])
                error_list_y.append(PID_params['y']['error'])

                # Check if we have collected 20 error values
                if len(error_list_x) >= 20 and len(error_list_y) >= 20:
                        # Reshape the error list for prediction
                    error_list_x_reshaped = np.array(error_list_x).reshape(1, -1)
                    error_list_y_reshaped = np.array(error_list_y).reshape(1, -1)
                    
                    print(error_list_x_reshaped)
                    predicted_labels_x = loaded_model.predict(error_list_x_reshaped*0.05)
                    predicted_labels_y = loaded_model.predict(error_list_y_reshaped*0.05)

                    # print(predicted_labels_x)
                    # Clear the error lists
                    error_list_x = []
                    error_list_y = []

                    if predicted_labels_x and predicted_labels_y:
                        print("Can bang")
                    else:
                        print("Khong can bang")

                current_time = time.time() - start_time
                error_x_values.append(PID_params['x']['error']*0.05)
                error_y_values.append(PID_params['y']['error']*0.05)
                time_values.append(current_time)

                error_str = f"{servo_angle_x}x{servo_angle_y}\n"
                ser.write(error_str.encode())
                # print(error_str)

        if not oke:
            servo_angle_x = 55
            servo_angle_y = 55
            error_str = f"{servo_angle_x}x{servo_angle_y}\n"
            ser.write(error_str.encode())
            print("khong nhan dien duoc")

    cv2.rectangle(frame, (square_x, square_y), (square_x + 10, square_y + 10), (0, 0, 255), -1)
    cv2.rectangle(frame, (square_x + setpoint_x, square_y + setpoint_y), (square_x + setpoint_x + 10, square_y + setpoint_y + 10), (255, 0, 255), -1)
    if draw_rectangle:
        cv2.rectangle(frame, (square_x, square_y), (square_x + 230, square_y + 230), (0, 0, 255), 2)

    cv2.imshow("Camera", frame)
    
    key = cv2.waitKey(1)
    
    if key == ord('w'):
        square_y -= 5
    elif key == ord('s'):
        square_y += 5
    elif key == ord('a'):
        square_x -= 5
    elif key == ord('d'):
        square_x += 5
    elif key == ord('1'):
        setpoint_x, setpoint_y = 65, 65
    elif key == ord('2'):
        setpoint_x, setpoint_y = 165, 165
    elif key == ord('3'):
        setpoint_x, setpoint_y = 65, 165
    elif key == ord('4'):
        setpoint_x, setpoint_y = 165, 65
    elif key == ord('0'):
        setpoint_x, setpoint_y = 115, 115
    
    if key == ord('f'):
        draw_rectangle = not draw_rectangle
    
    if key & 0xFF == ord('q'):
        break

ser.close()
cap.release()
cv2.destroyAllWindows()

plt.figure(1)
plt.plot(time_values, error_x_values)
plt.xlabel('Time (s)')
plt.ylabel('Error X cm')
plt.title('Error X over Time')

plt.figure(2)
plt.plot(time_values, error_y_values)
plt.xlabel('Time (s)')
plt.ylabel('Error Y cm')
plt.title('Error Y over Time')
plt.show()
