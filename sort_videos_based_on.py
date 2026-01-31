import os
from glob import glob

folder = r"C:\Users\Pc\Desktop\Teaching\temp"



def get_video_paths(folder):
    return glob(os.path.join(folder, "*.mp4"))


# based on creation time:
def sort_by_creation(paths):
    return sorted(paths, key=os.path.getctime)


# alphabeticaly 
def sort_alphabetically(paths):
    return sorted(paths, key=lambda p: os.path.basename(p).lower())


# user edits the text file manually
def manual_sort(paths, list_path="inputs.txt"):
    # Write initial list
    with open(list_path, "w", encoding="utf-8") as f:
        for path in sorted(paths, key=lambda p: os.path.basename(p).lower()):
            f.write(path + "\n")

    input(f"Edit {list_path} to reorder the videos, once saved your edits press Enter.")

    # Read back edited order
    with open(list_path, "r", encoding="utf-8") as f:
        edited = [line.strip() for line in f.readlines() if line.strip()]

    return edited


# wrapper method of sorting paths
def sort_videos(paths, mode="creation"):
    """

    :param paths: list of paths of videos from the temp folder.
    :param mode:  mode of sorting, "creation": sort by creation date, "alpha": sort alphabeticly, "manual": prompts the user to manually sort the 
    text file, "4th print": sort the videos based on the fourth print excercise number, "3rd print".

    returns a list of the sorted paths.
    """
    if mode == "creation":
        return sort_by_creation(paths)
    elif mode == "alpha":
        return sort_alphabetically(paths)
    elif mode == "manual":
        return manual_sort(paths)
    else:
        raise ValueError(f"Unknown sorting mode: {mode}")
    
# if __name__ == "__main__":
