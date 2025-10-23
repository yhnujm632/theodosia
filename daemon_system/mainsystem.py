import requests
import speech_recognition
import time
from transformers import pipeline
from functools import partial
from jsonpath_ng import parse
from .newsapi import NewsAPI
from lib.ezrecord import EzRecord
from lib.voice import Voice
from lib.choicemaker import ChoiceMaker

class MainSystem:
    def __init__(self, root_window):
        # Initialize the speech-to-text engine
        self.speech_to_text = speech_recognition.Recognizer()

        # Initialize the EzRecord object
        self.recorder = EzRecord("data/recording.wav", graphic_output=False)
        
        # Initialize the HuggingFace classification model
        self.classifier = pipeline(task="zero-shot-classification", model="facebook/bart-large-mnli")
        
        # Initialize the RootWindow class
        self.root_window = root_window
        
        # Initialize the Voice object
        self.voice = Voice()
        
        # Initialize the ChoiceMaker object
        self.choice_maker = ChoiceMaker(self.speech_to_text, self.recorder, self.classifier, self.audio_print)

        # Initialize the NewsAPI object. By default, it uses the Guardian's API. It can be changed in the CustomAPI class.
        self.news_api = NewsAPI()
        # Configure the RootWindow object to have access to the NewsAPI object
        self.root_window.set_news_api(self.news_api)

        # Initialize the section options. It doesn't change, so it's all capitalized here.
        self.SECTION_OPTIONS = [
            "about",
            "animals-farmed",
            "artanddesign",
            "australia-news",
            "better-business",
            "books",
            "business",
            "business-to-business",
            "cardiff",
            "childrens-books-site",
            "cities",
            "commentisfree",
            "community",
            "crosswords",
            "culture",
            "culture-network",
            "culture-professionals-network",
            "edinburgh",
            "education",
            "enterprise-network",
            "environment",
            "extra",
            "fashion",
            "film",
            "food",
            "football",
            "games",
            "global-development",
            "global-development-professionals-network",
            "government-computing-network",
            "guardian-foundation",
            "guardian-professional",
            "healthcare-network",
            "help",
            "higher-education-network",
            "housing-network",
            "inequality",
            "info",
            "jobsadvice",
            "katine",
            "law",
            "leeds",
            "lifeandstyle",
            #"local", <--- removing this one because it doesn't have any body text
            "local-government-network",
            "maggie goodlander", # ;)
            "media",
            "media-network",
            "membership",
            "money",
            "music",
            "news",
            "politics",
            "public-leaders-network",
            "science",
            "search",
            "small-business-network",
            "social-care-network",
            "social-enterprise-network",
            "society",
            "society-professionals",
            "sport",
            "stage",
            "teacher-network",
            "technology",
            "thefilter",
            "thefilter-us",
            "theguardian",
            "theobserver",
            "travel",
            "travel/offers",
            "tv-and-radio",
            "uk-news",
            "us-news",
            "us-wellness",
            "voluntary-sector-network",
            "weather",
            "wellness",
            "women-in-leadership",
            "working-in-development",
            "world"
        ]

    def audio_print(self, text, quit_audio=True, custom_quit_audio=None, article=False):
        # If this audio_print is not to cover an article:
        if not article:
            # Set voice text to whatever the text is
            def set_voice_text():
                self.root_window.set_voice_text(text)
            self.root_window.after(0, set_voice_text)
        else:
            # Set article text to whatever the text is
            def set_article_text():
                self.root_window.set_article_text(text)
            self.root_window.after(0, set_article_text)

        # Use voice to speak the text
        self.voice.output(text, quit_audio, custom_quit_audio)

    def _get_article_decision(self, page, previous_choice=None):
        # If there is no previous choice, give the following two options
        if previous_choice == None:
            question_background = """
            Do you want to read the latest articles, or search articles by section?
            If you want to search articles in a category, I would suggest section.
            If you just want the latest news, I would suggest reading the latest articles. 
            """.replace("\n", " ").replace("    ", " ").strip()
            main_question = "Which do you prefer: latest or section?"
            options = [
                "latest articles",
                "search articles by section"
            ]
        # If the previous choice was to select the latest articles, give the following options
        elif previous_choice == "latest articles" or previous_choice == "next page of latest articles" or previous_choice == "current page of latest articles":
            question_background = """
            Do you want to continue with the next page of the latest articles?
            You can also reread this current page of latest articles or search articles by section.
            Or, you can be done.
            """.replace("\n", " ").replace("    ", " ").strip()
            main_question = "Which do you prefer: next page of latest, current page of latest, search articles by section, or done?"
            options = [
                "next page of latest articles",
                "current page of latest articles",
                "search articles by section",
                "be done"
            ]
        # If the previous choice was to search articles by section, give the following options
        elif previous_choice == "search articles by section" or previous_choice == "a different section" or previous_choice == "next page of section" or previous_choice == "current page of section":
            question_background = """
            Do you want to continue with the next page of the articles under this section?
            You can also reread this current page of articles under this section or search for a new section.
            You can also read the latest articles.
            Or, you can be done.
            """.replace("\n", " ").replace("    ", " ").strip()
            main_question = "Which do you prefer: next page of section, current page of section, a different section, latest articles, or done?"
            options = [
                "next page of section",
                "current page of section",
                "a different section",
                "latest articles",
                "be done"
            ]

        # Ask the user to select
        decision = self.choice_maker.get_multiple_choice(options, question_background, main_question)

        # After selecting, let the user know the program has received the user's preferences
        self.audio_print("OK then!")

        # Return the decision
        return decision

    def _acquire_articles(self, page, decision, section=""):
        data = ""

        # Depending on what the decision is and the current page, make a slightly different API call
        match decision:
            case "latest articles":
                page = 1
                data = self.news_api.get_latest_articles(page)
            case "next page of latest articles":
                page += 1
                data = self.news_api.get_latest_articles(page)
            case "current page of latest articles":
                data = self.news_api.get_latest_articles(page)
            case "search articles by section" | "a different section":
                page = 1
                section = self.choice_maker.get_multiple_choice(self.SECTION_OPTIONS, "There are countless different sections.", "Name a general topic, and I will match it to the closest section available. Which topic would you like?")
                self.audio_print(f"I have selected the section {section} for you.")
                data = self.news_api.get_section_articles(page, section)
            case "next page of section":
                page += 1
                data = self.news_api.get_section_articles(page, section)
            case "current page of section":
                data = self.news_api.get_section_articles(page, section)

        # If an error ocurred the data will be set to False (or None)
        if not data:
            self.audio_print("Oops, an error happened when trying to get the articles. Make sure you're connected to WiFi. Also, if you are using custom URLs, make sure the URL and the API key are valid.", False)
            data = {}

        return (data, page, section)

    def compile_news(self):
        # At the beginning, the page should be 1 and the number article should be 1
        number_article = 1
        page = 1

        # Ask for the user's decision on which articles to browse, and then get the necessary articles
        decision = self._get_article_decision(page)
        articles, page, section = self._acquire_articles(page, decision)
        
        # Loop while the window is open
        while True:

            # If the user wants to quit
            if decision == "be done":
                self.audio_print("OK, see you then.", False)
                # Break out of the loop
                break

            # Get titles and contents using API
            titles = parse(self.news_api.paths[self.news_api.get_type(decision)]["title"]).find(articles)
            contents = parse(self.news_api.paths[self.news_api.get_type(decision)]["body_text"]).find(articles)

            # Attribute the source if needed
            if self.news_api.needs_attribution():
                self.audio_print(self.news_api.get_statement(), False)

            # After receiving the articles, send them to the RootWindow to make them show up in the left panel
            self.root_window.after(0, partial(self.root_window.compile_articles, titles, contents))

            # For each article in the list of articles:
            for x in range(min(len(titles), len(contents))):

                # Highlight the respective article button
                self.root_window.after(0, partial(self.root_window.highlight, (number_article - 1) % 10))

                # Ask if the user would like to read the article
                response = self.choice_maker.get_yes_or_no("Article number " + str(number_article) + ". " + titles[x].value, "Would you like to read this article?")
                
                # Read the article if yes, otherwise don't read the article
                if response:
                    self.audio_print("OK, let me read you the article.", False)
                    self.audio_print(contents[x].value, article=True)
                else:
                    self.audio_print("All right, moving on to the next article.", False)

                # Unhighlight the article afterwards, and clear the article text box
                self.root_window.after(0, partial(self.root_window.unhighlight, (number_article - 1) % 10))
                self.audio_print("", article=True)

                # Increase the article number by 1
                number_article += 1

            # Inform the user that this is the end of the articles currently loaded.
            self.audio_print("You have reached the end of the articles.")

            # Go again; ask what the user would like to read next!
            decision = self._get_article_decision(page, decision)
            articles, page, section = self._acquire_articles(page, decision, section)

        # When the loop is finished, destroy the window.
        self.root_window.destroy()

    def press_enter(self):
        # When enter is pressed, set the boolean value in the Voice object to True. If audio is playing, it will now stop. Otherwise, this won't do anything.
        self.voice.enter_pressed = True



