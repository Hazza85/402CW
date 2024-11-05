from xmlrpc.client import MAXINT


class Frame:
    def __init__(self, rows, cols, frame_number):
        # frame number isn't needed, but it's very convenient for things.
        self.frame_number: int = frame_number
        self.rows = rows
        self.cols = cols
        print(f"A ({rows}x{cols}) frame, ID: {self.frame_number}, created.")

        self.grid: [int, int] = [['.' for _ in range(cols)] for _ in range(rows)]  # '.' are empty spaces.
        self.links: [(int, int), str] = {}  # [(y, x), to_frame / key symbol];

        # Key Symbols:
        # X <- Location blocked, you cannot place a button there.

    def display(self):
        """
        Used to visualize the grid.
        """
        print(f"Frame ID: {self.frame_number} ")
        for row in self.grid:
            print(' '.join(row))
        print("")

    def set_link(self, row, col, target_frame) -> bool:
        """
        sets a button on the grid pointing to the target frame.

        Args:
            row (int): The row index where the button is to be placed.
            col (int): The column index where the button is to be placed.
            target_frame (str): The ID of the frame this button points to or X if blocked.

        Returns:
            bool: True if the button was successfully set, False if the position is already occupied.

        Notes:
            You are passing the number representing the target frame and not the actual reference to it.
        """
        if self.grid[row][col] == '.':
            self.grid[row][col] = str(target_frame)
            # Store target frame ID as a string for consistency, it's usually treated as a String.
            self.links[(row, col)] = str(target_frame)

            print(f"Button placed from: Frame {self.frame_number} to Frame {target_frame} at ({row}, {col}).")
            return True
        print(f"Frame: {target_frame} at ({row}, {col}) occupied.")
        return False


# To figure out where what goes; if you need to call all grids then in frameManager, else: others
class FrameManager:
    def __init__(self):
        self.frames: list[Frame] = []
        # Starting at 0 keeps the index and the frame_number the same.
        self.frame_number = 0

    def display_frames(self, block=MAXINT):
        for frame in self.frames:
            if frame.frame_number != block:
                print(f'{frame.display()}')

    def set_link_logic(self, row, col, from_frame, to_frame):
        for link in self.frames[to_frame].links:
            for link_row, link_col in link:
                if link_row == row and link_col == col:
                    return
        # Set buttons, twice for bi-directionality
        self.frames[from_frame].set_link(row, col, target_frame=to_frame)
        self.frames[to_frame].set_link(row, col, target_frame=from_frame)

    def check_placement_options(self, from_frame):
        print(f"\nPlacement Options for Frame {from_frame}:")

        # Creates where the available slots will be saved.
        all_frames = [str(i) for i in range(len(self.frames)) if i != from_frame]
        placement_grid = [[all_frames.copy() for _ in range(self.frames[from_frame].cols)]
                          for _ in range(self.frames[from_frame].rows)]

        # Loops through all frames but itself.
        for to_frame in range(len(self.frames)):
            if to_frame == from_frame: continue

            # These are probably the most computationally expensive parts.
            # Checks squares for exclusivity rule...
            for (link_row, link_col) in self.frames[to_frame].links.keys():
                if link_row < self.frames[from_frame].rows and link_col < self.frames[from_frame].cols:
                    # Error check to make sure the item you're removing is there.
                    if str(to_frame) in placement_grid[link_row][link_col]:
                        placement_grid[link_row][link_col].remove(str(to_frame))

            # Checks for occupied squares...
            for row in range(self.frames[from_frame].rows):
                for col in range(self.frames[from_frame].cols):
                    # This could be changed to look at links instead of looking at '.'.
                    if self.frames[to_frame].grid[row][col] != '.':
                        # Error check to make sure the item you're removing is there.
                        if str(to_frame) in placement_grid[row][col]:
                            placement_grid[row][col].remove(str(to_frame))

        # Print out the spaces that are available
        # TODO: Make it output as JSON.
        for row in placement_grid:
            print(" | ".join([", ".join(cell) if cell else "X" for cell in row]))


if __name__ == "__main__":
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
        go = True
        if choice == '1':
            while go:
                rows = int(input("no of Rows? "))
                cols = int(input("no of Columns? "))
                if rows > 0 and cols > 0:
                    frame_manager.frames.append(Frame(rows, cols, frame_manager.frame_number))
                    frame_manager.frame_number += 1
                    break

        elif choice == '2':
            frame_manager.display_frames()

            from_frame = int(input("From frame: "))

            print(f"Frames: (excluding {from_frame}):")
            frame_manager.check_placement_options(from_frame)
            to_frame = int(input("To frame: "))

            try:
                frame_manager.set_link_logic(row=int(input("Row (from 0) for button: ")),
                                             col=int(input("Col (from 0) for button: ")),
                                             from_frame=from_frame, to_frame=to_frame)
            except Exception as e:
                print(e)
                pass

        elif choice == '3':
            print("Displaying all frames: ")
            frame_manager.display_frames()

        elif choice == '4':
            go = False
            break

        else:
            print("Invalid choice.")
