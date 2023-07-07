from subprocess import run, STDOUT, PIPE
from subprocess import CalledProcessError


def keys_accepted(git_repo_dir: str) -> dict:
    cmd = ["salt-kyes", "--list=accepted", "--out=json"]
    try:
        output = run(cmd, stdout=PIPE, stderr=STDOUT, text=True, cwd=git_repo_dir)
        return output.stdout
    except (CalledProcessError, FileNotFoundError, PermissionError) as e:
        raise e

def keys_accept(git_repo_dir: str, key: str) -> dict:
    cmd = ["salt-kyes", f"--accept={key}", "--out=json"]
    try:
        output = run(cmd, stdout=PIPE, stderr=STDOUT, text=True, cwd=git_repo_dir)
        return output.stdout
    except (CalledProcessError, FileNotFoundError, PermissionError) as e:
        raise e
    

def keys_delete(git_repo_dir: str, key: str) -> dict:
    cmd = ["salt-kyes", f"--delete={key}", "--out=json"]
    try:
        output = run(cmd, stdout=PIPE, stderr=STDOUT, text=True, cwd=git_repo_dir)
        return output.stdout
    except (CalledProcessError, FileNotFoundError, PermissionError) as e:
        raise e


