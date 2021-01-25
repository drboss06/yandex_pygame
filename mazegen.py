from typing import List
from collections import deque
from random import choice


def generate(length: int, width: int) -> List[str]:
    if not length % 2 or not width % 2:
        raise ValueError("Length and width of maze must be odd, not even")

    maze = [["1"] * length for _ in range(width)]

    maze[1][1] = '0'
    q = deque([(1, 1)])

    while q:
        x, y = q.pop()
        maze[y][x] = '0'

        near = [(x1, y1, *_) for x1, y1, *_ in (
                (x + 2, y, x + 1, y), (x, y + 2, x, y + 1),
                (x - 2, y, x - 1, y), (x, y - 2, x, y - 1))
                if 0 < x1 < length - 1 and 0 < y1 < width - 1 and maze[y1][x1] == '1']

        if near:
            q.append((x, y))

            x1, y1, x2, y2 = choice(near)
            maze[y2][x2] = '0'

            q.append((x1, y1))

    return list(map("".join, maze))


if __name__ == "__main__":
    print(*generate(int(input("Length: ")), int(input("Width: "))), sep='\n')
    print()