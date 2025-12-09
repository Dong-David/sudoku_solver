import cv2
import numpy as np
import easyocr
import os

# Lấy đường dẫn hiện tại để lưu ảnh debug
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG_BOARD_PATH = os.path.join(CURRENT_DIR, "debug_board.jpg")

# Khởi tạo EasyOCR
reader = easyocr.Reader(['en'], gpu=False, verbose=False)

# --- ĐÂY LÀ HÀM MỚI (ROBUST) ---
def pre_process_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Tăng độ Blur lên (9,9) để làm mịn nhiễu
    blur = cv2.GaussianBlur(gray, (9, 9), 1)
    
    # 2. Adaptive Threshold
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    # 3. Morph Open/Close: "Hàn gắn" các đường kẻ bảng bị đứt
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return thresh
# -------------------------------

def find_board_contours(thresh):
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if len(approx) == 4:
                return approx
    return None

def reorder_points(points):
    points = points.reshape((4, 2))
    new_points = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)
    new_points[0] = points[np.argmin(add)]
    new_points[2] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    new_points[1] = points[np.argmin(diff)]
    new_points[3] = points[np.argmax(diff)]
    return new_points

def get_digit_easyocr(cell_img, row, col):
    h, w = cell_img.shape[:2]
    
    # 1. Cắt viền 10%
    crop_h = int(h * 0.1)
    crop_w = int(w * 0.1)
    crop = cell_img[crop_h:h-crop_h, crop_w:w-crop_w]
    
    # 2. Xử lý ảnh
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    # Threshold OTSU
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # --- TỐI ƯU HÓA CHO SỐ 7 VÀ SỐ 1 ---
    # Kỹ thuật: "Dilate" (Nở ra) - Làm nét chữ dày lên
    kernel = np.ones((2, 2), np.uint8) # Tạo nhân 2x2
    binary = cv2.dilate(binary, kernel, iterations=1) # Làm đậm nét chữ
    
    # Thêm viền đen (Padding) quanh số để số nằm giữa, OCR dễ đọc hơn
    binary = cv2.copyMakeBorder(binary, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=0)
    # -----------------------------------

    # 3. Lọc nhiễu (GIẢM NGƯỠNG XUỐNG 40 ĐỂ BẮT SỐ MẢNH)
    non_zero_pixels = cv2.countNonZero(binary)
    if non_zero_pixels < 40: 
        return 0

    # 4. Đọc số
    try:
        # Đọc trên ảnh Binary đã làm đậm
        results = reader.readtext(binary, allowlist='123456789', detail=0)
        
        if len(results) > 0:
            text = ''.join(filter(str.isdigit, results[0]))
            if text:
                return int(text)
            
        # Nếu thất bại, thử đọc trên ảnh Xám gốc (Gray) nhưng cũng thêm viền
        gray_padded = cv2.copyMakeBorder(gray, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255) # Viền trắng cho ảnh xám
        results_gray = reader.readtext(gray_padded, allowlist='123456789', detail=0)
        if len(results_gray) > 0:
            text = ''.join(filter(str.isdigit, results_gray[0]))
            if text:
                return int(text)
                
    except Exception as e:
        print(f"Lỗi nhẹ tại ô {row},{col}: {e}")
        pass
        
    return 0

def extract_sudoku_from_image(image_path):
    print(f"Đang xử lý ảnh: {image_path}")
    if not os.path.exists(image_path): return None
    
    img = cv2.imread(image_path)
    
    # 1. Tìm bảng
    thresh_map = pre_process_image(img)
    contour = find_board_contours(thresh_map)
    
    if contour is None:
        print("Lỗi: Không tìm thấy khung bảng!")
        return None
        
    # 2. Cắt bảng (Giữ nguyên size 900x900 là chuẩn nhất)
    contour = reorder_points(contour)
    pts1 = np.float32(contour)
    width, height = 900, 900 
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_warp = cv2.warpPerspective(img, matrix, (width, height))
    
    cv2.imwrite(DEBUG_BOARD_PATH, img_warp)

    # 3. Cắt lưới và nhận diện
    grid = []
    cell_h = height // 9
    cell_w = width // 9
    
    print("Đang quét số (Chế độ tối ưu nét mảnh)...")
    for r in range(9):
        row_vals = []
        for c in range(9):
            y1, y2 = r * cell_h, (r + 1) * cell_h
            x1, x2 = c * cell_w, (c + 1) * cell_w
            cell_img = img_warp[y1:y2, x1:x2]
            
            val = get_digit_easyocr(cell_img, r, c)
            row_vals.append(val)
        grid.append(row_vals)
        
    return grid