__author__ = "MrStaf"
__version__ = "1.0.0"
__license__ = "GNU General Public License v2.0"

import os
import random
import shutil
import stat
import subprocess

from dotenv import load_dotenv
load_dotenv()
pat_token = os.environ.get("PAT_TOKEN")
repo = os.environ.get("REPO")

PATH_GIT_FOLDER = ".\\git"
PATH_GIT = ".\\git\\cmd\\git.exe"

def readonly_handler(func, path, execinfo):
    """
    Remove the read-only flag on the file
    func: function to be called
    path: path to the file
    execinfo: info about the error
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone():
    """
    Try to clone the repo
    return True if success, False if failed
    """
    print()
    subprocess.run(f"{PATH_GIT} clone https://{pat_token}@github.com/{repo}", capture_output=False, stdout=subprocess.DEVNULL)
    res = False
    try:
        with open("test\\README.md", "r") as f:
            res = f.read() == "# test"
            f.close()
    except:
        res = False
    while os.path.exists("test"):
        try:
            shutil.rmtree("test", onerror=readonly_handler)
        except:
            pass
    print(f"Command status : {'success' if res else 'failed'}")
    return res

# list of all the files in the folder
def recur_list_files(path: str, list: list):
    """
    Recursively list all the files in the folder
    path: path to the folder
    list: list of files
    """
    if os.path.isdir(path):
        for file in os.listdir(path):
            recur_list_files(os.path.join(path, file), list)
    else:
        list.append(path)

needed_files = []

def main(**kwargs):
    """
    Main function of the script to delete files in the PATH_GIT_FOLDER folder, then try to clone the repo
    and if it fails, add the files back to the folder

    This is hacky and not optimized, but it works :)
    """
    # N: number of files to delete at the same time
    N = kwargs.get("N", 1)
    if type(N) != int:
        raise TypeError("N must be an integer")
    
    # list of all the files in the folder
    list_ = []
    recur_list_files(PATH_GIT_FOLDER, list_)

    # shuffle the list to make it funnier
    random.shuffle(list_)
    
    list_chuncks = [list_[i:i + N] for i in range(0, len(list_), N)]
    for chunck in list_chuncks:
        print("")
        for file in chunck:
            print(f"[{list_.index(file) + 1}\t/{len(list_)}] ({round((list_.index(file) + 1) / len(list_) * 100, 2)}%) Working on {file}", end="\r")
            # we don't want to delete any git.exe file
            if "git.exe" in file:
                continue
            else:
                try:
                    # copy the file to "./tmp" with the same path as the original file
                    os.makedirs(os.path.dirname(".\\tmp" + file[1:]), exist_ok=True)
                    shutil.copy(file, ".\\tmp" + file[1:])
                    os.remove(file)
                except:
                    continue
        
        if clone():
            for file in chunck:
                if "git.exe" in file:
                    continue
                os.remove(".\\tmp" + file[1:])
        else:
            print("ERROR : failed to clone")
            print("trying to add the files back to the folder")
            for file in chunck:
                if "git.exe" in file:
                    continue
                print(file)
                # add file back to the folder
                while not os.path.exists(file):
                    shutil.copy(".\\tmp" + file[1:], file)
                # delete the file from "./tmp"
                os.remove(".\\tmp" + file[1:])
                # If N == 1, save the file_path to the file "needed.txt"
                # so we can track essential files
                if N == 1:
                    with open("needed.txt", "a") as f:
                        f.write(file + "\n")
                        f.close()
        file = chunck[-1]
        if (list_.index(file) + 1) / len(list_) * 100 > 90:
            print("\n90% done, exiting")
            print("try to run the script again to finish the job")
            print("N recommended: 100 then 10 then 1")
            exit()

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            # save the error to the file
            with open("error.txt", "a") as f:
                f.write(str(e) + "\n")
                f.close()