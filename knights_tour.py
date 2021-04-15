class Knight:
    def __init__(self):
        self.dimension = [0, 0]
        self.current_position = [0, 0]
        self.cell_size = None
        self.board = None
        self.X_sign = None
        self.visited_mark = None
        self.border = None
        self.total_moves = 0
        self.available_moves = 0
        self.puzzle = True
        self.result = None
        self.answer = None
        self.possible_moves = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        self.valid_moves = []

    def dimension_input(self):
        while True:
            try:
                x, y = [int(num) for num in input('Enter your board dimensions: ').split()]
                if x <= 0 or y <= 0:
                    print('Invalid position!')
                else:
                    self.cell_size = len(str(x * y))
                    self.dimension[0] = x
                    self.dimension[1] = y
                    break
            except ValueError:
                print('Invalid position!')

    def starting_position_input(self):
        while True:
            try:
                x, y = [int(num) for num in input("Enter the knight's starting position: ").split()]
                if x <= 0 or y <= 0 or x > self.dimension[0] or y > self.dimension[1]:
                    print('Invalid position!')
                else:
                    self.update_position(x, y)
                    break
            except ValueError:
                print('Invalid position!')

    def next_move_input(self):
        while True:
            try:
                x, y = [int(num) for num in input('Enter your next move: ').split()]
                mx = x - 1
                my = self.dimension[1] - y
                if (x <= 0 or y <= 0 or x > self.dimension[0] or y > self.dimension[1] or
                        [mx, my] == self.current_position or
                        self.board[my][mx] == self.visited_mark or [mx, my] not in self.valid_moves):
                    print('Invalid move! ', end='')
                else:
                    self.board[self.current_position[1]][self.current_position[0]] = self.visited_mark
                    self.clean_moves()
                    self.update_position(x, y)
                    break
            except ValueError:
                print('Invalid move! ', end='')

    def try_puzzle(self):
        while True:
            self.answer = input('Do you want to try the puzzle? (y/n): ')
            if self.answer == 'y' or self.answer == 'n':
                break
            else:
                print('Invalid input!')
        self.solve()

    def create_data(self):
        self.board = [[('_' * self.cell_size) for _ in range(self.dimension[0])] for _ in range(self.dimension[1])]
        self.X_sign = (' ' * (self.cell_size - 1)) + 'X'
        self.visited_mark = (' ' * (self.cell_size - 1)) + '*'
        self.border = '-' * (self.dimension[0] * (self.cell_size + 1) + 3)

    def display(self):
        cell = ' '
        adjust_space = ' '
        if self.cell_size > 3:
            adjust_space = adjust_space * (self.cell_size - 2)

        print(f' {self.border}')
        print(*[f'{cell * (self.cell_size - len(str(self.dimension[1] - i))) + str(self.dimension[1] - i)}| '
                + ' '.join(self.board[i])
                + ' |' for i in range(self.dimension[1])], sep='\n')
        print(f' {self.border}')
        print(' ' * (len(str(self.dimension[0])) + 1),
              *[cell * (len(str(self.dimension[0])) - len(str(i)))
                + f'{adjust_space + str(i)}'
                for i in range(1, self.dimension[0] + 1)])
        print()

    def mark_position(self):
        self.board[self.current_position[1]][self.current_position[0]] = self.X_sign

    def update_position(self, x, y):
        self.current_position[0] = x - 1
        self.current_position[1] = self.dimension[1] - y
        self.total_moves += 1

    def check_moves(self, cx, cy):
        counter = 0
        for x, y in self.possible_moves:
            px = cx + x
            py = cy + y
            if (px < 0 or py < 0 or px >= self.dimension[0] or
                    py >= self.dimension[1] or [px, py] == self.current_position or
                    self.board[py][px] == self.visited_mark):
                continue
            else:
                counter += 1

        self.board[cy][cx] = (' ' * (self.cell_size - 1)) + str(counter)

    def clean_moves(self):
        for move in self.valid_moves:
            self.board[move[1]][move[0]] = '_' * self.cell_size
        self.valid_moves = []

    def moves(self):
        for x, y in self.possible_moves:
            tx = self.current_position[0] + x
            ty = self.current_position[1] + y

            if (tx < 0 or ty < 0 or tx >= self.dimension[0] or
                    ty >= self.dimension[1] or self.board[ty][tx] == self.visited_mark):
                pass
            else:
                if self.available_moves == 0:
                    self.available_moves += 1
                self.valid_moves.append([tx, ty])
                self.check_moves(tx, ty)

    def examine_board(self):
        if self.total_moves == self.dimension[0] * self.dimension[1]:
            print('What a great tour! Congratulations!')
            self.puzzle = False
        elif self.available_moves == 0:
            print(f'No more possible moves!\nYour knight visited {self.total_moves} squares!')
            self.puzzle = False
        else:
            self.available_moves = 0

    def solve(self):
        self.board[self.current_position[1]][self.current_position[0]] = (' ' * (self.cell_size - 1)) + str(1)
        # pos = 2
        # if not self.solve_backtracking(self.board, self.current_position[0], self.current_position[1], pos):
        if not self.solve_warnsdorff():
            print('No solution exists!')
            return
        else:
            self.result = True
        self.start_game()

    def solve_backtracking(self, board, cx, cy, pos):
        if pos == self.dimension[0] * self.dimension[1] + 1:
            return True

        for x, y in self.possible_moves:
            nx = cx + x
            ny = cy + y
            if self.is_valid(nx, ny, board):
                board[ny][nx] = (' ' * (self.cell_size - len(str(pos)))) + str(pos)
                if self.solve_backtracking(board, nx, ny, pos + 1):
                    return True

                board[ny][nx] = '_' * self.cell_size
        return False

    def is_valid(self, x, y, board):
        if 0 <= x < self.dimension[0] and 0 <= y < self.dimension[1] and board[y][x] == '_' * self.cell_size:
            return True
        return False

    def solve_warnsdorff(self):
        counter = 2
        x = self.current_position[0]
        y = self.current_position[1]
        n = (self.dimension[0] * self.dimension[1]) - 1
        for _ in range(n):
            pos = self.get_moves(x, y)
            if not pos:
                return False
            x, y = x + pos[0][0], y + pos[0][1]
            self.board[y][x] = (' ' * (self.cell_size - len(str(counter)))) + str(counter)
            counter += 1
        return True

    def find_moves(self, x, y):
        return [(i, j) for i, j in self.possible_moves if self.is_valid(x + i, y + j, self.board)]

    def get_moves(self, x, y):
        moves = self.find_moves(x, y)
        next_moves = [(len(self.find_moves(x + i, y + j)), i, j) for i, j in moves]
        return [(n[1], n[2]) for n in sorted(next_moves)]

    def show_result(self):
        if self.answer == 'n' and self.result:
            print("Here's the solution!")
            self.display()
            return True
        return False

    def initialize(self):
        self.dimension_input()
        self.create_data()
        self.starting_position_input()
        self.try_puzzle()

    def start_game(self):
        if self.show_result():
            return
        self.create_data()
        self.mark_position()
        self.moves()
        self.display()
        self.available_moves = 0
        self.puzzle_start()

    def puzzle_start(self):
        while self.puzzle:
            self.next_move_input()
            self.mark_position()
            self.moves()
            self.display()
            self.examine_board()


k = Knight()
k.initialize()
