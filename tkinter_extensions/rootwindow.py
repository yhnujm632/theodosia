import tkinter as tk
from .components.menustrip import MenuStrip
from .components.leftpanel import LeftPanel
from .components.rightpanel import RightPanel
from .components.customapi import CustomAPI
from tkinter import font

class RootWindow(tk.Tk):
    def __init__(self):
        # Initialize the superclass - the tk.Tk Tkinter class
        super().__init__()

        # Set the window size to 850 x 300 pixels
        self.geometry("850x300")

        # Set the window title to "Theodosia"
        self.title("Theodosia")

        # Set the window icon
        self.iconbitmap("icon_logo.ico")

        # Save the default font to a variable as the window font
        window_font = font.nametofont("TkDefaultFont")

        # Take the window font variable, make a copy of it, set it to the bold font variable, and then bold it
        bold_font = font.nametofont("TkDefaultFont").copy()
        bold_font.config(weight="bold")

        # Configure the number of rows and columns for the app's layout (0 rows and 0 columns because I'm not using a row-column layout)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Initialize the left and right panel classes, both of which will contain various other elements
        self.left_panel = LeftPanel(self, bold_font, window_font)
        self.right_panel = RightPanel(self, bold_font, window_font)

        # Create a tk.BooleanVar variable to measure if the left panel is visible        
        self.left_panel_is_showing = tk.BooleanVar(value=True)

        
        self.custom_api = CustomAPI(self)

        # Create a menu strip for the top. As you can see, the MenuStrip class takes a list of objects and can read it to create the appropriate menu. That way, from here I can choose what I want in my menu.
        self.menu = MenuStrip(self, [
            {
                "name": "file_menu",
                "label": "File",
                "dropdown": [
                    {
                        # Menu option to import a custom API
                        "label": "Import a Custom API...",
                        "type": "command",
                        "command": self.custom_api.pack
                    },
                    {
                        # Menu option to close the window
                        "label": "Close",
                        "type": "command",
                        "command": self.destroy
                    }
                ]
                
            },
            {
                "name": "view_menu",
                "label": "View",
                "dropdown": [
                    {
                        # Menu option to show/hide the left panel
                        "label": "Show Articles Panel",
                        "type": "checkbutton",
                        "variable": self.left_panel_is_showing,
                        "command": self._toggle_left_panel
                    }
                ]
            }
        ])

        # Pack the left and right panels
        self.left_panel.pack()
        self.right_panel.pack()

        # Set minimum size to 850 x 300 pixels (I think it looks ugly if you get it any smaller than that)
        self.minsize(850, 300)

        # Set up the function self._enter_listener() to run whenever the enter key is pressed
        self.bind("<Return>", self._enter_listener)
        
    def set_main_system(self, main_system):
        # Set the main_system variable here, not in the __init__() function, because after declaring the RootWindow class I have to initialize the MainSystem class using the RootWindow class as a parameter
        self.main_system = main_system

    def _toggle_left_panel(self):
        # Show/hide the left panel depending on if it's already showing or not
        if self.left_panel_is_showing.get():
            self.left_panel.pack()
        else:
            self.left_panel.pack_forget()
    
    def highlight(self, article_index):
        # Highlight a given article if it exists
        try:
            self.left_panel.highlight(article_index)
        except Exception as e:
            pass

    def unhighlight(self, article_index):
        # Unhighlight a given article if it exists
        try:
            self.left_panel.unhighlight(article_index)
        except Exception as e:
            pass

    def compile_articles(self, titles, contents):
        # Set up all the article boxes in the left panel
        self.left_panel.compile_articles(titles, contents)
        self.left_panel.pack()

    def set_voice_text(self, text):
        # Alter the text in the top-right box
        self.right_panel.change_voice_text(text)

    def set_article_text(self, text):
        # Alter the text in the bottom-right box
        self.right_panel.change_article_text(text)

    def _enter_listener(self, event):
        # Function to be called whenever the enter key is pressed
        self.main_system.press_enter()

    def set_news_api(self, news_api):
        # Set the news_api object here
        self.news_api = news_api
        self.custom_api.set_news_api(news_api)