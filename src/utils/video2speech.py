import logging
import moviepy.editor as mp

def video_to_speech(video_filename, wav_filename):
    clip = mp.VideoFileClip(video_filename).subclip(0,-0.5)
    clip.audio.write_audiofile(wav_filename)
    logging.info('video_to_speech success!')
    return 'ok'