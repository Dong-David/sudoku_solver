import pygame
import sys
import random
import os

# ===============================================================
# CẤU HÌNH & KHỞI TẠO
# ===============================================================
pygame.init()
WIDTH, HEIGHT = 540, 700 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Noel Edition 🎄❄️")
clock = pygame.time.Clock() 

# --- XỬ LÝ ĐƯỜNG DẪN TỰ ĐỘNG ---
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tên file ảnh (Chỉ còn ảnh nền và ảnh gỗ làm nút)
BG_FILENAME = "1295969.jpg"     # Ảnh nền cây thông
WOOD_FILENAME = "428228.jpg"    # Ảnh gỗ (dùng làm nút)
FONT_FILENAME = "Playwrite.ttf" # Font chữ

BG_PATH = os.path.join(current_dir, BG_FILENAME)
WOOD_PATH = os.path.join(current_dir, WOOD_FILENAME)
FONT_PATH = os.path.join(current_dir, FONT_FILENAME)

# --- HÀM TẠO ASSETS ---
def create_assets():
    assets = {}
    
    # 1. Background
    try:
        bg_raw = pygame.image.load(BG_PATH)
        assets["bg"] = pygame.transform.scale(bg_raw, (WIDTH, HEIGHT))
    except: assets["bg"] = None

    # 2. Gỗ (Để làm texture cho nút)
    try:
        wood_raw = pygame.image.load(WOOD_PATH)
        assets["wood"] = wood_raw 
    except: assets["wood"] = None

    return assets

GAME_ASSETS = create_assets()

# --- LOAD FONT ---
try:
    FONT = pygame.font.Font(FONT_PATH, 35) 
    SMALL_FONT = pygame.font.Font(FONT_PATH, 24)
    NUM_FONT = pygame.font.Font(FONT_PATH, 40)
except:
    FONT = pygame.font.SysFont("comicsans", 35, bold=True)
    SMALL_FONT = pygame.font.SysFont("comicsans", 24, bold=True)
    NUM_FONT = pygame.font.SysFont("arial", 40, bold=True)

# --- BẢNG MÀU ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 20, 60)      

# --- CHỈNH ĐỘ TRONG SUỐT (GLASSMORPHISM) ---
CELL_BG_ODD = (240, 248, 255, 190)  
CELL_BG_EVEN = (255, 255, 255, 110) 

# Highlight
HIGHLIGHT_RC = (255, 255, 0, 80)   
HIGHLIGHT_NUM = (50, 205, 50, 120)  

# Màu số
NUM_BLUE = (0, 0, 180)          
NUM_GRAY = (50, 50, 50)         
NUM_GREEN = (0, 100, 0)         
SNOW_WHITE = (255, 255, 255)

# --- [MỚI] MÀU BÁO LỖI (ĐỎ CRIMSON DỄ NHÌN) ---
ERROR_RED = (220, 20, 60) 

# Màu cơ bản cho nút
BTN_BASE_GRAY = (200, 200, 200)   
BTN_RED = (200, 30, 30)
BTN_GREEN = (30, 160, 60)
BTN_ORANGE = (255, 165, 0)

CELL_SIZE = WIDTH // 9
grid = [[0]*9 for _ in range(9)]
original_grid = [[0]*9 for _ in range(9)]
selected = None  
is_input_mode = False
snowflakes = [] 

# ===============================================================
# LOGIC GAME
# ===============================================================
def init_snow(count=120):
    global snowflakes
    for _ in range(count):
        snowflakes.append([
            random.randint(0, WIDTH),      
            random.randint(-HEIGHT, 0),    
            random.uniform(0.5, 2.0),      
            random.randint(2, 4)           
        ])

def update_and_draw_snow():
    for flake in snowflakes:
        flake[1] += flake[2] 
        if flake[1] > HEIGHT:
            flake[1] = random.randint(-50, -10)
            flake[0] = random.randint(0, WIDTH)
        pygame.draw.circle(SCREEN, SNOW_WHITE, (int(flake[0]), int(flake[1])), flake[3])

init_snow()

def is_valid(board, num, pos):
    # Kiểm tra hàng
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i: return False
    # Kiểm tra cột
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i: return False
    # Kiểm tra ô 3x3
    box_x, box_y = pos[1] // 3, pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num and (i, j) != pos: return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0: return (i, j)
    return None

solve_steps = 0 

