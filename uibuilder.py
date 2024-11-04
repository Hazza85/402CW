class Frame:
    def __init__(self, rows, cols, frame_number):
        self.frame_number: int = frame_number
        self.rows = rows
        self.cols = cols
        print(f"A ({rows}x{cols}) frame, ID: {self.frame_number}, created.")

        self.grid: [int, int] = [['.' for _ in range(cols)] for _ in range(rows)]  # '.' are empty spaces.
        self.button: [(int, int), int] = {}  # [(y, x), grid];

    # Used to display the grid
    def display(self):
        print(f"Frame ID: {self.frame_number} ")
        for row in self.grid:
            print(' '.join(row))
        print("")

    def set_button(self, row, col, target_frame) -> bool:
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
        # Adding prints here clutters the interface and makes it hard to follow.
        options = []
        for row in range(self.rows):

            row_options = []
            for col in range(self.cols):

                if self.can_set_button(row, col):
                    valid_targets = [i for i in range(len(all_frames)) if
                                     all_frames[i].can_set_button(row, col) and all_frames[i] != self]
                    row_options.append(valid_targets if valid_targets else ['.'])
                else:
                    row_options.append(['X'])

            options.append(row_options)
        return options


class FrameManager:
    def __init__(self):
        self.frames: list[Frame] = []
        # Having the frame number and the index not equal to each other makes the code hard to read.
        self.frame_number = -1

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
        self.display_frames()

        from_frame = int(input("From frame: "))

        print(f"Positions in Frame {from_frame}:")
        options = self.frames[from_frame].available_positions(self.frames)

        for row in range(self.frames[from_frame].rows):
            row_options = []

            for col in range(self.frames[from_frame].cols):
                if options[row][col] != ['.']:
                    row_options.append(f"[{', '.join(map(str, options[row][col]))}]")
                else:
                    row_options.append('.')
            print(' '.join(row_options))

        print(f"To frame (excluding {from_frame}):")
        for i, frame in enumerate(self.frames):
            if frame != from_frame: print(f"{i}. Frame {frame}")

        to_frame = int(input("To frame: "))
        row = int(input("Row for button: "))
        col = int(input("Col for button: "))

        # Checks if the button can even be put onto the source frame.
        if row <= self.frames[from_frame].rows - 1 or col <= self.frames[from_frame].cols - 1:
            # Check which of the two frames is bigger.
            if self.frames[from_frame].rows > self.frames[to_frame].rows or self.frames[from_frame].cols > self.frames[to_frame].cols:
                self.frames[from_frame].set_button(row, col, to_frame)
                if row < self.frames[to_frame].rows or col < self.frames[to_frame].cols:
                    self.frames[to_frame].set_button(row, col, from_frame)
            else:
                self.frames[from_frame].set_button(row, col, to_frame)
                self.frames[to_frame].set_button(row, col, from_frame)
        else:
            print("Outside of limits etc... ")

        # This checks for the dependencies on all frames for each button.
        for i, frame in enumerate(self.frames):
            # List allows for: RuntimeError: dictionary changed size during iteration
            for coords in list(frame.button):
                if frame.button[coords] != "X":
                    for inner_coords in list(self.frames[frame.button[coords]].button):
                        try:
                            if frame.grid[inner_coords[0]][inner_coords[1]] == '.':
                                frame.set_button(*inner_coords, 'X')
                        except Exception as e:
                            print("")
                            pass
                        pass

    def display_frames(self):
        for i, frame in enumerate(self.frames):
            frame.display()


def main() -> None:
    frame_manager = FrameManager()

    while True:
        print('''
Menu: 
1. New Frame 
2. Set Button 
3. Display Frames 
4. Exit
        ''')

        choice = input("Choice: ")

        if choice == '1':
            frame_manager.create_frame()
        elif choice == '2':
            frame_manager.set_button()
        elif choice == '3':
            print("Displaying all frames: ")
            frame_manager.display_frames()
        elif choice == '4':
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

