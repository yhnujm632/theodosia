[![Open Issues](https://img.shields.io/badge/open%20issues-0-green)](https://github.com/yhnujm632/theodosia/issues)
[![License](https://img.shields.io/badge/license-The%20Unlicense-yellow)](https://github.com/yhnujm632/theodosia/blob/main/LICENSE)

# Theodosia

## **What is it?**
A Python Tkinter app. It lets the user browse news, only requiring audio as input to work, making it ideal as a visually impaired accomodation. It reads out the articles to the user.

## **What does it do?**
* Gathers data from news source (the Guardian by default) using an API
* Uses text-to-speech (TTS) to ask the user if he/she would like to listen to the latest articles or search articles by section
* Lists articles 10 at a time, and asks the user for each if he/she would like to listen to the article
* If it's a yes, the app reads the article out to the user
* If it's a no, the app continues to the next article
* When all 10 articles have been completed, gives the user some options:
    * Continue with the next 10 articles
    * Switch to browsing latest articles/switch to searching articles by section
    * If the user is currently browsing articles by section, give the user the option of searching by a different section

## **What is it made with?**
***Programming languages:*** Python

***Standard libraries:*** `tkinter, time, threading, subprocess, os, sys, functools, wave, math, json, statistics`

***Extra libraries:*** `jsonpath_ng, numpy, pyaudio, requests, speechrecognition, transformers`

***Other resources:*** `piper.exe`, a text-to-speech program

## **How does it work?**
* Gets data using the requests library and the NewsAPI class in `daemon_system/newsapi.py`
* Speaks to the user using the Voice class in `lib/voice.py`
* Records the user's vocal response using the EzRecord class in `lib/EzRecord.py`
* Uses `speechrecognition` to turn audio into text
* Uses HuggingFace's ML libraries and the ChoiceMaker class in `lib/choicemaker.py` to analyze user input
* Uses various classes in the `tkinter_extensions` folder to make the UI. The RootWindow class in `tkinter_extensions/rootwindow.py` is the primary UI class
* The CustomAPI class in `tkinter_extensions/components/customapi.py` is a separate window where users can choose to use a different API from the default Guardian API.
    * e.g. If I wanted to listen to the New York Times instead, and I had an API key to the New York Times, I could use the Custom API window to listen to the New York Times instead.
* Saves user preferences in `data/preferences.json` for future use

## **What programming skills were used in/learned making this app?**
* ***Object-oriented programming (OOP).*** Lots of it. I took AP Computer Science A this past year, and this was the perfect place to use OOP. I have broken up different tasks into lots and lots of different classes, mostly instance classes for this app.
* ***UI design.*** I was kind of familiar with Tkinter, since I used it back in 7th grade, but I needed to refamiliarize myself for this app.
* ***Audio formatting.*** Before this project, I had no idea what `pa.Int16` or `pa.Int32` meant. Nor that 44.1 kHz was considered the standard audio sample rate. I know that now.
* ***Subprocess I/O handling.*** This sounds a lot more complicated than it actually is. It's basically controlling a terminal subprocess, determining the chunk sizes, setting up the standard input and output (STDIN/STDOUT) streams, etc.

## **Any important links?**
* My personal website page for the app: https://mampuzha.org/theodosia/
* YouTube demonstration (long version): https://www.youtube.com/watch?v=yPalMSkpB7Y
* YouTube demonstration (short version): https://www.youtube.com/watch?v=gECAJe6qbkU

## **Any other notes?**
**The folder named "piper" is NOT my own work - it's a library that I use that is saved locally. It is the folder containing the piper.exe file. Piper is the library I use to stream text to audio. You can find the source code to the piper.exe file here: https://github.com/rhasspy/piper**
