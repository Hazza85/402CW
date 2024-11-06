from xmlrpc.client import MAXINT


class Frame:
    """Represents a grid-based frame with rows and columns, where links can be added to connect frames.

    Attributes:
        frame_number (int): Unique identifier for the frame.
        rows (int): Number of rows in the frame grid.
        cols (int): Number of columns in the frame grid.
        grid (list[list[str]]): 2D list representing the grid, initialized with '.' for empty spaces.
        links (dict[tuple[int, int], str]): Dictionary to store links, with grid positions as keys and target frame symbols as values.

    Key Symbols:
        X <- Location blocked, you cannot place a link there.
        Number aka frame_number <- Indicates which other frame the link points to.
    """

    def __init__(self, rows, cols, frame_number):
        """Initializes a frame with the specified dimensions and frame number.

        Args:
            rows (int): Number of rows in the frame grid.
            cols (int): Number of columns in the frame grid.
            frame_number (int): Unique identifier for this frame.
        """
        self.frame_number: int = frame_number
        self.rows = rows
        self.cols = cols
        print(f"A ({rows}x{cols}) frame, ID: {self.frame_number}, created.")

        # Initialize grid with '.' for empty spaces.
        self.grid: [int, int] = [['.' for _ in range(cols)] for _ in range(rows)]
        self.links: {(int, int): str} = {}  # Dictionary to store links with positions and target frame symbols

    def display(self):
        """Used to visualize the grid.
        TODO: Return Json so it can be used else where...
        """
        print(f"Frame ID: {self.frame_number} ")
        for row in self.grid:
            print(' '.join(row))
        print("")

    def set_link(self, row, col, target_frame) -> bool:
        """Sets a link on the grid pointing to the target frame.

        Args:
            row (int): The row index where the link is to be placed.
            col (int): The column index where the link is to be placed.
            target_frame (str): The ID of the frame this link points to or 'X' if blocked.

        Returns:
            bool: True if the link was successfully set, False if the position is already occupied.

        Notes:
            You are passing the number representing the target frame and not the actual reference to it.
        """
        # Check if the position is empty
        if self.grid[row][col] == '.':
            # Place target frame ID as a string for consistency
            self.grid[row][col] = str(target_frame)
            self.links[(row, col)] = str(target_frame)

            print(f"Link placed from: Frame {self.frame_number} to Frame {target_frame} at ({row}, {col}).")
            return True
        print(f"Frame: {target_frame} at ({row}, {col}) occupied.")
        return False


class FrameManager:
    """Manages multiple frames and provides methods to create, display, and link frames.

    Attributes:
        frames (list[Frame]): List of all frames managed by this FrameManager.
        frame_number (int): Counter for assigning unique IDs to new frames.
    """

    def __init__(self):
        """Initializes an empty FrameManager with a frame counter set to zero."""
        self.frames: list[Frame] = []
        # Starting at 0 keeps the index and the frame_number the same
        self.frame_number = 0

    def display_frames(self, block=MAXINT):
        """Displays all frames, excluding a specified frame if needed.

        Args:
            block (int, optional): ID of the frame to exclude from display. Defaults to MAXINT, showing all frames.
        """
        # Loop through frames to display each unless it matches the block
        for frame in self.frames:
            if frame.frame_number != block:
                frame.display()

    def add_frame(self, rows: int, cols: int) -> Frame:
        """Creates and adds a new frame with the specified dimensions.

        Args:
            rows (int): Number of rows for the new frame.
            cols (int): Number of columns for the new frame.

        Returns:
            Frame: The newly created frame.
        """
        # Create a new frame with unique frame_number
        frame = Frame(rows, cols, self.frame_number)
        self.frames.append(frame)
        self.frame_number += 1  # Increment frame_number for next frame
        return frame

    def set_link_logic(self, row, col, from_frame, to_frame):
        """Sets bidirectional links between two frames at a specified grid position.

        Args:
            row (int): Row index in the grid for the link.
            col (int): Column index in the grid for the link.
            from_frame (int): ID of the source frame.
            to_frame (int): ID of the target frame.

        Notes:
            Ensures links are only set if the positions are free, and links are added in both directions.
        """
        # Check if a link already exists at the specified row and col
        for link in self.frames[to_frame].links:
            for link_row, link_col in link:
                if link_row == row and link_col == col:
                    return
        # Set links twice for bi-directionality
        self.frames[from_frame].set_link(row, col, target_frame=to_frame)
        self.frames[to_frame].set_link(row, col, target_frame=from_frame)

    def check_placement_options(self, from_frame):
        """Displays available placement options for links in a specified frame, excluding occupied positions.

        Args:
            from_frame (int): ID of the frame for which placement options are to be checked.

        Notes:
            Loops through all frames except the current one, checking squares for exclusivity and occupied spaces.
            This method outputs placement options in a grid format.
            TODO: Return Json so it can be used else where...
        """
        print(f"\nPlacement Options for Frame {from_frame}:")

        # Creates where the available slots will be saved
        all_frames = [str(i) for i in range(len(self.frames)) if i != from_frame]
        placement_grid = [[all_frames.copy() for _ in range(self.frames[from_frame].cols)]
                          for _ in range(self.frames[from_frame].rows)]

        # Loops through all frames except itself
        for to_frame in range(len(self.frames)):
            if to_frame == from_frame: continue

            # Check for exclusivity by inspecting links and adjusting grid
            for (link_row, link_col) in self.frames[to_frame].links.keys():
                if link_row < self.frames[from_frame].rows and link_col < self.frames[from_frame].cols:
                    if str(to_frame) in placement_grid[link_row][link_col]:
                        placement_grid[link_row][link_col].remove(str(to_frame))

            # Check for occupied squares
            for row in range(self.frames[from_frame].rows):
                for col in range(self.frames[from_frame].cols):
                    if self.frames[to_frame].grid[row][col] != '.':
                        if str(to_frame) in placement_grid[row][col]:
                            placement_grid[row][col].remove(str(to_frame))

        # Print the spaces that are available as a formatted grid
        for row in placement_grid:
            print(" | ".join([", ".join(cell) if cell else "X" for cell in row]))


