import pygame
import sys

# ===============================================================
# PHẦN LOGIC GIẢI SUDOKU (BACKTRACKING)
# ===============================================================

def solve(board):
    find = find_empty(board)
    if not find:
        return True
    row, col = find
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

def is_valid(board, num, pos):
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

# ===============================================================
# PHẦN GIAO DIỆN BẰNG PYGAME
# ===============================================================

pygame.init()
WIDTH, HEIGHT = 540, 620
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

FONT = pygame.font.SysFont("arial", 35)
SMALL_FONT = pygame.font.SysFont("arial", 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 0)     # màu xanh cho số do chương trình giải ra
GREEN = (0, 180, 0)
LIGHT_BLUE = (210, 230, 255)
RED = (255, 50, 50)
GRAY = (220, 220, 220)

cell_size = WIDTH // 9
selected = None

board = [[0 for _ in range(9)] for _ in range(9)]
user_cells = [[False for _ in range(9)] for _ in range(9)]  # đánh dấu ô người chơi nhập

def draw_grid():
    for i in range(10):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(SCREEN, BLACK, (0, i * cell_size), (WIDTH, i * cell_size), line_width)
        pygame.draw.line(SCREEN, BLACK, (i * cell_size, 0), (i * cell_size, WIDTH), line_width)

def draw_board():
    for r in range(9):
        for c in range(9):
            x, y = c * cell_size, r * cell_size
            color = LIGHT_BLUE if (r // 3 + c // 3) % 2 == 0 else WHITE
            pygame.draw.rect(SCREEN, color, (x, y, cell_size, cell_size))

            val = board[r][c]
            if val != 0:
                text_color = BLACK if user_cells[r][c] else BLUE
                text = FONT.render(str(val), True, text_color)
                SCREEN.blit(text, (x + 20, y + 10))

    if selected:
        r, c = selected
        pygame.draw.rect(SCREEN, RED, (c * cell_size, r * cell_size, cell_size, cell_size), 3)

def draw_buttons():
    pygame.draw.rect(SCREEN, GREEN, (60, 550, 200, 50), border_radius=8)
    pygame.draw.rect(SCREEN, RED, (320, 550, 140, 50), border_radius=8)
    solve_text = SMALL_FONT.render("Giải Sudoku", True, WHITE)
    clear_text = SMALL_FONT.render("Xóa", True, WHITE)
    SCREEN.blit(solve_text, (90, 560))
    SCREEN.blit(clear_text, (365, 560))

def clear_board():
    global board, user_cells
    board = [[0 for _ in range(9)] for _ in range(9)]
    user_cells = [[False for _ in range(9)] for _ in range(9)]

def main():
    global selected
    running = True
    while running:
        SCREEN.fill(GRAY)
        draw_board()
        draw_grid()
        draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < WIDTH:
                    selected = (y // cell_size, x // cell_size)
                elif 80 <= x <= 260 and 550 <= y <= 600:  # Nút giải
                    temp = [row[:] for row in board]
                    if solve(temp):
                        for r in range(9):
                            for c in range(9):
                                if not user_cells[r][c]:
                                    board[r][c] = temp[r][c]
                    else:
                        print("Không có lời giải hợp lệ.")
                elif 320 <= x <= 460 and 550 <= y <= 600:  # Nút xóa
                    clear_board()

            if event.type == pygame.KEYDOWN:
                if selected:
                    r, c = selected
                    if event.key == pygame.K_0 or event.key == pygame.K_DELETE:
                        board[r][c] = 0
                        user_cells[r][c] = False
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        board[r][c] = event.key - pygame.K_0
                        user_cells[r][c] = True  # đánh dấu là do người chơi nhập

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
