import os
import requests
import argparse
from urllib.parse import urlparse

from dotenv import load_dotenv


def shorten_link(token: str, url: str) -> str:
    """Returns a short link (bitlink)"""
    auth_header = {"Authorization": f"Bearer {token}"}
    json_payload = {"long_url": f"{url}"}
    response = requests.post(
        "https://api-ssl.bitly.com/v4/bitlinks",
        headers=auth_header,
        json=json_payload
    )
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(token: str, url: str) -> int:
    """Returns the number of clicks on the bitlink"""
    auth_header = {"Authorization": f"Bearer {token}"}
    parsed_link = urlparse(url)
    bitlink = f"{parsed_link.netloc}{parsed_link.path}"
    response = requests.get(
        f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary",
        headers=auth_header
    )
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def is_bitlink(token: str, url: str) -> bool:
    """Checks if the link is a bitlink"""
    auth_header = {"Authorization": f"Bearer {token}"}
    parsed_link = urlparse(url)
    bitlink = f"{parsed_link.netloc}{parsed_link.path}"
    response = requests.get(
        f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}",
        headers=auth_header
    )
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.getenv("BITLY_TOKEN")

    try:
        parser = argparse.ArgumentParser(
            description="Скрипт работает с сервисом bit.ly. Обычную ссылку\
            сокращает до вида https://bit.ly/ADCDEFG. При вводе \
            ссылки битлинк - выводит количество переходов по ней."
        )
        parser.add_argument(
            "link",
            help="Ссылка на сайт, либо короткая ссылка bitlink"
        )
        link = parser.parse_args().link

        if is_bitlink(bitly_token, link):
            print(
                f"Количество переходов по ссылке битли: "
                f"{count_clicks(bitly_token, link)}"
            )
        else:
            print(shorten_link(bitly_token, link))

    except requests.exceptions.HTTPError as error:
        print(f"В работе программы возникла ошибка:\n{error}")


if __name__ == "__main__":
    main()
