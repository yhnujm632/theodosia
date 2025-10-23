import pyaudio
import wave
import time
from math import ceil, floor
from numpy import sqrt, mean, frombuffer, int16

class EzRecord:
    def __init__(self, filename="recording.wav", graphic_output=True, audio_format=pyaudio.paInt16, channels=2, rate=44100, chunk=6144):

        # Initialize self._pyaudio_object -- it will be the object that plays the generated audio
        self.pyaudio_object = pyaudio.PyAudio()

        # Set the audio format - paInt16 is the setting I use
        self.format = audio_format

        # Set the channels - usually 2, because we want dual-channel audio
        self.channels = channels

        # Set the rate - standard rate is 44.1 kHz, so I do 44100
        self.rate = rate

        # Set the chunk - I've been using 6144 (6 KiB)
        self.chunk = chunk

        # Set the filepath
        self.filepath = filename

        # Set the graphic output to true or false. Default is True.
        self.graphic_output = graphic_output

    def _calc_volume(self, data, width=2):
        # Based off of the RMS formula for calculating volume
        print(int(sqrt(mean(pow(frombuffer(data, int16).astype(float), 2))) / 16))
        return int(sqrt(mean(pow(frombuffer(data, int16).astype(float), 2))) / 16)

    def _write_to_wav(self, audio_frames):
        with wave.open(self.filepath, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.pyaudio_object.get_sample_size(self.format))
            wav_file.setframerate(self.rate)
            wav_file.writeframes(b''.join(audio_frames))
        
    def recordUntilQuiet(self):
        # Reset the pyaudio_object if it's been destroyed
        if not self.pyaudio_object:
            self.pyaudio_object = pyaudio.PyAudio()

        # Use the pyaudio_object and create a new audio recording stream
        recorder = self.pyaudio_object.open(input=True, format=self.format, channels=self.channels, rate=self.rate, frames_per_buffer=self.chunk)

        # Initialize a list to hold the audio frames
        audio_frames = []

        # Initialize booleans for logic
        has_been_loud_before = False
        can_get_start_time = True

        # Set default time to 0 (the distance between the current time and the start_time is what matters)
        start_time = 0

        # Repeat until the loop is broken when the distance in time since the user has quietened down is at least 2 seconds
        while True:
            # Read the current chunk of audio
            audio_frame = recorder.read(self.chunk)
            # Append it to the list of frames
            audio_frames.append(audio_frame)
            # If the volume of this frame is over 30 units:
            if self._calc_volume(audio_frame) > 30:
                # Set the has_been_loud_before to True (it might already be True based on previous iterations but that's ok) and the can_get_start_time to True
                has_been_loud_before = True
                can_get_start_time = True
                # Set the start_time back to 0 in case it's not 0
                start_time = 0
            elif has_been_loud_before and can_get_start_time:
                # Set the start time to the current time, because it's not loud anymore
                start_time = time.time()
                can_get_start_time = False
            elif has_been_loud_before and time.time() - start_time > 2:
                # Break, because the distance between when the user began being quiet and now is more than 2 seconds
                break

        # Stop the recording stream and close the recorder
        recorder.stop_stream()
        recorder.close()
        # Terminate the current pyaudio_object (it will need to be reset)
        self.pyaudio_object.terminate()

        # Write the data to a .wav file
        self._write_to_wav(audio_frames)

        # Reset the pyaudio object
        self.pyaudio_object = None
