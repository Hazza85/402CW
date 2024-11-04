class Frame:
    def __init__(self, rows, cols, frame_number):
        self.frame_number = frame_number
        self.rows = rows
        self.cols = cols
        print(f"A ({rows}x{cols}) frame, ID: {self.frame_number}, created.")

        # TODO: The grid Var doesn't need to be here if we have self.button, but removing it takes time and doesn't help with anything...
        self.grid: [int, int] = [['.' for _ in range(cols)] for _ in range(rows)]  # '.' are empty spaces.
        self.button: [(int, int), int] = {}  # [(y, x), grid];

    # Used to display the grid,
    def display(self):
        print(f"Frame ID: {self.frame_number}... ")
        for row in self.grid:
            print(' '.join(row))
        # '\n' <- I have a 60% keyboard I don't have a '\' that I can use; do NOT delete this comment.
        print('\n')

    def set_button(self, row, col, target_frame: int) -> bool:
        # You are passing the number representing the target frame and not the actual reference to it.
        if self.grid[row][col] == '.':
            self.grid[row][col] = str(target_frame)
            self.button[(row, col)] = target_frame

            print(f"Button placed from: Frame {self.frame_number} to Frame {target_frame} at ({row}, {col}).")
            return True
        print(f"Frame: {target_frame} at ({row}, {col}) occupied.")
        return False

    # This checks if the grid location is of '.'.
    def can_set_button(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] == '.'

    def available_positions(self, all_frames: list) -> list:
        options: list = []
        for row in range(self.rows):

            row_options: list = []
            for col in range(self.cols):

                if self.can_set_button(row, col):
                    # This grabs the frame numbers of those that can be put in certain squares on the grid.
                    valid_targets = [i + 1 for i in range(len(all_frames)) if
                                     all_frames[i].can_set_button(row, col) and all_frames[i] != self]
                    row_options.append(valid_targets if valid_targets else ['.'])
                else:
                    # This is when there already a button on the FROM frames square, avoids excess compute.
                    row_options.append(['X'])  # TODO: This shouldn't be '.' for clarity.

            options.append(row_options)
        return options


class FrameManager:
    def __init__(self):
        self.frames: list[Frame] = []
        self.frame_number = 0  # Logic from before the frames knew what number they were, so do NOT change this to -1.

    def frame_number_next(self):
        self.frame_number += 1
        return self.frame_number

    def create_frame(self) -> None:
        while True:
            try:
                rows = int(input("no of Rows? "))
                cols = int(input("no of Columns? "))
                if rows > 0 and cols > 0:
                    frame = Frame(rows, cols, self.frame_number_next())
                    self.frames.append(frame)
                    break
            except ValueError:
                print("Invalid input. Please enter integers.")

    def set_button(self) -> None:
        print("Available frames:")
        for i, frame in enumerate(self.frames):
            print(f"{i + 1}. Frame {i + 1}")

        from_frame_index = int(input("From frame: "))

        print(f"Positions in Frame {from_frame_index + 1}:")
        options = self.frames[from_frame_index].available_positions(self.frames)
        for row in range(self.frames[from_frame_index].rows):
            output_row = []
            for col in range(self.frames[from_frame_index].cols):
                if options[row][col] != ['.']:
                    output_row.append(f"[{', '.join(map(str, options[row][col]))}]")
                else:
                    output_row.append('.')
            print(' '.join(output_row))

        print(f"To frame (excluding {from_frame_index + 1}):")
        to_frame_indices: list[int] = [i for i in range(len(self.frames)) if i != from_frame_index]
        for i in to_frame_indices:
            print(f"{i + 1}. Frame {i + 1}")

        to_frame_index = int(input("To frame: "))
        row = int(input("Row for button: "))
        col = int(input("Col for button: "))

        if self.frames[from_frame_index].can_set_button(row, col):
            if self.frames[to_frame_index].can_set_button(row, col):
                if self.frames[from_frame_index].set_button(row, col, to_frame_index + 1):
                    self.frames[to_frame_index].set_button(row, col, from_frame_index + 1)
        else:
            print("cannot set button here. ")

    def display_frames(self):
        print("Displaying all frames: ")
        for i, frame in enumerate(self.frames): frame.display()


def main() -> None:
    frame_manager = FrameManager()

    while True:
        print('''
Menu: 
1. New Frame 
2. Set Portal 
3. Display Frames 
4. Exit
        ''')
        choice = input("Choice: ")

        if choice == '1':
            frame_manager.create_frame()
        elif choice == '2':
            frame_manager.set_button()
        elif choice == '3':
            frame_manager.display_frames()
        elif choice == '4':
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()


''' Notes:
I used to call them portals; transition to calling them buttons.
'''
