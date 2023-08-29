import logging
import os
import azure.cognitiveservices.speech as speechsdk
import time
import datetime

speech_key = os.getenv("AZURE_KEY")
def speech_to_text(audio_filename="sample-20230828-1854.wav"):
    global speech_key
    
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
    service_region = "eastasia"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)

    # Creates a recognizer with the given settings
    speech_config.speech_recognition_language="zh-CN"
    speech_config.request_word_level_timestamps()
    speech_config.enable_dictation()
    speech_config.output_format = speechsdk.OutputFormat(1)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    #result = speech_recognizer.recognize_once()
    all_results = []

    #https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.recognitionresult?view=azure-python
    def handle_final_result(evt):
        all_results.append(evt.result.text) 
    
    
    done = False

    def stop_cb(evt):
        logging.info('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done= True

    #Appends the recognized text to the all_results variable. 
    speech_recognizer.recognized.connect(handle_final_result) 

    #Connect callbacks to the events fired by the speech recognizer & displays the info/status
    #Ref:https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.eventsignal?view=azure-python   
    speech_recognizer.recognizing.connect(lambda evt: logging.info('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: logging.info('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: logging.info('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: logging.info('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: logging.info('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)
    logging.info('speech_to_text success!')
    return ''.join(all_results)

if __name__ == '__main__':
    #calling the conversion through a function    
    res = speech_to_text('example.wav')
    print(''.join(res))