import tkinter as tk
from tkinter import ttk

class CustomAPI(tk.Toplevel):
    def __init__(self, root):
        # Initialize the superclass
        super().__init__(root)
        # Set the size of the window, and make it unresizable so it's permanent
        self.geometry("600x600")
        self.resizable(False, False)
        # Set the title of the window
        self.title("Import a Custom API")
        # Set the window icon
        self.iconbitmap("icon_logo.ico")
        # Edit the window commands so that when you "x" out it doesn't destroy the whole window, it just minimizes it
        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        # Labels
        # Create the label for the URL for the latest articles
        self.latest_articles_label = tk.Label(self, wraplength=440, justify="left", anchor="w", text="Enter your latest article API url here (you must have the API key).\nWhere the page number goes, replace it with \"%p\".")
        # Create the label for the JSON path for the title in the latest articles API
        self.latest_articles_title_label = tk.Label(self, wraplength=440, justify="left", anchor="w", text="Enter the JSON path to the *title* in the latest articles' URL API.")
        # Create the label for the JSON path for the content in the latest articles API
        self.latest_articles_content_label = tk.Label(self, wraplength=440, justify="left", anchor="w", text="Enter the JSON path to the *body text* in the latest articles' URL API.")
        # Create the label for the URL for the search by section
        self.search_by_section_label = tk.Label(self, wraplength=440, justify="left", anchor="w", text="Enter your search article by section API url here (you must have the API key).\nWhere the page number goes, replace it with \"%p\".\nWhere the section goes, replace it with \"%s\".")
        # Create the label for the JSON path for the title in the search by section
        self.search_by_section_title_label = tk.Label(self, wraplength=440, justify="left", anchor="w", text="Enter the JSON path to the *title* in the search by section's URL API.")
        # Create the label for the JSON path for the content in the search by section
        self.search_by_section_content_label = tk.Label(self, wraplength=440, justify="left", anchor="w", text="Enter the JSON path to the *body text* in the search by section's URL API.")
        # Create the label for the attribution label
        self.attribution_label = tk.Label(self, wraplength=440, justify="left", anchor="w", text="This is if the terms of service of your API require you to attribute your content.\nType the attribution statement in here.")

        # Just to cover my rear end from any legal repurcussions
        self.legal_text = tk.Label(self, wraplength=440, justify="left", anchor="w", text="For legal reasons, by using your API here, you agree you have permission to use the API and are following the API's terms.\nYou agree that this app and its creator are not liable for any misuse of an API.")

        # Entries
        self.latest_articles_entry = tk.Entry(self)
        self.latest_articles_title_entry = tk.Entry(self)
        self.latest_articles_content_entry = tk.Entry(self)
        self.search_by_section_entry = tk.Entry(self)
        self.search_by_section_title_entry = tk.Entry(self)
        self.search_by_section_content_entry = tk.Entry(self)
        self.attribution_entry = tk.Entry(self)


        # Create the save button, and set the command to the class function _save_changes()
        self.save_button = ttk.Button(self, text="Save Changes (temporary)", command=self._save_changes)
        self.save_default_button = ttk.Button(self, text="Save Changes (permanent)", command=self._save_default)
        self.restore_default_button = ttk.Button(self, text="Restore Default Preferences (permanent)", command=self._restore_default)

        # Minimize the window on startup
        self.withdraw()

    def set_news_api(self, news_api):
        # Setter method for the news_api object
        self.news_api = news_api

        # Autofills
        self.latest_articles_entry.insert(0, self.news_api.api_urls["latest_articles"])
        self.latest_articles_title_entry.insert(0, self.news_api.paths["latest_articles"]["title"])
        self.latest_articles_content_entry.insert(0, self.news_api.paths["latest_articles"]["body_text"])
        self.search_by_section_entry.insert(0, self.news_api.api_urls["search_by_section"])
        self.search_by_section_title_entry.insert(0, self.news_api.paths["search_by_section"]["title"])
        self.search_by_section_content_entry.insert(0, self.news_api.paths["search_by_section"]["body_text"])
        self.attribution_entry.insert(0, self.news_api.get_statement())

    def _save_changes(self):
        # Set the URLs and JSON paths
        self.news_api.set_latest_articles_url(self.latest_articles_entry.get())
        self.news_api.set_latest_articles_path(self.latest_articles_title_entry.get(), self.latest_articles_content_entry.get())
        self.news_api.set_section_articles_url(self.search_by_section_entry.get())
        self.news_api.set_section_articles_path(self.search_by_section_title_entry.get(), self.search_by_section_content_entry.get())

        # If the attribution isn't empty
        if self.attribution_entry.get() != "":
            # Save the attribution
            self.news_api.set_attribution(True, self.attribution_entry.get())
        else:
            self.news_api.set_attribution(False)

    def _save_default(self):
        # Call the _save_changes function
        self._save_changes()
        # Then tell the news_api object to save the preferences to a file
        self.news_api.save_preferences()

    def _restore_default(self):
        # Return the news_api object's values to the default
        self.news_api.setup_default()
        
        # Restore autofills
        self.latest_articles_entry.delete(0, 'end')
        self.latest_articles_title_entry.delete(0, 'end')
        self.latest_articles_content_entry.delete(0, 'end')
        self.search_by_section_entry.delete(0, 'end')
        self.search_by_section_title_entry.delete(0, 'end')
        self.search_by_section_content_entry.delete(0, 'end')
        self.attribution_entry.delete(0, 'end')

        self.latest_articles_entry.insert(0, self.news_api.api_urls["latest_articles"])
        self.latest_articles_title_entry.insert(0, self.news_api.paths["latest_articles"]["title"])
        self.latest_articles_content_entry.insert(0, self.news_api.paths["latest_articles"]["body_text"])
        self.search_by_section_entry.insert(0, self.news_api.api_urls["search_by_section"])
        self.search_by_section_title_entry.insert(0, self.news_api.paths["search_by_section"]["title"])
        self.search_by_section_content_entry.insert(0, self.news_api.paths["search_by_section"]["body_text"])
        self.attribution_entry.insert(0, self.news_api.get_statement())

        # Then tell the news_api object to save the preferences to a file
        self.news_api.save_preferences()

    def pack(self):
        # Pack the legal text
        self.legal_text.pack(fill="x", padx=30, anchor="w", pady=(10, 5))

        # Latest articles: first pack the URL label and entry, then the title JSON path label and entry, then the content JSON path label and entry
        self.latest_articles_label.pack(fill="x", padx=30, anchor="w", pady=5)
        self.latest_articles_entry.pack(fill="x", padx=33, anchor="w", pady=5)
        self.latest_articles_title_label.pack(fill="x", padx=30, anchor="w", pady=5)
        self.latest_articles_title_entry.pack(fill="x", padx=33, anchor="w", pady=5)
        self.latest_articles_content_label.pack(fill="x", padx=30, anchor="w", pady=5)
        self.latest_articles_content_entry.pack(fill="x", padx=33, anchor="w", pady=5)
        
        # Search by section: first pack the URL label and entry, then the title JSON path label and entry, then the content JSON path label and entry
        self.search_by_section_label.pack(fill="x", padx=30, anchor="w", pady=5)
        self.search_by_section_entry.pack(fill="x", padx=33, anchor="w", pady=5)
        self.search_by_section_title_label.pack(fill="x", padx=30, anchor="w", pady=5)
        self.search_by_section_title_entry.pack(fill="x", padx=33, anchor="w", pady=5)
        self.search_by_section_content_label.pack(fill="x", padx=30, anchor="w", pady=5)
        self.search_by_section_content_entry.pack(fill="x", padx=33, anchor="w", pady=5)

        # Pack the label and entry field for the attribution
        self.attribution_label.pack(fill="x", padx=30, anchor="w", pady=5)
        self.attribution_entry.pack(fill="x", padx=33, anchor="w", pady=5)

        # Pack the save changes button
        self.save_button.pack(anchor="w", padx=(30, 0), side="left", pady=5)
        self.save_default_button.pack(anchor="w", side="left", pady=5)
        self.restore_default_button.pack(anchor="w", side="left", pady=5)

        # Open the window
        self.deiconify()
