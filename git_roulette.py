import os
import random
import shutil
import stat
import subprocess
from dotenv import load_dotenv
load_dotenv()
path_git_folder = ".\\git"
path_git = ".\\git\\cmd\\git.exe"
pat_token = os.environ.get("PAT_TOKEN")
repo = os.environ.get("REPO")

def readonly_handler(func, path, execinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone():
    # output of the command must be muted
    subprocess.run(f"{path_git} clone https://{pat_token}@github.com/{repo}", capture_output=False, stdout=subprocess.DEVNULL)
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
    print("res: ", res)
    return res

# list of all the files in the folder
def recur_list_files(path, list):
    if os.path.isdir(path):
        for file in os.listdir(path):
            recur_list_files(os.path.join(path, file), list)
    else:
        list.append(path)

needed_files = []

def main(**kwargs):
    N = kwargs.get("N", 1)
    if type(N) != int:
        raise TypeError("N must be an integer")
    # list of all the files in the folder
    list_ = []
    recur_list_files(path_git_folder, list_)
    # shuffle the list
    random.shuffle(list_)
    
    list_chuncks = [list_[i:i + N] for i in range(0, len(list_), N)]
    for chunck in list_chuncks:
        for file in chunck:
            print(f"Working on {file} which is {list_.index(file) + 1} out of {len(list_)} ({round((list_.index(file) + 1) / len(list_) * 100, 2)}%)                                  ", end="\r")
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
                # delete the file
        if clone():
            print("success")
            for file in chunck:
                if "git.exe" in file:
                    continue
                os.remove(".\\tmp" + file[1:])
        else:
            print("ERROR : failed to clone")
            for file in chunck:
                if "git.exe" in file:
                    continue
                print(file)
                # add file back to the folder
                while not os.path.exists(file):
                    shutil.copy(".\\tmp" + file[1:], file)
                # delete the file from "./tmp"
                os.remove(".\\tmp" + file[1:])
                # add the file to the file : "needed.txt"
                if N == 1:
                    with open("needed.txt", "a") as f:
                        f.write(file + "\n")
                        f.close()
            print("added to needed.txt")
        file = chunck[-1]
        if (list_.index(file) + 1) / len(list_) * 100 > 90:
            break

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            # save the error to the file
            with open("error.txt", "a") as f:
                f.write(str(e) + "\n")
                f.close()