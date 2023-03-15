import os
import shutil

def list_empty_dir(path, list):
    list_folders = os.listdir(path)
    for folder in list_folders:
        new_path = os.path.join(path, folder)
        if os.path.isdir(new_path):
            if len(os.listdir(new_path)) == 0:
                list.append(new_path)
            else:
                list_empty_dir(new_path, list)

def main():
    list_empty = []
    path_git_folder = ".\\git"
    list_empty_dir(path_git_folder, list_empty)
    print(list_empty)
    for folder in list_empty:
        try:
            print(folder)
            shutil.rmtree(folder)
        except Exception as e:
            print("ERROR: failed to delete folder: ", folder, e)
    list_empty = []
    list_empty_dir(path_git_folder, list_empty)
    return list_empty

if __name__ == "__main__":
    l = [0]
    while len(l) > 0:
        l = main()