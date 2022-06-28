import os
import requests
from urllib.parse import urlparse

from dotenv import load_dotenv


def shorten_link (token: str, url: str) -> str:
    """Returns a short link (bitlink)"""
    auth_header = {
        "Authorization" : f"Bearer {token}", 
        "Content-Type" : "application/json"
    }
    json_payload = {"long_url": f"{url}"}
    response = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=auth_header, json=json_payload)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks (token: str, url: str) -> int:
    """Returns the number of clicks on the bitlink"""
    auth_header = {
        "Authorization" : f"Bearer {token}",
        "Content-Type" : "application/json"
    }
    parsed_link = urlparse(url)
    bitlink = f"{parsed_link.netloc}{parsed_link.path}"
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary", headers=auth_header)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count 


def is_bitlink(token: str, url: str) -> bool:
    """Checks if the link is a bitlink"""
    auth_header = {
        "Authorization" : f"Bearer {token}",
        "Content-Type" : "application/json"
    }
    parsed_link = urlparse(url)
    bitlink = f"{parsed_link.netloc}{parsed_link.path}"
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}", headers=auth_header)
    return response.ok

def main():
    load_dotenv()
    BITLY_TOKEN = str(os.getenv("BITLY_TOKEN"))

    try:
        link = input("Введите ссылку: ")

        if is_bitlink(BITLY_TOKEN, link):
            print(count_clicks(BITLY_TOKEN, link))
        else:
            print(shorten_link(BITLY_TOKEN, link))

    except requests.exceptions.HTTPError as error:
        print(f"В работе программы возникла ошибка:\n{error}")


if __name__ == "__main__":
    main()