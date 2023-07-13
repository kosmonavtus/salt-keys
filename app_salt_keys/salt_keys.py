from app_salt_keys.config import Settings
from subprocess import run, STDOUT, PIPE
from subprocess import CalledProcessError
import json


config = Settings()


def _get_cmd_param(param: str, key='str') -> list:
    match param:
        case 'check':
            return [config.bin_path, "--list=accepted", "--out=json"]
        case 'accept':
            return [config.bin_path, f"--accept={key}", "--out=json", "--yes"]
        case 'delete':
            return [config.bin_path, f"--delete={key}", "--out=json", "--yes"]
        case _:
            return []


def chek_keys_in_accepted(key: str) -> bool:
    kyes_dict = key_accepted_check()
    if key in kyes_dict['minions']:
        return True
    else:
        return False


def key_accepted_check() -> dict:
    cmd = _get_cmd_param('check')
    try:
        output = run(cmd, stdout=PIPE, stderr=STDOUT, text=True, cwd=config.salt_worck_dir)
        json_output = json.loads(output.stdout)
        return json_output
    except (CalledProcessError, FileNotFoundError, PermissionError) as e:
        raise e


def key_accept(key: str) -> bool:
    cmd = _get_cmd_param('accept', key)
    try:
        output = run(cmd, stdout=PIPE, stderr=STDOUT, text=True, cwd=config.salt_worck_dir)
        if output.stdout ==  f"The key glob '{key}' does not match any unaccepted keys.\n":
            return False
        elif output.stdout == f"Key for minion {key} accepted.\n":
            return True
        else:
            return False
    except (CalledProcessError, FileNotFoundError, PermissionError) as e:
        raise e


def key_delete(key: str) -> bool:
    cmd = _get_cmd_param('delete', key)
    try:
        run(cmd, stdout=PIPE, stderr=STDOUT, text=True, cwd=config.salt_worck_dir)
        return True
    except (CalledProcessError, FileNotFoundError, PermissionError) as e:
        raise e
