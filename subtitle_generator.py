import os
import tempfile
import subprocess
import srt
from datetime import timedelta
import re
from deep_translator import GoogleTranslator

SUPPORTED_LANGS = GoogleTranslator().get_supported_languages(as_dict=True)
LANG_DICT = {name.title(): code for name, code in SUPPORTED_LANGS.items()}


def get_font_for_text(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "fonts/NotoSansArabic-Regular.ttf"
    elif re.search(r'[\u0590-\u05FF]', text):
        return "fonts/NotoSansHebrew-Regular.ttf"
    elif re.search(r'[\u3040-\u30FF\u31F0-\u31FF]', text):
        return "fonts/NotoSansCJKjp-Regular.otf"
    elif re.search(r'[\uAC00-\uD7AF]', text):
        return "fonts/NotoSansCJKkr-Regular.otf"
    elif re.search(r'[\u4E00-\u9FFF]', text):
        return "fonts/NotoSansSC-Regular.ttf"
    elif re.search(r'[\u0900-\u097F]', text):
        return "fonts/NotoSansDevanagari-Regular.ttf"
    else:
        return "fonts/NotoSans-Regular.ttf"


def export_srt(segments, srt_path):
    subs = []
    for i, segment in enumerate(segments, start=1):
        subs.append(srt.Subtitle(index=i,
                                 start=timedelta(seconds=segment["start"]),
                                 end=timedelta(seconds=segment["end"]),
                                 content=segment["text"]))
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))


def burn_subtitles_with_ffmpeg(video_path, srt_path, output_path):
    command = [
        "ffmpeg", "-y", "-i", video_path, "-vf", f"subtitles={srt_path}",
        "-c:a", "copy", output_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise Exception(f"FFmpeg subtitle burning failed: {result.stderr.decode()}")
