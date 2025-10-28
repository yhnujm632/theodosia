import pyaudio
import time
import subprocess as sp
from functools import partial
from threading import Thread
import os
import sys

class Voice:
    def __init__(self):

        # Initialize self._pyaudio_object -- it will be the object that plays the generated audio
        self._pyaudio_object = pyaudio.PyAudio()

        # Initialize the self._can_play object to True
        self._can_play = True

        # Define where the Piper model is stored (I use absolute file path)
        self.piper_model_path = "piper_voices/en_US-amy-low/en_US-amy-low.onnx"

        # Set bool that can be used to quit out of the audio
        self.enter_pressed = False

    def _default_audio(self):

        # Open the audio stream from the pyaudio object
        default_audio_stream = self._pyaudio_object.open(output=True, format=pyaudio.paInt16, rate=16000, channels=1)
        
        # Loop until broken
        while True:

            # Save chunk with limit of 6 KiB, and write it to the pyaudio stream (to play it)
            chunk = self._tts_subprocess.stdout.read(6144)
            default_audio_stream.write(chunk)

            if not chunk or not self._can_play:
                # First, kill Piper TTS subprocess (which is generating the audio)
                self._tts_subprocess.terminate()
                self._tts_subprocess.wait()

                # Next, kill the pyaudio stream (which is playing the audio)
                default_audio_stream.stop_stream()
                default_audio_stream.close()
                self._pyaudio_object.terminate()

                # Close the subprocess output
                self._tts_subprocess.stdout.close()

                # Reset the self._pyaudio_object variable for the next audio stream
                self._pyaudio_object = pyaudio.PyAudio()

                # Set the self._can_play bool to False in case the default_quit thread doesn't yet know to stop
                self._can_play = False

                break


    def _default_quit(self):

        # Reset the enter_pressed value to False
        self.enter_pressed = False

        # Repeat unless self._can_play is False
        while self._can_play:
            
            # Just add a little delay so the system doesn't blow itself up
            time.sleep(0.1)

            # If the self.enter_pressed bool has been set to False by the Tkinter window the Voice class can quit out of playback
            if self.enter_pressed == True:
                self._can_play = False



    def output(self, input_str, default_quit_audio=True, custom_quit=None, after=None):
        # Creates a Python subprocess to interact with the Piper TTS engine (this basically runs a command line prompt)
        self._tts_subprocess = sp.Popen(['.\piper\piper.exe', '--output-raw', '-m', self.piper_model_path], stdout=sp.PIPE, stdin=sp.PIPE, bufsize=0, creationflags=sp.CREATE_NO_WINDOW)
        
        # Send the input string to the stdin (standard input) using PIPE
        # I wanted to just insert the input_str as another parameter in the inital subprocess, but apparently Windows has a character limit for commands
        self._tts_subprocess.stdin.write(input_str.encode("UTF-8"))
        self._tts_subprocess.stdin.close()


        # Create a Thread to run the default audio function
        thread1 = Thread(target=self._default_audio)

        # If the function call wants the default quit function as well:
        if default_quit_audio:

            # Create another Thread for the default quit function
            thread2 = Thread(target=self._default_quit)

            # Start them together so they run at the same time
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()

        # If the function call wants to use a custom quit function instead of the default quit function:
        elif custom_quit:

            # Create another Thread for the custom quit function
            thread2 = Thread(target=partial(custom_quit, self)) # partial() basically auto-fills the function's first parameter with self -- so that the function can access class variables if it so pleases
            
            # Start them together so they run at the same time
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()

        # If the function call doesn't want any way to quit out of the default audio function:
        else:
            # Start the default audio function
            thread1.start()
            thread1.join()
            
        self._can_play = True
