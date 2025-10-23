import speech_recognition
from statistics import stdev

class ChoiceMaker:
    def __init__(self, speech_to_text, recorder, classifier, audio_print):

        # Initalize speech-to-text engine
        self.speech_to_text = speech_to_text

        # Initalize EzRecord object
        self.recorder = recorder
        
        # Initalize HuggingFace classification object
        self.classifier = classifier
        
        # Initalize audio_print function
        self.audio_print = audio_print

    def get_yes_or_no(self, background_info_str, question_str):

        # audio_print the background to the question and then the question itself
        self.audio_print(background_info_str)
        self.audio_print(question_str, False)

        # Record the user's response
        self.recorder.recordUntilQuiet()

        # Use Google's text-to-speech library to convert from text into speech
        with speech_recognition.AudioFile("data/recording.wav") as recording:
            try:
                text = self.speech_to_text.recognize_google(self.speech_to_text.record(recording))
            except Exception as e:
                # If something gets messed up, set it to "maybe" by default. That way, the question can be re-asked.
                text = "maybe"

        # Classify the response as either a "yes", a "no", or a "maybe"
        classification = self.classifier(text, candidate_labels=["yes", "no", "maybe"])

        # If there's no clear winner in classification or it's classified as a "maybe"
        if stdev(classification["scores"]) < 0.15 or classification["labels"][0] == "maybe":

            # Try again
            self.audio_print("Sorry, I couldn't understand if that was a yes or a no. Can you try again?", False)

            # Recursively run the function again
            return self.get_yes_or_no(background_info_str, question_str)

        # If it's a yes
        elif classification["labels"][0] == "yes":
            return True

        # If it's a no
        elif classification["labels"][0] == "no":
            return False

    def get_multiple_choice(self, options, background_info_str, question_str):

        # audio_print the background to the question and then the question itself
        self.audio_print(background_info_str)
        self.audio_print(question_str, False)

        # Record the user's response
        self.recorder.recordUntilQuiet()

        # Use Google's text-to-speech library to convert from text into speech
        with speech_recognition.AudioFile("data/recording.wav") as recording:
            try:
                text = self.speech_to_text.recognize_google(self.speech_to_text.record(recording))
            except Exception as e:
                # If something gets messed up, set it to "maybe" by default. That way, the question can be re-asked.
                text = "maybe"

        # Classify the response as either a "yes", a "no", or a "maybe"
        classification = self.classifier(text, candidate_labels=options)

        # If there's no clear winner in classification or it's classified as a "maybe"
        if stdev(classification["scores"]) < 0.001:
        
            # Try again
            self.audio_print("Sorry, I couldn't understand that. Can you try again?", False)

            # Recursively run the function again
            return self.get_multiple_choice(options, background_info_str, question_str)

        # Otherwise just return the outcome
        else:
            return classification["labels"][0]