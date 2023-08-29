import logging
import moviepy.editor as mp

def video_to_speech(video_filename, wav_filename):
    """视频转音频

    Args:
        video_filename (string): 待转换的视频文件路径
        wav_filename (string): 音频文件保存路径，建议转化成.wav文件

    Returns:
        string: _description_
    """
    try:
        clip = mp.VideoFileClip(video_filename).subclip(0,-0.5)
        clip.audio.write_audiofile(wav_filename)
        logging.info('video_to_speech success!')
        return 'ok'
    except Exception as e:
        return f'Convert failed! error message: {e.__str__}'