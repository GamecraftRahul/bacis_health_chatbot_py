from tkinter import *
import tkinter.messagebox
from bot import get_prediction, get_solution, get_precautions

BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
BG_GRAY = "#ABB2B9"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self.window.title("Smart Health Care Chatbot")
        self.window.geometry("950x650")
        self.window.configure(bg=BG_COLOR)

        self.user_name = None
        self.show_name_screen()

    def run(self):
        self.window.mainloop()

    # ==========================
    # NAME SCREEN
    # ==========================
    def show_name_screen(self):
        self.clear_window()

        Label(self.window, text="Enter Your Name:",
              bg=BG_COLOR, fg=TEXT_COLOR,
              font=FONT_BOLD).pack(pady=60)

        self.name_entry = Entry(self.window,
                                bg=BG_GRAY,
                                font=FONT_BOLD,
                                width=30)
        self.name_entry.pack()
        self.name_entry.focus()
        self.name_entry.bind("<Return>", self.get_name)

        Button(self.window,
               text="Start Chat",
               bg="red",
               fg="white",
               command=self.get_name).pack(pady=20)

    def get_name(self, event=None):
        name = self.name_entry.get().strip()

        if len(name) < 2:
            tkinter.messagebox.showwarning("Error", "Enter valid name")
            return

        self.user_name = name.split()[0]
        self.show_chat_screen()

    # ==========================
    # CHAT SCREEN
    # ==========================
    def show_chat_screen(self):
        self.clear_window()

        # TEXT AREA
        self.text_widget = Text(self.window,
                                bg=BG_COLOR,
                                fg=TEXT_COLOR,
                                font=FONT,
                                wrap=WORD)
        self.text_widget.pack(fill=BOTH, expand=True)

        # SCROLLBAR
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_widget.yview)

        self.text_widget.config(state=DISABLED)

        # INPUT AREA
        bottom_frame = Frame(self.window, bg=BG_COLOR)
        bottom_frame.pack(fill=X)

        self.msg_entry = Entry(bottom_frame,
                               bg=BG_GRAY,
                               font=FONT)
        self.msg_entry.pack(side=LEFT,
                            fill=X,
                            expand=True,
                            padx=5,
                            pady=5)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.send_message)

        Button(bottom_frame,
               text="Send",
               bg=BG_GRAY,
               font=FONT_BOLD,
               command=self.send_message).pack(side=RIGHT,
                                               padx=5,
                                               pady=5)

        # Disclaimer + Welcome
        self.bot_message("⚠️ This chatbot is for educational purposes only.")
        self.bot_message(f"Hello {self.user_name}! Describe your symptoms.")

    # ==========================
    # SEND MESSAGE
    # ==========================
    def send_message(self, event=None):
        user_input = self.msg_entry.get().strip()

        if not user_input:
            return

        self.user_message(user_input)
        self.msg_entry.delete(0, END)

        try:
            predictions = get_prediction(user_input)

            if predictions:
                for disease in predictions:
                    self.bot_message(f"🩺 Possible Condition: {disease}")
                    self.bot_message(f"💊 Solution: {get_solution(disease)}")
                    self.bot_message(f"⚠️ Precautions: {get_precautions(disease)}")
            else:
                self.bot_message("❌ I couldn't detect disease. Please explain symptoms clearly.")

        except Exception as e:
            self.bot_message("⚠️ Error processing request.")
            print(e)

    # ==========================
    # MESSAGE DISPLAY
    # ==========================
    def user_message(self, message):
        self.text_widget.config(state=NORMAL)
        self.text_widget.insert(END, f"{self.user_name}: {message}\n", "user")
        self.text_widget.tag_config("user", foreground="cyan")
        self.text_widget.config(state=DISABLED)
        self.text_widget.see(END)

    def bot_message(self, message):
        self.text_widget.config(state=NORMAL)
        self.text_widget.insert(END, f"Bot: {message}\n", "bot")
        self.text_widget.tag_config("bot", foreground="yellow")
        self.text_widget.config(state=DISABLED)
        self.text_widget.see(END)

    # ==========================
    # CLEAR WINDOW
    # ==========================
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = ChatApplication()
    app.run()