def solve(board, visualize=False):
    global solve_steps
    find = find_empty(board)
    if not find: return True
    row, col = find
    
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            
            if visualize:
                solve_steps += 1
                if solve_steps % 15 == 0: 
                    draw_window() 
                    pygame.display.update()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        pygame.quit()
                        sys.exit()
            
            if solve(board, visualize): return True
            
            board[row][col] = 0
            
    return False

def generate_random_puzzle():
    global grid, original_grid, is_input_mode
    is_input_mode = False
    grid = [[0]*9 for _ in range(9)]
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for r in range(3):
            for c in range(3):
                grid[i+r][i+c] = nums.pop()
    solve(grid, visualize=False)
    remove_count = 40
    while remove_count > 0:
        r, c = random.randint(0, 8), random.randint(0, 8)
        if grid[r][c] != 0: grid[r][c] = 0; remove_count -= 1
    original_grid = [row[:] for row in grid]

def enable_input_mode():
    global grid, original_grid, is_input_mode
    is_input_mode = True
    grid = [[0]*9 for _ in range(9)]
    original_grid = [[0]*9 for _ in range(9)]

# ===============================================================
# DRAWING
# ===============================================================

def draw_highlights():
    if not selected: return
    r_sel, c_sel = selected
    val_sel = grid[r_sel][c_sel]
    
    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    s.fill(HIGHLIGHT_RC)
    for i in range(9):
        SCREEN.blit(s, (i * CELL_SIZE, r_sel * CELL_SIZE))
        SCREEN.blit(s, (c_sel * CELL_SIZE, i * CELL_SIZE))

    if val_sel != 0:
        s_num = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        s_num.fill(HIGHLIGHT_NUM)
        for r in range(9):
            for c in range(9):
                if grid[r][c] == val_sel:
                     SCREEN.blit(s_num, (c*CELL_SIZE, r*CELL_SIZE))

def draw_grid_lines():
    GRID_COLOR = (0, 0, 0) 
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(SCREEN, GRID_COLOR, (0, i*CELL_SIZE), (WIDTH, i*CELL_SIZE), thickness)
        pygame.draw.line(SCREEN, GRID_COLOR, (i*CELL_SIZE, 0), (i*CELL_SIZE, WIDTH), thickness)

