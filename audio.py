from pydub import AudioSegment
import os
import wave
import subprocess
from datetime import datetime
import db
import s3
import asyncio
import config


def amr_to_mp3(input_file, output_file):
    # 使用pydub加载AMR文件
    audio = AudioSegment.from_file(input_file, format='amr')

    # 将音频导出为MP3文件
    audio.export(output_file, format='mp3')


def pcm_to_mp3(pcm_file, output_file):
    pcmf = open(pcm_file, 'rb')
    pcmdata = pcmf.read()
    pcmf.close()
    pcm2wav(pcmdata, "temp.wav")
    # 使用 FFmpeg 将 WAV 文件转换为 MP3 文件
    subprocess.call(['ffmpeg', '-i', 'temp.wav', output_file])

    # 删除临时的 WAV 文件
    os.remove('temp.wav')
    os.remove(pcm_file)


def pcm_to_s3(pcm_file):
    try:
        current_timestamp = int(datetime.timestamp(datetime.now()))
        mp3_file_name = f'{current_timestamp}.mp3'
        pcm_to_mp3(pcm_file, mp3_file_name)
        s3.upload_obj_to_s3(mp3_file_name, s3.prefix+mp3_file_name)
        db.insert_data(current_timestamp, False)
    except Exception as e:
        print(str(e))


def pcm2wav(pcm_data, wav_file, channels=1, bits=16, sample_rate=config.get_config_info()['rate']):
    wavfile = wave.open(wav_file, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(bits // 8)
    wavfile.setframerate(sample_rate)
    wavfile.writeframes(pcm_data)
    wavfile.close()


if __name__ == "__main__":
    input_file = './data.bin'
    output_file = 'output.mp3'
    pcm_to_mp3(input_file, output_file)
