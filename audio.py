from pydub import AudioSegment
import os
import wave
import subprocess
import datetime
import db
import s3
import asyncio


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
    current_timestamp = int(datetime.timestamp(datetime.now()))
    mp3_file_name = f'{current_timestamp}.mp3'
    print("start pcm_to_mp3")
    pcm_to_mp3(pcm_file, mp3_file_name)
    print("start upload 2 s3")
    s3.upload_obj_to_s3(mp3_file_name, s3.prefix+mp3_file_name)
    print("start write db")
    db.insert_data(current_timestamp, False)


def pcm2wav(pcm_data, wav_file, channels=1, bits=16, sample_rate=16000):
    # 打开 PCM 文件

    # 打开将要写入的 WAVE 文件
    wavfile = wave.open(wav_file, 'wb')
    # 设置声道数
    wavfile.setnchannels(channels)
    # 设置采样位宽
    wavfile.setsampwidth(bits // 8)
    # 设置采样率
    wavfile.setframerate(sample_rate)
    # 写入 data 部分
    wavfile.writeframes(pcm_data)
    wavfile.close()


if __name__ == "__main__":
    input_file = './data.bin'
    output_file = 'output.mp3'
    pcm_to_mp3(input_file, output_file)
