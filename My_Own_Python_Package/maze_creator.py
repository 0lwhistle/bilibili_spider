import random

def chioce_random_direction(direction):
    return random.choice(direction)

def all_directions_known(current_position, known, odds_w, odds_h):
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    for direction in directions:
        next_position = [current_position[0] + direction[0] * 2, current_position[1] + direction[1] * 2]
        if next_position[0] in odds_w and next_position[1] in odds_h:
            if not next_position in known:
                return False
    return True

def not_done(known, odds_w, odds_h):
    for i in odds_w:
        for j in odds_h:
            if (i, j) not in known:
                return True
    return False

def get_next_position(current_position, direction):
    return [current_position[0] + direction[0] * 2, current_position[1] + direction[1] * 2]
def create_maze(width, height):

    maze = [[0 for x in range(width)] for y in range(height)]

    maze[1][0] = 1
    maze[height-2][width-1] = 1

    stack = []
    known = []
    wall_down = []
    known.append([1, 0])
    known.append([1, 1])
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    odds_w = []
    odds_h = []
    for i in range(width):
        if i % 2 != 0 and i != 0 and i != width-1:
            odds_w.append(i)
    #print("odds", odds)

    for i in range(height):
        if i % 2 != 0 and i != 0 and i != height-1:
            odds_h.append(i)

    for i in odds_h:
        for j in odds_w:
            maze[i][j] = 1

    for row in maze:
        for cell in row:
            if cell == 1:
                print("@ ", end="")
            else:
                print("# ", end="")
        print()

    current_position = [1, 1]

    while not_done(known, odds_h, odds_w):
        # print(1)
        direction = chioce_random_direction(directions)
        next_position = get_next_position(current_position, direction)
        while (not next_position[0] in odds_h or not next_position[1] in odds_w):
            print(2)
            # print("current_position", current_position)
            # print("next_position", next_position)
            # print("direction", direction)
            # for row in maze:
            #     for cell in row:
            #         if cell == 1:
            #             print("@ ", end="")
            #         if cell == 2:
            #             print("@ ", end="")
            #         if cell == 0:
            #             print("# ", end="")
            #     print()
            direction = chioce_random_direction(directions)
            next_position = [current_position[0] + direction[0] * 2, current_position[1] + direction[1] * 2]


        if not next_position in known:
            stack.append(next_position)
            known.append(next_position)

            print("current_position", current_position)
            print("next_position", next_position)
            print("direction", direction)
            print(f"Have known{len(known)}", known)
            print(f"Have stack{len(stack)}", stack)
            print("wall_down", current_position[0] + direction[0], current_position[1] + direction[1])
            for row in maze:
                for cell in row:
                    if cell == 1:
                        print("@ ", end="")
                    if cell == 2:
                        print("@ ", end="")
                    if cell == 0:
                        print("# ", end="")
                print()

            # print(f"{current_position}current_position ->", next_position)
            maze[current_position[0] + direction[0]][current_position[1] + direction[1]] = 1
            wall_down.append([current_position[0] + direction[0], current_position[1] + direction[1]])
            current_position = next_position

        elif all_directions_known(current_position, known, odds_h, odds_w):
            # print(3)
            if len(stack) > 0:
                current_position = stack.pop()
            else:
                break
    maze[current_position[0]][current_position[1]] = 4
    return maze


if __name__ == '__main__':
    maze = create_maze(5, 7)
    for row in maze:
        print(row)

