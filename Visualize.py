import tkinter as tk

class Pointer:
    def __init__(self, initial_x=0, initial_y=0, diameter=50, color='red'):
        # Create a transparent window
        self.window = tk.Tk()
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.attributes('-transparentcolor', self.window['bg'])
        self.window.attributes('-topmost', True)  # Keep window on top

        # Initial settings
        self.diameter = diameter
        self.color = color

        # Create canvas and dot
        self.canvas = tk.Canvas(self.window, width=self.diameter, height=self.diameter, 
                                highlightthickness=0, bd=0)
        self.dot = self.canvas.create_oval(0, 0, self.diameter, self.diameter, 
                                           fill=self.color, outline=self.color)
        self.canvas.pack()
        self.Xpos = initial_x
        self.Ypos = initial_y
        self.gotoXY(initial_x, initial_y)

    def gotoXY(self, x, y):
        self.window.geometry(f"+{x}+{y}")

    def tick(self):
        self.gotoXY(self.Xpos, self.Ypos)

    def hide(self):
        self.window.withdraw()

    def show(self):
        self.window.deiconify()

    def change_diameter(self, new_diameter):
        self.diameter = new_diameter
        self.canvas.config(width=self.diameter, height=self.diameter)
        self.canvas.coords(self.dot, 0, 0, self.diameter, self.diameter)

    def change_color(self, new_color):
        self.color = new_color
        self.canvas.itemconfig(self.dot, fill=self.color, outline=self.color)

if __name__ == "__main__":
    # Create a pointer
    pointer = Pointer(initial_x=783, initial_y=1183, diameter=20)

    # Keep the window open
    tk.mainloop()