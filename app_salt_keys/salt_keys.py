from subprocess import run, STDOUT, PIPE
from subprocess import CalledProcessError
import json


def key_accepted_check(salt_worck_dir: str, bin_path: str) -> dict:
    cmd = [bin_path, "--list=accepted", "--out=json"]
    try:
        output = run(cmd, stdout=PIPE, stderr=STDOUT, text=True, cwd=salt_worck_dir)
        json_output = json.loads(output.stdout)
        return json_output
    except (CalledProcessError, FileNotFoundError, PermissionError) as e:
        raise e


def key_accept(salt_worck_dir: str, key: str, bin_path: str) -> bool:
    cmd = [bin_path, f"--accept={key}", "--out=json"]
    try:
        run(cmd, stdout=PIPE, stderr=STDOUT, text=True, cwd=salt_worck_dir)
        return True
    except (CalledProcessError, FileNotFoundError, PermissionError) as e:
        raise e


def key_delete(salt_worck_dir: str, key: str, bin_path: str) -> bool:
    cmd = [bin_path, f"--delete={key}", "--out=json"]
    try:
        run(cmd, stdout=PIPE, stderr=STDOUT, text=True, cwd=salt_worck_dir)
        return True
    except (CalledProcessError, FileNotFoundError, PermissionError) as e:
        raise e