# --- [ĐÃ SỬA] HÀM VẼ SỐ CÓ KIỂM TRA LỖI ---
def draw_numbers():
    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            if val != 0:
                # 1. Tạm thời nhấc số ra để kiểm tra
                grid[r][c] = 0
                
                # 2. Kiểm tra xem số đó có hợp lệ ở vị trí (r, c) không
                if not is_valid(grid, val, (r, c)):
                    color = ERROR_RED  # Bị trùng -> Màu Đỏ
                else:
                    # Logic màu cũ
                    if original_grid[r][c] != 0: color = NUM_BLUE
                    elif is_input_mode: color = NUM_BLUE
                    else: color = NUM_GRAY
                
                # 3. Trả lại giá trị cho ô
                grid[r][c] = val 

                text = NUM_FONT.render(str(val), True, color)
                text_rect = text.get_rect(center=(c*CELL_SIZE + CELL_SIZE//2, r*CELL_SIZE + CELL_SIZE//2))
                SCREEN.blit(text, text_rect)

def draw_selection():
    if selected:
        r, c = selected
        pygame.draw.rect(SCREEN, (255, 0, 0), (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def draw_textured_button(label, x, y, w, h, base_color, is_active=False):
    # Bóng đổ
    pygame.draw.rect(SCREEN, (30, 30, 30, 180), (x+3, y+3, w, h), border_radius=12)

    # Texture Gỗ
    if GAME_ASSETS["wood"]:
        wood_tex = pygame.transform.scale(GAME_ASSETS["wood"], (WIDTH, HEIGHT))
        wood_cut = wood_tex.subsurface((x, y, w, h))
        SCREEN.blit(wood_cut, (x, y))
    else:
        pygame.draw.rect(SCREEN, base_color, (x, y, w, h), border_radius=12)

    # Tint màu
    tint_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay_color = (*base_color, 180) if not is_active else (255, 200, 50, 150)
    pygame.draw.rect(tint_surface, overlay_color, (0, 0, w, h), border_radius=12)
    SCREEN.blit(tint_surface, (x, y))

    # Viền
    border_col = (255, 255, 255) if not is_active else (255, 0, 0)
    pygame.draw.rect(SCREEN, border_col, (x, y, w, h), 2, border_radius=12)

    # Chữ
    text_surf = SMALL_FONT.render(label, True, WHITE)
    text_shadow = SMALL_FONT.render(label, True, (0,0,0))
    center_x, center_y = x + w//2, y + h//2
    text_rect = text_surf.get_rect(center=(center_x, center_y))
    SCREEN.blit(text_shadow, (text_rect.x + 1, text_rect.y + 1))
    SCREEN.blit(text_surf, text_rect)

def draw_buttons():
    y1, y2 = 570, 635
    btn_w, btn_h = 220, 50
    
    draw_textured_button("New Game", 30, y1, btn_w, btn_h, BTN_BASE_GRAY)
    draw_textured_button("Input Mode", 290, y1, btn_w, btn_h, BTN_ORANGE, is_input_mode)
    draw_textured_button("Solve Now", 30, y2, btn_w, btn_h, BTN_GREEN)
    draw_textured_button("Reset", 290, y2, btn_w, btn_h, BTN_RED)

def draw_window():
    if GAME_ASSETS["bg"]:
        SCREEN.blit(GAME_ASSETS["bg"], (0,0))
    else:
        SCREEN.fill(DARK_BLUE)
    
    update_and_draw_snow()

    s_odd = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    s_odd.fill(CELL_BG_ODD)   
    s_even = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    s_even.fill(CELL_BG_EVEN) 

    for r in range(9):
        for c in range(9):
            x, y = c * CELL_SIZE, r * CELL_SIZE
            if (r//3 + c//3) % 2 != 0: 
                 SCREEN.blit(s_odd, (x, y))
            else:
                 SCREEN.blit(s_even, (x, y))

    draw_highlights()
    draw_grid_lines()
    draw_numbers()
    draw_selection()
    draw_buttons()
    
    mode_text = "Mode: Input" if is_input_mode else "Mode: Player"
    text_surf = SMALL_FONT.render(mode_text, True, WHITE)
    text_shadow = SMALL_FONT.render(mode_text, True, BLACK)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, 553))
    
    SCREEN.blit(text_shadow, (text_rect.x + 1, text_rect.y + 1)) 
    SCREEN.blit(text_surf, text_rect) 

    pygame.display.update()

# ===============================================================
# MAIN LOOP
# ===============================================================
def main():
    global selected, grid, original_grid, is_input_mode, solve_steps
    generate_random_puzzle()
    running = True

    while running:
        clock.tick(60) 
        draw_window()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if y < WIDTH: selected = (y // CELL_SIZE, x // CELL_SIZE)
                
                elif 30 <= x <= 250 and 570 <= y <= 620: # New Game
                    generate_random_puzzle(); selected = None
                elif 290 <= x <= 510 and 570 <= y <= 620: # Input Mode
                    enable_input_mode(); selected = None
                elif 30 <= x <= 250 and 635 <= y <= 685: # Solve Now
                    if is_input_mode: 
                        original_grid = [row[:] for row in grid]
                        is_input_mode = False
                    
                    solve_steps = 0
                    solve(grid, visualize=True)
                    draw_window()
                    pygame.display.update()
                elif 290 <= x <= 510 and 635 <= y <= 685: # Reset
                    if is_input_mode: grid = [[0]*9 for _ in range(9)]; original_grid = [[0]*9 for _ in range(9)]
                    else: grid = [row[:] for row in original_grid]

            if event.type == pygame.KEYDOWN:
                if selected:
                    r, c = selected
                    if event.key == pygame.K_0 or event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        if is_input_mode or original_grid[r][c] == 0:
                            grid[r][c] = 0
                            if is_input_mode: original_grid[r][c] = 0
                    
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        val = event.key - pygame.K_0
                        # Chỉ cho phép nhập nếu ô đó không phải ô đề bài (hoặc đang ở Input Mode)
                        if is_input_mode: 
                            grid[r][c] = val; original_grid[r][c] = val
                        elif original_grid[r][c] == 0: 
                            grid[r][c] = val
                    
                    if event.key == pygame.K_LEFT:  selected = (r, max(0, c - 1))
                    elif event.key == pygame.K_RIGHT: selected = (r, min(8, c + 1))
                    elif event.key == pygame.K_UP:    selected = (max(0, r - 1), c)
                    elif event.key == pygame.K_DOWN:  selected = (min(8, r + 1), c)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
