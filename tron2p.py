import time
import curses
import random

p1_pos = None
p2_pos = None
p1_dir = None
p2_dir = None
frame = None
playing = True

def main(stdscr):
    global p1_pos, p2_pos, frame, playing
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)   # Player 1 color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Player 2 color
    curses.curs_set(0)
    stdscr.nodelay(True)
    
    INTERVAL = 0.1
    DIMENSION = 30

    while True:
        initialize_game(DIMENSION)
        draw_initial_frame(stdscr, DIMENSION)
        while playing:
            getPlayerDirections(stdscr)
            result = movePlayers(DIMENSION)
            update_frame(stdscr, DIMENSION)
            stdscr.refresh()
            time.sleep(INTERVAL)
            if result:
                break

        game_over(stdscr, DIMENSION, result)
        if not play_again(stdscr):
            break

def initialize_game(d):
    global p1_pos, p2_pos, frame, playing, p1_dir, p2_dir
    frame = [[None for _ in range(d*2)] for _ in range(d)]
    
    p1_pos = get_random_position(d)
    p2_pos = get_random_position(d)
    
    while manhattan_distance(p1_pos, p2_pos) < d // 2:
        p2_pos = get_random_position(d)
    
    p1_dir = get_random_direction()
    p2_dir = get_random_direction()
    
    frame[p1_pos[0]][p1_pos[1]] = 'p1'
    frame[p2_pos[0]][p2_pos[1]] = 'p2'
    playing = True

def get_random_position(d):
    return [random.randint(2, d-3), random.randint(2, d*2-3)]

def get_random_direction():
    return random.choice([[-1, 0], [1, 0], [0, -1], [0, 1]])

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def getPlayerDirections(stdscr):
    global p1_dir, p2_dir
    key = stdscr.getch()
    
    # Player 1 (WASD)
    if key == ord('w') and p1_dir != [1, 0]:
        p1_dir = [-1, 0]
    elif key == ord('s') and p1_dir != [-1, 0]:
        p1_dir = [1, 0]
    elif key == ord('a') and p1_dir != [0, 1]:
        p1_dir = [0, -1]
    elif key == ord('d') and p1_dir != [0, -1]:
        p1_dir = [0, 1]
    
    # Player 2 (Arrow keys)
    elif key == curses.KEY_UP and p2_dir != [1, 0]:
        p2_dir = [-1, 0]
    elif key == curses.KEY_DOWN and p2_dir != [-1, 0]:
        p2_dir = [1, 0]
    elif key == curses.KEY_LEFT and p2_dir != [0, 1]:
        p2_dir = [0, -1]
    elif key == curses.KEY_RIGHT and p2_dir != [0, -1]:
        p2_dir = [0, 1]

def movePlayers(d):
    global p1_pos, p2_pos, frame, playing
    
    new_p1_pos = [p1_pos[0] + p1_dir[0], p1_pos[1] + p1_dir[1]]
    new_p2_pos = [p2_pos[0] + p2_dir[0], p2_pos[1] + p2_dir[1]]
    
    # Check collisions
    p1_valid = is_valid_move(new_p1_pos, d)
    p2_valid = is_valid_move(new_p2_pos, d)
    
    if not p1_valid and not p2_valid:
        playing = False
        return "Draw"
    elif not p1_valid:
        playing = False
        return "Player 2 Wins"
    elif not p2_valid:
        playing = False
        return "Player 1 Wins"
    
    # Move players
    frame[new_p1_pos[0]][new_p1_pos[1]] = 'p1'
    frame[new_p2_pos[0]][new_p2_pos[1]] = 'p2'
    p1_pos = new_p1_pos
    p2_pos = new_p2_pos
    return None

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
    stdscr.addch(p1_pos[0], p1_pos[1], '&', curses.color_pair(1))
    stdscr.addch(p2_pos[0], p2_pos[1], '@', curses.color_pair(2))

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