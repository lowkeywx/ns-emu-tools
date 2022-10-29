import eel
from config import yuzu_config
from repository.yuzu import get_all_yuzu_release_infos
from module.common import get_firmware_infos

eel.init("web")


def success_response(data=None, msg=None):
    return {'code': 0, 'data': data, 'msg': msg}


def exception_response(ex):
    return error_response(999, str(ex))


def error_response(code, msg):
    return {'code': code, 'msg': msg}


@eel.expose
def get_yuzu_config():
    return yuzu_config.to_dict()


@eel.expose
def get_yuzu_release_infos():
    try:
        return success_response(get_all_yuzu_release_infos())
    except Exception as e:
        return exception_response(e)


@eel.expose
def get_available_firmware_infos():
    try:
        return success_response(get_firmware_infos())
    except Exception as e:
        return exception_response(e)


@eel.expose
def install_yuzu(version):
    if not version or version == '':
        return {'msg': f'无效的版本 {version}'}
    from module.yuzu import install_yuzu
    return {'msg': install_yuzu(version)}


@eel.expose
def install_firmware(version):
    if not version or version == '':
        return {'msg': f'无效的版本 {version}'}
    from module.yuzu import install_firmware_to_yuzu
    return {'msg': install_firmware_to_yuzu(version)}


@eel.expose
def get_available_keys_info():
    from module.common import get_keys_info
    try:
        return success_response(get_keys_info())
    except Exception as e:
        return exception_response(e)


@eel.expose
def install_keys(name):
    if not name or name == '':
        return {'msg': f'无效的 key {name}'}
    from module.yuzu import install_key_to_yuzu
    return success_response(msg=install_key_to_yuzu(name))


@eel.expose
def detect_yuzu_version():
    from module.yuzu import detect_yuzu_version
    return {'yuzu_version': detect_yuzu_version()}


def can_use_chrome():
    """ Identify if Chrome is available for Eel to use """
    import os
    from eel import chrome
    chrome_instance_path = chrome.find_path()
    return chrome_instance_path is not None and os.path.exists(chrome_instance_path)


def main():
    from module.msg_notifier import update_notifier
    update_notifier('eel')
    if can_use_chrome():
        eel.start("index.html", port=0)
    else:
        eel.start("index.html", port=0, mode='user default')


if __name__ == '__main__':
    main()
