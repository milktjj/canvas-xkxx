from pydub import AudioSegment


def amr_to_mp3(input_file, output_file):
    # 使用pydub加载AMR文件
    audio = AudioSegment.from_file(input_file, format='amr')

    # 将音频导出为MP3文件
    audio.export(output_file, format='mp3')


if __name__ == "__main__":
    input_file = './1700195987.amr'
    output_file = 'output.mp3'

    amr_to_mp3(input_file, output_file)
