config_info = {
    "record": False,
    "sleep": 600,
    "fileLen": 1,
    "rate": 8000,
}

ping_time = 0


def get_config_info():
    return config_info


def update_config_info(key, value):
    config_info[key] = value
    return config_info
