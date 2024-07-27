import tkinter as tk
import time

def create_red_dot():
    # Create a transparent window
    window = tk.Tk()
    window.overrideredirect(True)  # Remove window decorations

    # Make the window transparent and always on top
    window.attributes('-transparentcolor', window['bg'])
    window.attributes('-topmost', True)  # Keep window on top

    # Create a canvas to draw the red dot
    diameter = 50
    canvas = tk.Canvas(window, width=diameter, height=diameter, highlightthickness=0)
    canvas.pack()

    # Draw a red circle in the middle of the canvas
    canvas.create_oval(0, 0, diameter, diameter, fill='red', outline='red')

    return window, canvas

def move_red_dot(window, start_x, start_y, end_x, increment=10):
    y = start_y
    for x in range(start_x, end_x + 1, increment):
        window.geometry(f"+{x}+{y}")
        window.update()
        time.sleep(0.05)  # adjust the speed of movement

# Initial position and target position
start_pos_x = 0
pos_y = 100
end_pos_x = 300

# Create and display the dot
dot_window, dot_canvas = create_red_dot()
move_red_dot(dot_window, start_pos_x, pos_y, end_pos_x)

while True:
    1+1

#dot_window.mainloop()9