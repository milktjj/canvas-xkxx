config_info = {
    "record": True,
    "sleep": 600,
    "fileLen": 15,
}

ping_time = 0


def get_config_info():
    return config_info


def update_config_info(key, value):
    config_info[key] = value
    return config_info
