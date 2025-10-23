import tkinter as tk
class ArticleButton(tk.Text):
    def __init__(self, parent_frame, bold_font, window_font, title, subtitle):
        # Initialize the text box itself
        super().__init__(parent_frame, height=3, wrap="word", cursor="hand2", borderwidth=0, relief="solid", highlightthickness=0, bg="white")
        # Set up bold and normal fonts
        self.tag_configure("bold", font=bold_font)
        self.tag_configure("normal", font=window_font)

        # Insert the title text
        self.insert("1.0", title, "bold")
        
        # Disable the text box
        self.config(state="disabled")
    
    def press(self, event=None):
        # Highlight the box when something calls this function
        self.config(highlightthickness=1, highlightcolor="#99D1FF", bg="#CCE8FF")

    def release(self, event=None):
        # Unhighlight the box when something calls this function
        self.config(highlightthickness=0, bg="white")

    def change_title(self, new_title):
        # Edit the title of the article. I don't think I ever use this, but it's useful to have on hand.
        self.config(state="normal")
        self.insert("1.0", new_title, "bold")
        self.config(state="disabled")