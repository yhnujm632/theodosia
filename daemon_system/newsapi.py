import requests
import json

class NewsAPI:
    def __init__(self):
        # I'm keeping the API key in one place for security
        self.default_api_key = "test"

        try:
            # Open the JSON preferences file if it exists
            with open("data/preferences.json") as preferences:
                # Read the file
                data = json.load(preferences)
                # Set the variables accordingly
                self.api_urls = data["api_urls"]
                self.paths = data["paths"]
                self.attribution = data["attribution"]
                self.statement = data["statement"]
        except Exception as e:
            # If the file doesn't exist or is malformed
            self.setup_default()

    def setup_default(self):
        # Set up default URLs
        self.api_urls = {
            "latest_articles": "https://content.guardianapis.com/search?show-fields=bodyText,standfirst&page=%p&api-key=DEFAULT_API_KEY",
            "search_by_section": "https://content.guardianapis.com/search?show-fields=bodyText,standfirst&section=%s&page=%p&api-key=DEFAULT_API_KEY"
        }

        # Set up default JSON paths
        self.paths = {
            "latest_articles": {
                "title": "$.response.results[*].webTitle",
                "body_text": "$.response.results[*].fields.bodyText"
            },
            "search_by_section": {
                "title": "$.response.results[*].webTitle",
                "body_text": "$.response.results[*].fields.bodyText"
            }
        }

        # Set up default attribution
        self.attribution = False
        self.statement = ""

    def save_preferences(self):
        # Get the current values, and combine them in a dictionary
        data = {
            "api_urls": self.api_urls,
            "paths": self.paths,
            "attribution": self.attribution,
            "statement": self.statement
        }
        # Write to JSON file
        with open("data/preferences.json", "w") as preferences:
            json.dump(data, preferences, indent=4)

    def set_latest_articles_url(self, url):
        # Setter for latest articles URL
        self.api_urls["latest_articles"] = url

    def set_latest_articles_path(self, title_path, content_path):
        # Setter for JSON path variables for latest articles
        self.paths["latest_articles"]["title"] = title_path
        self.paths["latest_articles"]["body_text"] = content_path

    def set_section_articles_url(self, url):
        # Setter for section articles URL
        self.api_urls["search_by_section"] = url

    def set_section_articles_path(self, title_path, content_path):
        # Setter for JSON path variables for section articles
        self.paths["search_by_section"]["title"] = title_path
        self.paths["search_by_section"]["body_text"] = content_path

    def set_attribution(self, attribution, statement=""):
        # Setter for attribution variables
        self.attribution = attribution
        self.statement = statement

    def get_latest_articles(self, page):
        # Get the data using the API URL and the JSON path
        try:
            return requests.get(self.api_urls["latest_articles"].replace("%p", str(page)).replace("DEFAULT_API_KEY", self.default_api_key)).json()
        except Exception as e:
            # If there's an error just return False. The program will handle it at a later point.
            return False

    def get_section_articles(self, page, section):
        # Get the data using the API URL and the JSON path
        try:
            return requests.get(self.api_urls["search_by_section"].replace("%p", str(page)).replace("%s", section).replace("DEFAULT_API_KEY", self.default_api_key)).json()
        except Exception as e:
            # If there's an error just return False. The program will handle it at a later point.
            return False

    def needs_attribution(self):
        # Getter for the attribution value
        return self.attribution

    def get_statement(self):
        # Getter for the attribution statement value
        return self.statement

    def get_type(self, decision):
        # A simple function just to classify the command as either a "latest article" request or a "section article" request
        match decision:
            case "latest articles" | "next page of latest articles" | "current page of latest articles":
                return "latest_articles"
            case "search articles by section" | "a different section" | "next page of section" | "current page of section":
                return "search_by_section"

        return ""

