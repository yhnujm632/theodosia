import tkinter as tk
class MenuStrip(tk.Menu):
    def __init__(self, root, child_menus):
        # Initialize the menu's superclass (tk.Menu)
        super().__init__(root)
        # Configure the RootWindow so that this menu is THE menu
        root.config(menu=self)
        
        # Take the passed-in list of dictionaries and interpret it accordingly to create the menu
        # For each menu dropdown
        for child_menu in child_menus:
            # Create a class attribute to this class with name of the attribute based on whatever it says in the dictionary
            setattr(self, child_menu["name"], tk.Menu(self, tearoff=False))

            # Add a dropdown
            self.add_cascade(menu=getattr(self, child_menu["name"]), label=child_menu["label"])
            
            # For each selection in the dropdown for the respective dropdown:
            for selection in child_menu["dropdown"]:

                # If the type of selection is a command
                if selection["type"] == "command":
                    # Create a selection that does a command
                    getattr(self, child_menu["name"]).add_command(label=selection["label"], command=selection["command"])

                # Otherwise it's a checkbutton
                else:
                    # So create a selection that is a checkbutton
                    getattr(self, child_menu["name"]).add_checkbutton(label=selection["label"], variable=selection["variable"], command=selection["command"])

    