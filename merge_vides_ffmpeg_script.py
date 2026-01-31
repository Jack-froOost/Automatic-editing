import os
import subprocess
from sort_videos_based_on import sort_videos, get_video_paths

folder = r"C:\Users\Pc\Desktop\Teaching\temp"

# Create file list using paths of videos
def write_ffmpeg_list(paths, output="inputs.txt"):
    with open(output, "w", encoding="utf-8") as f:
        for p in paths:
            f.write(f"file '{p}'\n")


# Run ffmpeg concat
def run_ffmpeg(list_file, output_path):
    """
    :param list_file: path to input text file; text file of videos orginized to be concatnated.
    :param output_path: path to output video file.
    """
    subprocess.run([
        "ffmpeg",
        "-hide_banner",  "-loglevel", "info", "-stats",
        "-threads", "0", # use all cores
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_path
    ])



#wrapper method that writes sorted paths to input.txt, creates the final video.
def create_video(video_paths, input_txt_path, output_path):

    write_ffmpeg_list(video_paths, output=input_txt_path)
    run_ffmpeg(input_txt_path, output_path)
