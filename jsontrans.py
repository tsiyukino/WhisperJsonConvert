'''
Github: tsiyukino
Last Update: 2/4/2025 07:46:50 UTC
Description: Just a simple program that can help you merge sentences created by Openai-Whisper .json file and converted into .srt. Need adaptation for other format, but follows the same path, its easy.
Im actually thinking about writing a GUI for this and adapt it to more formats. Maybe some day. 
IMPORTANT: --word_timestamps True and .json file needed. 
'''
import json
import re

def json_to_srt(json_file, srt_file, max_line_length=42):
    """
    Converts a JSON file with word-level timestamps to an SRT file,
    merging all segments into a single sequence of subtitles,
    splitting subtitles at punctuation marks, respecting maximum line length,
    and ensuring only single spaces between words.

    Args:
        json_file (str): Path to the input JSON file.
        srt_file (str): Path to the output SRT file.
        max_line_length (int): Maximum character length for each subtitle line.
    """

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    segments = data['segments']
    subtitle_index = 1
    srt_content = ""

    sentence_lines = []
    sentence_start_time = None
    sentence_end_time = None
    current_line = ""

    all_words = []
    for segment in segments:
        all_words.extend(segment['words'])

    for word_data in all_words:
        word = word_data['word']
        start_time = word_data['start']
        end_time = word_data['end']

        if sentence_start_time is None:
            sentence_start_time = start_time

        potential_line = current_line + word + " "

        if len(potential_line) <= max_line_length:
            current_line = potential_line
        else:
            sentence_lines.append(current_line.strip())
            current_line = word + " "

        sentence_end_time = end_time

        # Punctuation
        if re.search(r'[.,;!?]', word) or word == all_words[-1]['word']:
            sentence_lines.append(current_line.strip())

            # Format times
            start_time_srt = format_time(sentence_start_time)
            end_time_srt = format_time(sentence_end_time)

            srt_content += str(subtitle_index) + "\n"
            srt_content += start_time_srt + " --> " + end_time_srt + "\n"
            for line in sentence_lines:
                srt_content += re.sub(' +', ' ', line) + "\n"
            srt_content += "\n"

            # Reset for the next subtitle
            subtitle_index += 1
            sentence_lines = []
            current_line = ""
            sentence_start_time = None
            sentence_end_time = None


    with open(srt_file, 'w', encoding='utf-8') as f:
        f.write(srt_content)


def format_time(seconds):
    # Converts seconds to SRT time format (HH:MM:SS,MS)
    milliseconds = int(seconds * 1000)
    hours = milliseconds // (3600 * 1000)
    milliseconds %= (3600 * 1000)
    minutes = milliseconds // (60 * 1000)
    milliseconds %= (60 * 1000)
    seconds = milliseconds // 1000
    milliseconds %= 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


json_file=input("Json File:")
srt_file=input("Output .srt:")
max_line_length=int(input("Max Line Length(in characters):"))


json_to_srt(json_file, srt_file, max_line_length)
print(f"Successfully converted {json_file} to {srt_file} with a maximum line length of {max_line_length}.")