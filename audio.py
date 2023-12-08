from pydub import AudioSegment
import os
import wave
import subprocess
from datetime import datetime
import db
import s3
import numpy as np


def amr_to_mp3(input_file, output_file):
    # 使用pydub加载AMR文件
    audio = AudioSegment.from_file(input_file, format='amr')

    # 将音频导出为MP3文件
    audio.export(output_file, format='mp3')


def pcm_to_mp3(pcm_file, output_file):
    # need_seek = False
    # if check_byte_offset(pcm_file):
    #     need_seek = True
    pcmf = open(pcm_file, 'rb')
    # if need_seek:
    #     pcmf.seek(1, 1)
    pcmdata = pcmf.read()
    pcmf.close()
    pcm2wav(pcmdata, output_file)
    # 使用 FFmpeg 将 WAV 文件转换为 MP3 文件
    # subprocess.call(['ffmpeg', '-i', 'temp.wav', output_file])
    #
    # # 删除临时的 WAV 文件
    # os.remove('temp.wav')
    # os.remove(pcm_file)


def check_byte_offset(pcm_file):
    # 从二进制文件中读取PCM信号
    file = open(pcm_file, "rb")
    pcm_signal = np.fromfile(file, dtype=np.int16)
    # 计算信号的均值和方差
    mean = np.mean(pcm_signal)
    file.close()
    # variance = np.var(pcm_signal)
    # print(mean)
    # print(variance)
    # 设置阈值用于判断是否存在字节偏移
    threshold = 2000  # 根据实际情况进行调整

    if abs(mean) < threshold:
        return True  # 存在字节偏移
    else:
        return False  # 不存在字节偏移


def pcm_to_s3(pcm_file):
    try:
        current_timestamp = int(datetime.timestamp(datetime.now()))
        mp3_file_name = f'{current_timestamp}.wav'
        pcm_to_mp3(pcm_file, mp3_file_name)
        s3.upload_obj_to_s3(mp3_file_name, s3.prefix+mp3_file_name)
        db.insert_data(current_timestamp, False)
    except Exception as e:
        print(e)
    finally:
        if os.path.exists(pcm_file):
            os.remove(pcm_file)
        if os.path.exists(mp3_file_name):
            os.remove(mp3_file_name)


def pcm2wav(pcm_data, wav_file, channels=1, bits=16, sample_rate=8000):
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
