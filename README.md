# 🎄 Sudoku Giáng Sinh (Christmas Edition) ❄️

Chào mừng đến với **Sudoku Giáng Sinh** - một trò chơi giải đố Sudoku cổ điển được khoác lên mình giao diện lễ hội ấm áp với hiệu ứng tuyết rơi và các tính năng hỗ trợ thông minh. Dự án được viết bằng **Python** và thư viện **Pygame**.

![Sudoku Preview](https://via.placeholder.com/600x400?text=Screenshot+Game+Sudoku) 
*(Bạn có thể thay thế link trên bằng ảnh chụp màn hình game thực tế của bạn)*

## ✨ Tính Năng Chính

* **Giao diện Lễ hội:** Tông màu Đỏ, Xanh, Vàng ấm áp cùng hiệu ứng tuyết rơi (Snowfall Animation) liên tục.
* **Hai Chế độ chơi:**
    * **Player Mode:** Máy tạo đề, bạn tự giải.
    * **Input Mode:** Bạn tự nhập đề bài (từ sách, báo...) để máy giải hoặc để tự chơi.
* **Giải Tự Động (Visual Solver):** Tích hợp thuật toán **Backtracking** (Quay lui) có hiển thị quá trình giải trực quan (Animation "nhảy số").
* **Hệ thống tiện ích:**
    * Đồng hồ đếm giờ.
    * Kiểm tra lỗi sai (số sai sẽ hiện màu đỏ).
    * Tạo đề mới ngẫu nhiên (New Game).

## 🛠️ Cài Đặt

Để chạy được game, bạn cần cài đặt Python và thư viện Pygame.

1.  **Cài đặt Python:** [Tải tại python.org](https://www.python.org/)
2.  **Cài đặt thư viện Pygame:**
    Mở Terminal (hoặc CMD) và chạy lệnh sau:
    ```bash
    pip install pygame
    ```

## 🚀 Cách Chạy Game

1.  Đảm bảo bạn có đầy đủ 2 file trong cùng một thư mục:
    * `main.py` (Source code).
    * `PlaywriteNO-VariableFont_wght.ttf` (Font chữ Giáng sinh).
2.  Chạy file `main.py`:
    ```bash
    python main.py
    ```

## 🎮 Hướng Dẫn Chơi

### Các phím điều khiển
* **Chuột trái:** Chọn ô cần điền số hoặc bấm các nút chức năng.
* **Phím số (1-9):** Điền số vào ô đã chọn.
* **Phím Backspace / Delete:** Xóa số trong ô đã chọn.

### Các nút chức năng
* **New Game:** Tạo một bàn cờ Sudoku mới ngẫu nhiên.
* **Reset:** Xóa hết các số bạn đã điền, đưa bàn cờ về trạng thái ban đầu.
* **Solve Now:** Máy tính sẽ tự động giải bài toán cho bạn (có hiệu ứng chạy số).
* **Input Mode / Player Mode:** Chuyển đổi giữa chế độ nhập đề và chế độ chơi.

## 🧠 Thuật Toán

Game sử dụng thuật toán **Backtracking (Quay lui)** đệ quy để giải Sudoku:
1.  Tìm một ô trống.
2.  Thử điền các số từ 1 đến 9.
3.  Kiểm tra xem số đó có hợp lệ không (không trùng hàng, cột, ô 3x3).
4.  Nếu hợp lệ, đi tiếp sang ô tiếp theo.
5.  Nếu đi vào ngõ cụt, quay lại (backtrack) và thử số khác.

## 📂 Cấu Trúc Thư Mục

```text
Sudoku-Christmas/
├── main.py                         # Mã nguồn chính của trò chơi
├── PlaywriteNO-VariableFont_wght.ttf # Font chữ tùy chỉnh
└── README.md                       # Tài liệu hướng dẫn
