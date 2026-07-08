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
            return f"{hours:01d}:0{minutes:01d}:{secs:02d}"
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
from PIL import Image, ImageFont, ImageDraw

from PIL import Image, ImageFont, ImageDraw

from PIL import Image, ImageFont, ImageDraw

def render_text_to_image(text, output_path='img.png', font_size=40, text_color="black", outline=True, 
                         max_width=1920, max_height=1080, padding=20, min_font_size=12,
                         font_path=r"C:\Windows\Fonts\arial.ttf"):
    
    lines = text.splitlines()
    current_font_size = font_size
    vertical_buffer = 50 

    while current_font_size >= min_font_size:
        font = ImageFont.truetype(font_path, size=current_font_size)
        
        # FIX: Get the true typographical metrics of the font
        ascent, descent = font.getmetrics()
        
        # Proportional line height: true text height + 35% breathing room
        line_height = int((ascent + descent) * 1.1)  
        
        total_text_height = line_height * len(lines)
        required_img_height = total_text_height + (padding * 2) + (vertical_buffer * 2)

        if required_img_height <= max_height:
            break
            
        current_font_size -= 2
    else:
        font = ImageFont.truetype(font_path, size=min_font_size)
        ascent, descent = font.getmetrics()
        line_height = int((ascent + descent) * 1.35)
        required_img_height = max_height

    final_height = min(required_img_height, max_height)

    img = Image.new("RGBA", (max_width, final_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    stroke_color = "white" if text_color == "black" else "black" if outline else None
    stroke_width = 2 if outline else 0

    y = padding + vertical_buffer
    
    for line in lines:
        if y + line_height > final_height - (padding + vertical_buffer):
            break

        if any('\u0600' <= c <= '\u06FF' for c in line): 
            try:
                line = reshape_arabic(line)
            except NameError:
                pass

        draw.text(
            (padding, y),
            line,
            font=font,
            fill=text_color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color
        )
        y += line_height

    img.save(output_path, format="PNG")
    return img


import numpy as np
def ffmpeg_overlay_png(input_video, overlay_png, output_video, start=5, duration=12.5, position="center"):
    end_time = start + duration
    #say resolution is 1920x1080, y -> 100 for timestamps to appear seems appropriate..
    #set y='max((H-h)/2,0)' to be in the center of the screen for any resolution instead of hardcoding it..
    # in the future u could do a position parameter that sets the x and y values accordingly, for now we will just do left onlu.
    # if position == "left":
    #     overlay = "overlay=x=10:y='max((H-h)/2,0)'"
    # else:
    #     overlay = f"overlay=x='max((W-w)/2,0)':y=20"
    cmd = [
    "ffmpeg",
    "-stats", "-v", "error",
    "-threads", "0", # use all cores
    "-i", input_video,
    "-i", overlay_png,
    "-filter_complex",
    (f"[0:v][1:v]overlay=x=10:y='max((H-h)/2,0)':enable='between(t,{start},{end_time})'"),
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
