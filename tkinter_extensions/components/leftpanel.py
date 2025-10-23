import tkinter as tk
from .articlebutton import ArticleButton

class LeftPanel(tk.Frame):
    def __init__(self, root, bold_font, window_font):
        # Initialize frame
        super().__init__(root, width=200, highlightthickness=0)
        # Initialize scrollbar
        self.scrollbar = tk.Scrollbar(self)
        # Initialize canvas
        self.scroll_canvas = tk.Canvas(self, width=200, highlightthickness=0)
        # Initialize frame within canvas
        self.scroll_canvas_frame = tk.Frame(self.scroll_canvas, width=200, highlightthickness=0)
        # Initialize window of frame in the canvas
        self.scroll_canvas_frame_window = self.scroll_canvas.create_window(0, 0, anchor="nw", window=self.scroll_canvas_frame, width=200)

        # Initialize fonts
        self.bold_font = bold_font
        self.window_font = window_font

        # Initialize list of buttons
        self.article_buttons = []
        
        # Configure the frame within the canvas to scroll the overflow within it
        self.scroll_canvas_frame.bind("<Configure>", self._auto_overflow)
        # Connect the scrollbar to the canvas
        self.scrollbar.config(command=self.scroll_canvas.yview)
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)

    def compile_articles(self, titles, contents):
        # Basically, just run through the api_results parameter passed in and add an ArticleButton object for each article with the appropriate information. "standfirst" is just the name for the subtitle of the article.
        self.article_buttons = []
        for x in range(min(len(titles), len(contents))):
            self.article_buttons.append(ArticleButton(self.scroll_canvas_frame, self.bold_font, self.window_font, titles[x].value, contents[x].value))
    
    def highlight(self, article_index):
        # Simulate a press state change if someone wants to highlight the ArticleButton - it basically makes the button blue
        self.article_buttons[article_index].press()

    def unhighlight(self, article_index):
        # Simulate an "unpress" (I don't know the word) state change if someone wants to unhighlight the ArticleButton - it basically makes the button white again
        self.article_buttons[article_index].release()

    def _auto_overflow(self, event):
        # Auto-configure the canvas to NOT increase its height to accomodate all the articles - I want the overflow to be scrolled
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def pack(self):
        # First, pack the frame itself by calling super()
        super().pack(side="left", fill="y", padx=(10, 0), pady=10)
        # Next, pack the scrollbar
        self.scrollbar.pack(side="right", fill="y")
        # Next, pack the canvas
        self.scroll_canvas.pack(fill="both", expand=True)
        # Finally, pack the articles
        for article_button in self.article_buttons:
            article_button.pack(fill="x", padx=1, ipady=10)