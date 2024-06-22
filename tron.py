import time
import curses
import random

p_pos = None
e_pos = None
p_dir = None
e_dir = None
frame = None
playing = True

def main(stdscr):
    global p_pos, e_pos, frame, playing
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Player color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Enemy color
    
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.cbreak()  
    
    INTERVAL = 0.1
    DIMENSION = 20

    while True:
        initialize_game(DIMENSION)
        draw_initial_frame(stdscr, DIMENSION)
        while playing:
            getPlayerDirection(stdscr)
            result = moveEntities(DIMENSION)
            update_frame(stdscr, DIMENSION)
            stdscr.refresh()
            time.sleep(INTERVAL)
            if result:
                break

        game_over(stdscr, DIMENSION, result)
        if not play_again(stdscr):
            break

def initialize_game(d):
    global p_pos, e_pos, frame, playing, p_dir, e_dir
    frame = [[None for _ in range(d*2)] for _ in range(d)]
    
    p_pos = get_random_position(d)
    e_pos = get_random_position(d)
    
    while manhattan_distance(p_pos, e_pos) < d // 2:
        e_pos = get_random_position(d)
    
    p_dir = get_random_direction()
    e_dir = get_random_direction()
    
    frame[p_pos[0]][p_pos[1]] = 'p'
    frame[e_pos[0]][e_pos[1]] = 'e'
    playing = True

def get_random_position(d):
    return [random.randint(2, d-3), random.randint(2, d*2-3)]

def get_random_direction():
    return random.choice([[-1, 0], [1, 0], [0, -1], [0, 1]])

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def getPlayerDirection(stdscr):
    global p_dir
    key = stdscr.getch()
    if key == ord('w') and p_dir != [1, 0]:
        p_dir = [-1, 0]
    elif key == ord('s') and p_dir != [-1, 0]:
        p_dir = [1, 0]
    elif key == ord('a') and p_dir != [0, 1]:
        p_dir = [0, -1]
    elif key == ord('d') and p_dir != [0, -1]:
        p_dir = [0, 1]

def moveEntities(d):
    global p_pos, e_pos, frame, playing, e_dir
    
    new_p_pos = [p_pos[0] + p_dir[0], p_pos[1] + p_dir[1]]
    
    if not is_valid_move(new_p_pos, d):
        playing = False
        return "You lose!"
    
    frame[new_p_pos[0]][new_p_pos[1]] = 'p'
    p_pos = new_p_pos
    
    # Enemy AI movement
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    if random.random() < 0.1:
        random.shuffle(directions)
    else:
        directions.sort(key=lambda dir: count_free_spaces(e_pos, dir, d), reverse=True)
    
    for direction in directions:
        new_e_pos = [e_pos[0] + direction[0], e_pos[1] + direction[1]]
        if is_valid_move(new_e_pos, d):
            frame[new_e_pos[0]][new_e_pos[1]] = 'e'
            e_pos = new_e_pos
            e_dir = direction
            return None
    
    playing = False
    return "You win!"

def count_free_spaces(pos, direction, d):
    count = 0
    x, y = pos
    dx, dy = direction
    while True:
        x += dx
        y += dy
        if not is_valid_move([x, y], d):
            break
        count += 1
    return count

def is_valid_move(pos, d):
    return (0 < pos[0] < d-1 and 0 < pos[1] < d*2-1 and 
            frame[pos[0]][pos[1]] is None)

def draw_initial_frame(stdscr, d):
    for y in range(d):
        for x in range(d*2):
            if x == 0 or x == d*2-1 or y == 0 or y == d-1:
                stdscr.addch(y, x, '#')
            else:
                stdscr.addch(y, x, ' ')
    stdscr.refresh()

def update_frame(stdscr, d):
    stdscr.addch(p_pos[0], p_pos[1], '&', curses.color_pair(1))
    stdscr.addch(e_pos[0], e_pos[1], '@', curses.color_pair(2))

def game_over(stdscr, d, result):
    stdscr.addstr(d // 2, d - 5, "GAME OVER")
    stdscr.addstr(d // 2 + 1, d - len(result)//2, result)
    stdscr.addstr(d // 2 + 2, d - 8, "Play again? (y/n)")
    stdscr.refresh()

def play_again(stdscr):
    while True:
        key = stdscr.getch()
        if key == ord('y'):
            return True
        elif key == ord('n'):
            return False

if __name__ == "__main__":
    curses.wrapper(main)