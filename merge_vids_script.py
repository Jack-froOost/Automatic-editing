from moviepy import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import os
from glob import glob
from tqdm import tqdm


#get path to folder ...
path = r'C:\Users\Pc\Desktop\Teaching\temp'
# print(f'paths: {os.listdir(path)}')
# print(glob(f'{path}\*.mp4'))



#TODO: order the tiles based on creation time / time added to file / sorted alphabeticly / based on 4th\3rd print value
videoPaths = glob(os.path.join(path, "*.mp4"))

videosToConcatnate = []
for videoPath in tqdm(videoPaths, desc="Loading videos"):
    #load video
    clip = VideoFileClip(videoPath)
    videosToConcatnate.append(clip)

final_clip  = concatenate_videoclips(videosToConcatnate)
output_path = os.path.join(path, 'Final_Video_!.mp4')
final_clip.write_videofile(output_path)


# Cleanup
final_clip.close() 
for clip in videosToConcatnate:
    clip.close()