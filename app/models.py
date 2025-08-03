from datetime import datetime

url_store = {}


def insert_url_mapping(short_code, original_url):
    url_store[short_code] = {
        "short_code": short_code,
        "original_url": original_url,
        "created_at": datetime.utcnow().isoformat(),
        "clicks": 0
    }

def get_url(short_code):
    return url_store.get(short_code)


def increment_clicks(short_code):
    if short_code in url_store:
        url_store[short_code]["clicks"] += 1


def get_stats(short_code):
    return get_url(short_code)

def check_url_already_exist(original_url):
    for data in url_store.values():
        if data["original_url"] == original_url:
            return data["short_code"]
    return False