class FrameManagerInterface:
    """Interface class for interacting with FrameManager in a command-line menu.

    Attributes:
        frame_manager (FrameManager): Instance of FrameManager for managing frames and links.
    """

    def __init__(self):
        """Initializes the FrameManagerInterface with a new FrameManager instance."""
        self.frame_manager = FrameManager()

    def run(self):
        """Runs the main menu loop for frame management."""
        while True:
            print('''
            
Menu: 
1. New Frame 
2. Set Link 
3. Display Frames 
4. Exit

            ''')
            choice = input("Choice: ")
            if choice == '1':
                self.add_new_frame()
            elif choice == '2':
                self.set_link()
            elif choice == '3':
                self.display_all_frames()
            elif choice == '4':
                self.exit_program()
                break
            else:
                print("Invalid choice.")

    def add_new_frame(self):
        """Prompts the user to enter dimensions and adds a new frame to the FrameManager."""
        # Prompting user for frame dimensions
        rows = int(input("Number of Rows? "))
        cols = int(input("Number of Columns? "))

        # Validate dimensions to be greater than 0
        if rows > 0 and cols > 0:
            self.frame_manager.add_frame(rows, cols)
            print("Frame added successfully.")
        else:
            print("Invalid dimensions; rows and columns must be greater than 0.")

    def set_link(self):
        """Allows the user to set a bidirectional link between two frames."""
        # Display all frames first so user can decide on link positions
        self.display_all_frames()

        try:
            # Selecting frames and grid positions
            from_frame = int(input("From frame: "))

            # Show the frames you can choose from
            print(f"Frames (excluding {from_frame}):")
            self.frame_manager.check_placement_options(from_frame)

            to_frame = int(input("To frame: "))
            row = int(input("Row (from 0) for link: "))
            col = int(input("Col (from 0) for link: "))
            self.frame_manager.set_link_logic(row=row, col=col, from_frame=from_frame, to_frame=to_frame)

            print("Link set successfully.")

        except ValueError:
            print("Invalid input. Please enter integers for frame numbers and grid positions.")

        except IndexError:
            print("Error: Row or column out of bounds.")

        except Exception as e:
            print(f"Error: {e}")

    def display_all_frames(self):
        """Displays all frames using the FrameManager's display function."""
        print("Displaying all frames:")
        self.frame_manager.display_frames()

    @staticmethod
    def exit_program():
        """Handles the exit procedure for the FrameManagerInterface."""
        print("Exiting program. Goodbye!")


# Only runs the interface if the script is executed directly
if __name__ == "__main__":
    # Initialize the interface and run the main menu loop
    FrameManagerInterface().run()
