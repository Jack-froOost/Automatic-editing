import os
from merge_vides_ffmpeg_script import create_video
from sort_videos_based_on import sort_videos, get_video_paths
from timestamps_onto_startingClip import generate_timestamps, render_text_to_image, ffmpeg_overlay_png

def cli_main():
    #global file paths:
    folder = r"C:\Users\Pc\Desktop\Teaching\temp"  #path to directory of stored clips (to be concatnated / timestamps extracted ..)
    sorted_videos_path= 'inputs.txt' #order of concatination, video paths
    timestamps_file = "timestamps.txt"
    overlay_path    = "timestamps_overlay.png" #timestamp image will be saved here
    output_video    = "starting_clip_modified.mp4" #temp start cilp saved here

    print("="*50)
    print("🎬 Timestamped Video Compiler")
    print("="*50)
    print("Make sure your desired videos are in the target folder. (target folder: C:\\Users\\Pc\\Desktop\\Teaching\\temp)")
    input("Once ready, press Enter to continue...")

    import time
    start_time = time.perf_counter()
    
    # Step 1: Get video paths
    video_paths = get_video_paths(folder)
    print(f"Found {len(video_paths)} video(s).")

    # Step 2: Choose sorting method
    print("\nChoose sorting method: (default /press enter: manual)")
    print("1 - By creation time")
    print("2 - By filename")
    print("3 - Manualy sort them (videos will be in 'inputs.txt')")
    
    cont = 'y'
    while cont=='y':
        sort_choice = input("Enter choice (1 or 2 or 3): ").strip()
        if sort_choice == '1':
            sort_mode = "creation"
        elif sort_choice=='2':
            sort_mode = "alpha"
        else:
            sort_mode = "manual"

        sorted_paths = sort_videos(video_paths, mode=sort_mode, temp_videos_paths=sorted_videos_path)
        print(f"Sorted paths: {sorted_paths}.")
        cont = input(f"\ndo you want to redo sorting (y/n) ? ")

    # Step 3: Generate timestamps
    timestamps_text = generate_timestamps(sorted_paths, output_file=timestamps_file)
    print(f"\n{"="*50}")
    print("Generated timestamps:")
    print(timestamps_text)
    print("="*50)

    # Segway: if you'd like to change the timestamps headlines for some extra details on the videos
    print(f"\n{"="*50}")
    change_timestamps = input("would you like to customize the timestamps (y/n) ? ")
    change_timestamps = (change_timestamps == 'y')
    if change_timestamps:
        input(f"Edit {timestamps_file} and customize the timestamps, once saved your edits press Enter.")

        # Read back edited timestamps
        with open(timestamps_file, "r", encoding="utf-8") as f:
            timestamps_text = [line.strip() for line in f.readlines() if line.strip()]
            timestamps_text = "\n".join(timestamps_text)
        print("The Custom Generated timestamps:")
        print(timestamps_text)
    print("="*50)

    # Step 4: Choose text style; everything after this is just editing, no user input required.
    print(f"\n{"="*50}")
    print("Setting parameters")
    print("Choose timestamp text color:")
    text_color = input("Enter color (e.g. black, white, red): ").strip()
    outline_choice = input("Add outline? (y/n): ").strip().lower()
    final_output   = f"{input("Enter the desired final video name: ")}.mp4"
    text_start_time= int(input("when would you like the text to appear? "))
    outline = (outline_choice == "y")
    print("="*50)

    # Step 5: Render timestamp image
    print(f"\n{"="*50}")
    print("Creating the video:")
    Editing_time_start = time.perf_counter()

    render_text_to_image(
        timestamps_text,
        output_path=overlay_path,
        font_size=45,
        text_color=text_color,
        outline=outline,
        max_width=int(1920 * 0.7),
        padding=20
    )
    print(f"Timestamp image saved to: {overlay_path}.")

    # Step 6: Overlay image onto starting clip
    output_video = output_video
    #if output_video already exisits, delete it
    if os.path.exists(output_video):
        os.remove(output_video)
    print("Creating the modified starting clip video..")
    ffmpeg_overlay_png(
        input_video=sorted_paths[0],
        overlay_png=overlay_path,
        output_video=output_video,
        start=text_start_time
    )
    print(f"Modified starting clip saved to: {output_video}")

    # Step 7: Update sorted paths
    sorted_paths[0] = output_video

    # Step 8: Concatenate videos
    final_output = os.path.join(folder, final_output)
    print("Concatinating videos:")
    create_video(sorted_paths, sorted_videos_path, final_output)

    end_time = time.perf_counter()
    
    print(f"\n\n🎉 Final video created: {final_output}")
    print(f"Total Elapsed time: {(end_time - start_time)}.\nTime to Edit: {end_time-Editing_time_start}.")
    print(f"- Frost.")    
    print(f"{"="*50}")

if __name__ == "__main__":
    cli_main()
