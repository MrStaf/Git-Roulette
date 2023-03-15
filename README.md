
# **Git Roulette**

**Git Roulette** is a Python script that can help you reduce PortableGit size by removing random files and checking if the repository can still be cloned. It is designed to help you identify which files are necessary for your project and which ones can be safely removed to reduce the size of your repository.

## Installation

To use **Git Roulette**, you will need to clone this repository and set up a few things:

- Create a virtual environment for Python 3.6 or later
- Install the required dependencies using ``pip install -r requirements.txt``
- Create a new repository on GitHub which contain ``README.MD`` file as following.

```MD
# test
```

- Set up your ``.env`` file with your GitHub Personal Access Token (``PAT_Token``) to test the script and the repo name as following.

```bash
PAT_Token=your_token
REPO=username/repo_name
```

## Usage

To use **Git Roulette**, run the following command:

```bash
python git_roulette.py N
```

where N is the number of files to delete each epoch. You can experiment with different values of N to find the smallest number of files that your repository needs to remain functional.

The script will randomly select files from your repository and remove them one by one, testing the repository's portability after each deletion. The results will be displayed in the console, and the script will continue until the desired number of files has been deleted.

## Example

After running **Git Roulette** on PortableGit and the clone with PAT command, the number of files was reduced from 6100 to 23, and the size of the repository was reduced from 314 MB to 19.4 MB. Here are the commands that were used:

```bash
python git_roulette.py 100
python git_roulette.py 10
python git_roulette.py 1
```

Then I used delete_empty_folders.py to remove empty folders.

## Contributing

If you find any bugs or issues with **Git Roulette**, please submit a GitHub issue or a pull request. We welcome all contributions and feedback.

## License

**Git Roulette** is licensed under the GNU v2 License. See ``LICENSE`` for more information.
