import time
import random
import tkinter as tk
from tkinter import font, messagebox

def get_text():
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Python programming is fun and engaging.",
        "Typing tests improve your speed and accuracy.",
        "Practice makes perfect when it comes to typing.",
        "The early bird catches the worm.",
        "Success comes to those who work hard.",
        "Learning to type fast is a valuable skill.",
        "Consistency is key to improvement."
    ]
    return random.choice(texts)

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg='#F0F0F0')
        
        # Add window icon and make window resizable
        self.root.resizable(True, True)
        
        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.text_font = font.Font(family="Courier New", size=16)
        self.result_font = font.Font(family="Arial", size=14, weight="bold")

        # Initialize variables
        self.start_time = None
        self.running = False
        self.original_text = ""
        self.best_wpm = 0
        self.best_accuracy = 0

        # Build UI
        self.setup_ui()
        self.new_test()

    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#F0F0F0')
        main_container.pack(expand=True, fill='both', padx=20, pady=20)

        self.header = tk.Label(main_container, text="Typing Speed Test", font=self.title_font, bg='#F0F0F0', fg='#2C3E50')
        self.header.pack(pady=10)

        # Stats frame
        stats_frame = tk.Frame(main_container, bg='#F0F0F0')
        stats_frame.pack(fill='x', pady=5)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Best WPM: 0 | Best Accuracy: 0%",
            font=self.result_font,
            bg='#F0F0F0',
            fg='#2980B9'
        )
        self.stats_label.pack()

        self.sample_frame = tk.Frame(main_container, bg='white', padx=20, pady=20)
        self.sample_frame.pack(pady=10, fill='x')

        self.sample_label = tk.Label(
            self.sample_frame,
            text="",
            font=self.text_font,
            bg='white',
            fg='#34495E',
            wraplength=700,
            justify=tk.LEFT
        )
        self.sample_label.pack()

        self.input_text = tk.Text(
            main_container,
            font=self.text_font,
            height=5,
            width=60,
            padx=10,
            pady=10,
            wrap=tk.WORD,
            bg='#FFFFFF'
        )
        self.input_text.pack(pady=20, fill='x')
        self.input_text.bind("<KeyPress>", self.start_timer)
        self.input_text.bind("<Control-r>", lambda e: self.new_test())  # Add keyboard shortcut

        self.btn_frame = tk.Frame(main_container, bg='#F0F0F0')
        self.btn_frame.pack(pady=10)

        self.restart_btn = tk.Button(
            self.btn_frame,
            text="New Test (Ctrl+R)",
            font=self.text_font,
            command=self.new_test,
            bg='#3498DB',
            fg='white',
            activebackground='#2980B9',
            activeforeground='white'
        )
        self.restart_btn.pack(side=tk.LEFT, padx=10)

        self.result_label = tk.Label(
            main_container,
            text="Click the text area below to start typing!",
            font=self.result_font,
            bg='#F0F0F0',
            fg='#27AE60'
        )
        self.result_label.pack(pady=10)

    def new_test(self):
        self.original_text = get_text()
        self.sample_label.config(text=self.original_text)
        self.input_text.delete('1.0', tk.END)
        self.result_label.config(text="Click the text area below to start typing!", fg='#27AE60')
        self.running = False
        self.start_time = None
        self.input_text.config(bg='#FFFFFF', state=tk.NORMAL)
        self.input_text.focus_set()

    def start_timer(self, event):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.input_text.config(bg='#F9EBEA')
            self.result_label.config(text="Typing...", fg='#E74C3C')
            self.root.after(100, self.update_timer)

        self.check_completion()

    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.start_time
            wpm = self.calculate_wpm(elapsed)
            self.result_label.config(text=f"Elapsed Time: {elapsed:.1f}s | WPM: {wpm}")
            self.root.after(100, self.update_timer)  # Update more frequently

    def calculate_wpm(self, elapsed):
        typed_text = self.input_text.get('1.0', 'end-1c')
        typed_words = len(typed_text.split())
        return int(typed_words / (elapsed / 60)) if elapsed > 0 else 0

    def check_completion(self):
        user_input = self.input_text.get('1.0', 'end-1c')
        if user_input == self.original_text:
            self.show_final_results()

    def show_final_results(self):
        self.running = False
        self.input_text.config(state=tk.DISABLED)
        elapsed_time = time.time() - self.start_time
        user_input = self.input_text.get('1.0', 'end-1c')

        min_length = min(len(self.original_text), len(user_input))
        correct = sum(1 for o, t in zip(self.original_text, user_input) if o == t)
        accuracy = (correct / len(self.original_text)) * 100 if len(self.original_text) > 0 else 0
        wpm = self.calculate_wpm(elapsed_time)

        # Update best scores
        if wpm > self.best_wpm:
            self.best_wpm = wpm
        if accuracy > self.best_accuracy:
            self.best_accuracy = accuracy

        self.stats_label.config(text=f"Best WPM: {self.best_wpm} | Best Accuracy: {self.best_accuracy:.1f}%")

        result_text = (
            f"Time: {elapsed_time:.2f}s | WPM: {wpm} | Accuracy: {accuracy:.1f}%\n"
            "Press 'New Test' or Ctrl+R to try again!"
        )

        if user_input == self.original_text:
            result_text = "Perfect! " + result_text
            messagebox.showinfo("Congratulations!", "Perfect typing! Great job!")

        self.result_label.config(text=result_text, fg='#27AE60')
        self.input_text.config(bg='#EAFAF1')

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
