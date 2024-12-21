from tkinter import *
import random

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
GAME_TICK_SPEED = 100
GRID_CELL_SIZE = 25
INITIAL_SNAKE_LENGTH = 3

COLOR_SNAKE = "#4ade80"
COLOR_SNAKE_HEAD = "#22c55e"
COLOR_FOOD = "#f87171"
COLOR_BACKGROUND = "#1e293b"
COLOR_GRID = "#334155"
COLOR_TEXT = "#f1f5f9"
COLOR_SCORE_BG = "#0f172a"

SCORE_FONT = ('Helvetica', 32, 'bold')
GAME_OVER_FONT = ('Helvetica', 64, 'bold')
RESTART_FONT = ('Helvetica', 24)

score = 0
movement_direction = 'right'
snake = None
food = None

class Snake:
    def __init__(self):
        self.length = INITIAL_SNAKE_LENGTH
        self.positions = []
        self.body_segments = []

        center_x = (WINDOW_WIDTH // GRID_CELL_SIZE) // 2 * GRID_CELL_SIZE
        center_y = (WINDOW_HEIGHT // GRID_CELL_SIZE) // 2 * GRID_CELL_SIZE
        
        for i in range(0, INITIAL_SNAKE_LENGTH):
            self.positions.append([center_x, center_y + (i * GRID_CELL_SIZE)])

        for i, (x, y) in enumerate(self.positions):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE
            segment = canvas.create_rectangle(
                x + 1, y + 1,
                x + GRID_CELL_SIZE - 1, 
                y + GRID_CELL_SIZE - 1,
                fill=color,
                outline="",
                tags="snake",
                width=0
            )
            self.body_segments.append(segment)

class Food:
    def __init__(self):
        x = random.randint(0, (WINDOW_WIDTH // GRID_CELL_SIZE) - 1) * GRID_CELL_SIZE
        y = random.randint(0, (WINDOW_HEIGHT // GRID_CELL_SIZE) - 1) * GRID_CELL_SIZE
        self.position = [x, y]

        self.glow = canvas.create_oval(
            x - 2, y - 2,
            x + GRID_CELL_SIZE + 2,
            y + GRID_CELL_SIZE + 2,
            fill=COLOR_FOOD,
            stipple='gray50',
            tags="food"
        )
        
        self.body = canvas.create_oval(
            x + 2, y + 2,
            x + GRID_CELL_SIZE - 2,
            y + GRID_CELL_SIZE - 2,
            fill=COLOR_FOOD,
            outline="",
            tags="food"
        )

def create_grid():
    for i in range(0, WINDOW_WIDTH, GRID_CELL_SIZE):
        canvas.create_line(i, 0, i, WINDOW_HEIGHT, fill=COLOR_GRID, width=1)
        canvas.create_line(0, i, WINDOW_WIDTH, i, fill=COLOR_GRID, width=1)

def update_game_state(snake, food):
    x, y = snake.positions[0]

    if movement_direction == "up": y -= GRID_CELL_SIZE
    elif movement_direction == "down": y += GRID_CELL_SIZE
    elif movement_direction == "left": x -= GRID_CELL_SIZE
    elif movement_direction == "right": x += GRID_CELL_SIZE

    snake.positions.insert(0, (x, y))
    
    new_segment = canvas.create_rectangle(
        x + 1, y + 1,
        x + GRID_CELL_SIZE - 1,
        y + GRID_CELL_SIZE - 1,
        fill=COLOR_SNAKE_HEAD,
        outline="",
        width=0
    )
    
    if snake.body_segments:
        canvas.itemconfig(snake.body_segments[0], fill=COLOR_SNAKE)
    
    snake.body_segments.insert(0, new_segment)

    if x == food.position[0] and y == food.position[1]:
        global score
        score += 1
        score_label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.positions[-1]
        canvas.delete(snake.body_segments[-1])
        del snake.body_segments[-1]

    if check_collision(snake):
        show_game_over()
    else:
        window.after(GAME_TICK_SPEED, update_game_state, snake, food)

def show_game_over():
    canvas.delete(ALL)
    create_grid()
    
    canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
                          fill=COLOR_BACKGROUND, stipple='gray50')
    
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2
    
    canvas.create_text(
        center_x + 2, center_y - 48,
        font=GAME_OVER_FONT,
        text="GAME OVER",
        fill="#000000",
        alpha=0.5
    )
    canvas.create_text(
        center_x, center_y - 50,
        font=GAME_OVER_FONT,
        text="GAME OVER",
        fill=COLOR_TEXT
    )
    
    canvas.create_text(
        center_x, center_y + 50,
        font=RESTART_FONT,
        text="Press R to Restart",
        fill=COLOR_TEXT,
        tags="restart_text"
    )

def handle_direction_change(new_direction):
    global movement_direction
    opposite_directions = {
        'left': 'right', 'right': 'left',
        'up': 'down', 'down': 'up'
    }
    if movement_direction != opposite_directions.get(new_direction):
        movement_direction = new_direction

def check_collision(snake):
    head_x, head_y = snake.positions[0]
    return (head_x < 0 or head_x >= WINDOW_WIDTH or 
            head_y < 0 or head_y >= WINDOW_HEIGHT or 
            any(head_x == segment[0] and head_y == segment[1] 
                for segment in snake.positions[1:]))

def reset_game():
    global snake, food, score, movement_direction
    canvas.delete(ALL)
    create_grid()
    
    score = 0
    movement_direction = 'right'
    score_label.config(text=f"Score: {score}")
    
    snake = Snake()
    food = Food()
    
    update_game_state(snake, food)

window = Tk()
window.title("Modern Snake")
window.resizable(False, False)
window.configure(bg=COLOR_SCORE_BG)

score_frame = Frame(window, bg=COLOR_SCORE_BG, pady=10)
score_frame.pack(fill='x')

score_label = Label(
    score_frame,
    text=f"Score: {score}",
    font=SCORE_FONT,
    fg=COLOR_TEXT,
    bg=COLOR_SCORE_BG
)
score_label.pack()

canvas = Canvas(
    window,
    bg=COLOR_BACKGROUND,
    height=WINDOW_HEIGHT,
    width=WINDOW_WIDTH,
    highlightthickness=0
)
canvas.pack()

window.update()
window_x = int((window.winfo_screenwidth() / 2) - (window.winfo_width() / 2))
window_y = int((window.winfo_screenheight() / 2) - (window.winfo_height() / 2))
window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{window_x}+{window_y}")

create_grid()

window.bind('<Left>', lambda event: handle_direction_change('left'))
window.bind('<Right>', lambda event: handle_direction_change('right'))
window.bind('<Up>', lambda event: handle_direction_change('up'))
window.bind('<Down>', lambda event: handle_direction_change('down'))
window.bind('<r>', lambda event: reset_game())

snake = Snake()
food = Food()

update_game_state(snake, food)

window.mainloop()