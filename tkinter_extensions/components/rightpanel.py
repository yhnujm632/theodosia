import tkinter as tk

class RightPanel(tk.Frame):
    def __init__(self, root, bold_font, window_font):
        # Initialize frame
        super().__init__(root)
        # Initialize frame inside of frame
        self.article_frame = tk.Frame(self)
        
        # Initialize text box for most narration purposes
        self.voice_text = tk.Text(self, height=1, font=window_font, state="disabled")
        # Initialize text box for just the reading of the articles
        self.article_text = tk.Text(self.article_frame, wrap="word", font=window_font, state="disabled")
        
        # Initialize scrollbar for the article_text text box
        self.article_scrollbar = tk.Scrollbar(self.article_frame, command=self.article_text.yview)
        # Set scrollbar to control the article_text text box
        self.article_text.config(yscrollcommand=self.article_scrollbar.set)
        
    def change_voice_text(self, text):
        # Enable editing of the text box
        self.voice_text.config(state="normal")
        # Clear text
        self.voice_text.delete("1.0", "end")
        # Insert new text
        self.voice_text.insert("1.0", text)
        # Disable again
        self.voice_text.config(state="disabled")

    def change_article_text(self, text):
        # Enable editing of the text box
        self.article_text.config(state="normal")
        # Clear text
        self.article_text.delete("1.0", "end")
        # Insert new text
        self.article_text.insert("1.0", text)
        # Disable again
        self.article_text.config(state="disabled")

    def pack(self):
        # Pack the frame itself
        super().pack(expand=True, fill="both", side="right")
        # Pack the voice_text text box
        self.voice_text.pack(side="top", fill="x", padx=10, pady=(10, 0))
        # Pack the frame inside the frame for the article text
        self.article_frame.pack(side="top", expand=True, fill="both", padx=10, pady=10)
        # Pack the article scrollbar for the article_text text box
        self.article_scrollbar.pack(side="right", fill="y")
        # Pack the article_text text box
        self.article_text.pack(side="left", expand=True, fill="both")