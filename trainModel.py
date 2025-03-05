import numpy as np
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Tạo dữ liệu mẫu đảm bảo cả hai lớp đều có mặt
np.random.seed(42)
num_samples_per_class = 1000

# Tạo dữ liệu cho lớp cân bằng (1)
X_balanced = np.random.uniform(-1, 1, (num_samples_per_class, 20))
y_balanced = np.ones(num_samples_per_class)

# Tạo dữ liệu cho lớp không cân bằng (0)
X_unbalanced = np.random.uniform(-10, 10, (num_samples_per_class, 20))
y_unbalanced = np.zeros(num_samples_per_class)

# Gộp dữ liệu lại
X = np.vstack((X_balanced, X_unbalanced))
y = np.hstack((y_balanced, y_unbalanced))

# Trộn dữ liệu
p = np.random.permutation(len(y))
X, y = X[p], y[p]

# Kiểm tra phân phối của nhãn trong dữ liệu
unique, counts = np.unique(y, return_counts=True)
print(f'Phan phoi nhan trong tap du lieu: {dict(zip(unique, counts))}')

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra với stratify để giữ nguyên phân phối của nhãn
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Kiểm tra phân phối của nhãn trong tập huấn luyện
unique, counts = np.unique(y_train, return_counts=True)
print(f'Phan phoi nhan trong tap huan luyen: {dict(zip(unique, counts))}')

# Khởi tạo và huấn luyện mô hình Random Forest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Lưu mô hình
model_path = "random_forest_model.joblib"
dump(model, model_path)

# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá độ chính xác
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')