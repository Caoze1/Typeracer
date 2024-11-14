import tkinter as tk
from tkinter import ttk
import pandas as pd
from random import randrange
import time



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Celeritas')
        self.configure(bg="gray20")
        self.iconbitmap('C:/Users/vikto/OneDrive/Bilder/Celeritas_Hastighet.ico')
        self.geometry("465x355+500+200")

        # Container to hold all frames
        container = tk.Frame(self, bg="gray20")
        container.grid()

        self.frames = {}

        for F in (StartPage, PlayPage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        frame.focus_set()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.configure(bg="gray20")
        self.controller = controller

        label = tk.Label(self, text="CELERITAS", font=("Comic Sans MS", 40), bg="gray20", fg="white")
        label.grid(row=0, column=0, padx=80, pady=10, sticky="nsew")

        p_button = tk.Button(self, text="Play", font=("Comic Sans MS", 20), command=self.play, bg="dark gray", fg="white")
        p_button.grid(row=1, column=0, padx=80, pady=10, sticky="nsew")

        s_button = tk.Button(self, text="Settings", font=("Comic Sans MS", 20), command=self.settings, bg="dark gray", fg="white")
        s_button.grid(row=2, column=0, padx=80, pady=10, sticky="nsew")


    def play(self):
        self.controller.frames["PlayPage"].fetch_quote()
        self.controller.frames["PlayPage"].new_quote()
        self.controller.frames["PlayPage"].reset_stopwatch()
        self.controller.show_frame("PlayPage")
        self.controller.frames["PlayPage"].start()


    def settings(self):
        self.controller.show_frame("SettingsPage")


class PlayPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="gray20")

        self.df = pd.read_csv("Elden Ring.csv")

        self.phrase = []
        self.correct = 0
        self.incorrect = 0
        self.word_count = 0

        # Create a Text widget to display the string
        self.text_widget = tk.Text(self, height=10, width=55, bg="dark gray", fg="black")
        self.text_widget.grid(row=3, column=0)

        # Stopwatch components
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False

        self.label = tk.Label(self, text="00:00.0", font=("Helvetica", 24), bg="gray20", fg="red")
        self.label.grid(row=0, column=0, pady=20)

        # win_button = tk.Button(self, text="win", command=self.finish, font=("Comic Sans MS", 14), bg="gray24", fg="white")
        # win_button.grid(row=1, column=0, padx=10)

        back_button = tk.Button(self, text="Back", command=self.back_to_start, font=("Comic Sans MS", 14), bg="gray24", fg="white", borderwidth=0)
        back_button.grid(row=2, column=0, pady=10)

        # read keys pressed
        self.bind('<KeyPress>', self.on_key_press)


    def back_to_start(self):
        self.running = False
        self.reset_stopwatch()
        self.controller.show_frame("StartPage")


    def update_time(self):
        if self.running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            self.display_time()
            self.after(50, self.update_time)


    def display_time(self):
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        tenths = int((self.elapsed_time * 10) % 10)
        time_string = f"{minutes:02}:{seconds:02}.{tenths}"
        self.label.config(text=time_string)


    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.update_time()

            # Create a Text widget to display the string
            self.text_widget.grid(row=3, column=0, padx=10)
            self.text_widget.insert(tk.END, self.quote)
            self.text_widget.config(state=tk.DISABLED)


    def end_screen(self, wpm):
        # Create the popup window
        popup = tk.Toplevel(self)
        popup.title("Finished")
        popup.iconbitmap('C:/Users/vikto/OneDrive/Bilder/Celeritas_Hastighet.ico')
        popup.configure(bg="gray20")
        popup.geometry("200x150+650+300")

        # Label inside the popup
        label = tk.Label(popup, bg="gray20", text=f"Time: {round(self.elapsed_time, 1)} s \nWPM: {round(wpm, 1)}", font=("Comic Sans MS", 12), fg="white")
        label.grid(row=0, column=0, pady=20, padx=53)

        # Close button for the popup
        close_button = tk.Button(popup, bg="gray24", fg="white", borderwidth=0, text="Close", command=popup.destroy, font=("Comic Sans MS", 14))
        close_button.grid(row=1, column=0, pady=10, padx=53)


    def finish(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False

            wpm = self.word_count / (self.elapsed_time // 60 + self.elapsed_time % 60 / 60)
            self.end_screen(wpm)


    def reset_stopwatch(self):
        self.running = False
        self.elapsed_time = 0
        self.start_time = 0
        self.display_time()


    def switch_df(self, new_df):
        self.df = pd.read_csv(new_df)


    def new_quote(self):
        self.text_widget.config(state=tk.NORMAL)  # Enable the widget
        self.text_widget.delete(1.0, tk.END)      # Clear the widget
        self.text_widget.insert(tk.END, self.quote)  # Insert the new quote
        self.text_widget.config(state=tk.DISABLED)
        self.correct = 0
        self.incorrect = 0
        self.phrase = []


    def fetch_quote(self):
        """fetches quote from df and makes a string and a list of it"""
        self.quote = self.df.iat[randrange(0, len(self.df)),1 ]

        self.quote_list = []
        for char in self.quote:
            self.quote_list.append(char)

        self.word_count = len(self.quote.split())


    def update_colors(self, color_ranges):
        """
        Updates the colors of the tags based on the new_color_ranges.

        text_widget: Tkinter Text widget
        color_ranges: A list of tuples where each tuple contains a start index, end index, and new color
        """
        self.text_widget.config(state=tk.NORMAL)
        for tag in self.text_widget.tag_names():
            self.text_widget.tag_delete(tag)  # Remove existing tags

        # Re-apply color tags with the new color ranges
        for start, end, color in color_ranges:
            tag_name = f"color_{start}_{end}"
            self.text_widget.tag_add(tag_name, f"1.0+{start}c", f"1.0+{end}c")
            self.text_widget.tag_config(tag_name, foreground=color)

        self.text_widget.config(state=tk.DISABLED)


    def on_key_press(self, event):

        key_pressed = event.keysym
        if self.running:
            if len(key_pressed) > 1:
                if key_pressed == 'period':
                    self.phrase.append('.')
                elif key_pressed == 'minus':
                    self.phrase.append('-')
                elif key_pressed == 'exclam':
                    self.phrase.append('!')
                elif key_pressed == 'space':
                    self.phrase.append(' ')
                elif key_pressed == 'apostrophe':
                    self.phrase.append('\'')
                elif key_pressed == 'comma':
                    self.phrase.append(',')
                elif key_pressed == 'question':
                    self.phrase.append('?')
                elif key_pressed == 'BackSpace':
                    self.phrase.pop()
                    if self.incorrect > 0:
                        self.incorrect -= 1
                    else:
                        self.correct -= 1
            else:
                self.phrase.append(key_pressed)

            # erase
            if key_pressed != 'BackSpace' and key_pressed != 'Shift_L' and key_pressed != 'Shift_R':
                if len(self.phrase) > 0:
                    if self.phrase[len(self.phrase)-1] == self.quote_list[len(self.phrase)-1] and self.incorrect == 0:
                        self.correct += 1
                    else:
                        self.incorrect += 1

            # color change on text
            color_ranges = [(0, self.correct, 'green'),
                            (self.correct, self.correct + self.incorrect, 'red')
                            ]

            self.update_colors(color_ranges)

            if self.correct == len(self.quote):
                self.finish()


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="gray20")

        label = tk.Label(self, text="Dataset:", bg="gray20", fg="white", borderwidth=0, font=("Comic Sans MS", 14))
        label.grid(row=1, column=1, pady=10)

        # Drop-down list (combobox)
        options = ["Elden Ring", "Counter Strike", "League of Legends", "Real people"]
        self.selected_option = tk.StringVar()
        dropdown = ttk.Combobox(self, textvariable=self.selected_option, values=options, state="readonly", font=("Comic Sans MS", 10))
        dropdown.grid(row=1, column=2, pady=10, padx=10)
        dropdown.current(0)  # Select the first option by default

        #confirm button
        c_button = tk.Button(self, text="Confirm", command=self.confirm, bg="gray24", fg="white", borderwidth=0, font=("Comic Sans MS", 14))
        c_button.grid(row=1, column=3, pady=10)

        #back button
        b_button = tk.Button(self, text="Back", command=self.back, bg="gray24", fg="white", borderwidth=0, font=("Comic Sans MS", 14))
        b_button.grid(row=0, column=0, pady=10, padx=10)

        #dark/light mode?


    def confirm(self):
        self.controller.frames["PlayPage"].switch_df(self.selected_option.get()+".csv")


    def back(self):
        self.controller.show_frame("StartPage")


if __name__ == "__main__":
    app = App()
    app.mainloop()
