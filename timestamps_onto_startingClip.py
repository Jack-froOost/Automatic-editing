from sort_videos_based_on import sort_videos, get_video_paths
import subprocess
import os

def get_video_duration(filename):
    """
    Gets the duration of a video file using ffprobe.
    Returns the duration in seconds as a float.
    """
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        filename
    ]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        duration = float(result.stdout.strip())
        return duration
    except ValueError:
        return None
    except FileNotFoundError:
        print("Error: ffprobe not found. Ensure FFmpeg is installed and in your system's PATH.")
        return None


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        if minutes >= 10:
            return f"{hours:01d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{hours:01d}:{minutes:01d}:{secs:02d}"
    else:
        if minutes >=10:
            return f"{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:01d}:{secs:02d}"            


def generate_timestamps(sorted_paths, output_file="timestamps.txt", timestamp_mode='manual'):
    """
    Docstring for generate_timestamps
    
    :param output_file: path to output timestamp text folder
    :param Sorting_mode: sorting videos mode, manual / creation / alpha
    :param timestamp_mode: timestamp mode, "manual": you edit the videos on the text file before continuing, "automatic" (TODO)
    """


    lines = []
    current_time = 0.0

    for path in sorted_paths:
        clip_duration = get_video_duration(path)
        timestamp     = format_time(current_time)
        title         = os.path.splitext(os.path.basename(path))[0]
        if current_time > 0:
            lines.append(f"{timestamp:<12} {title}" )
        current_time += clip_duration

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Return the text for later use
    return "\n".join(lines)


import arabic_reshaper
from bidi.algorithm import get_display

def reshape_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)



from PIL import Image, ImageDraw, ImageFont
def render_text_to_image(text, output_path='img.png', font_size=40, text_color="black", outline=True, max_width=1000,padding=20,
                         font_path = r"C:\Windows\Fonts\arial.ttf"):
    # Use monospaced font to preserve spacing
    # font_path = r"C:\Windows\Fonts\arial.ttf"  # Consolas
    font = ImageFont.truetype(font_path, size=font_size)

    # Split text into lines exactly as written
    lines = text.splitlines()

    # Measure line height
    line_height = font.getbbox("A")[3] + 10
    img_height = line_height * len(lines) + padding * 2

    # Create transparent image
    img = Image.new("RGBA", (max_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outline settings
    stroke_color = "white" if text_color == "black" else "black" if outline else None
    stroke_width = 2 if outline else 0

    # Draw each line
    y = padding
    for line in lines:
        if any('\u0600' <= c <= '\u06FF' for c in line): # contains Arabic
            line = reshape_arabic(line)
        draw.text(
            (padding, y),
            line,
            font=font,
            fill=text_color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color
        )
        y += line_height

    # Save PNG
    img.save(output_path, format="PNG")
    return img



import numpy as np
def ffmpeg_overlay_png(input_video, overlay_png, output_video, start=5, duration=12.5):
    end_time = start + duration
    #say resolution is 1920x1080, y -> 100 for timestamps to appear seems appropriate..
    #set y = max((H-h)/2,0) to be in the center of the screen for any resolution instead of hardcoding it..
    cmd = [
    "ffmpeg",
    "-stats", "-v", "error",
    "-threads", "0", # use all cores
    "-i", input_video,
    "-i", overlay_png,
    "-filter_complex",
    (f"[0:v][1:v]overlay=x=10:y='100':enable='between(t,{start},{end_time})'"),
    "-c:a", "copy",
    "-c:v", "libx264",
    "-crf", "18",
    "-preset", "superfast",
    output_video
    ]
    subprocess.run(cmd)



if __name__ == "__main__":
    folder = r"C:\Users\Pc\Desktop\Teaching\temp"

    paths = get_video_paths(folder)
    sorted_paths = sort_videos(paths, mode="creation")

    timestamps_text = generate_timestamps(sorted_paths)
    print("Applying timestamps to starting clip: ")
    img = render_text_to_image(timestamps_text, font_size = 40, text_color = "black",
                                outline = True, max_width = int(1920*0.8), padding = 20)

    # Create modified starting clip
    print("Creating the video:")
    ffmpeg_overlay_png(input_video=sorted_paths[0], overlay_png=r'C:\Users\Pc\Desktop\programming\Python\Teaching scripts\img.png',
                        output_video="starting_clip_modified.mp4" )
    # Save it
    modified_start_path = os.path.join(folder, "starting_clip_modified.mp4")
    # for the next step, you'd probably want to do something like:
    sorted_paths[0] = modified_start_path
    # Now sorted_paths is ready to be concatnated... !
