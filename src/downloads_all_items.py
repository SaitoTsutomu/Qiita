import datetime
import json
import os
import re
import time
from math import ceil

import requests


def downloads_all_items():
    # QIITA_API_TOKEN: https://qiita.com/settings/applications
    headers = {
        "Authorization": f"Bearer {os.environ['QIITA_API_TOKEN']}",
        "Accept": "application/json",
    }
    page = 1
    with open("items.md", "w") as fpt:
        fpt.write("Posts on Qiita\n\n")
        fpt.write(f"created {datetime.date.today()}\n\n")
        while True:
            url = f"https://qiita.com/api/v2/authenticated_user/items?page={page}&per_page=100"
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                print(f"Error at page {page} {res.status_code}")
                break
            print("Rate-Remaining:", res.headers["Rate-Remaining"])
            items = json.loads(res.text)
            for item in items:
                if item["private"]:
                    continue
                title = item["title"]
                title = re.sub("<[^>]*?>", "", title)  # タグ削除
                title = re.sub("[~`!@#$%^&*=+{}\\|;:\"',<.>/?]", "", title)  # 記号削除
                fpt.write(f"- [{title}]({item['url']})\n")
                drc = f"items/{item['created_at'][:4]}"
                os.makedirs(drc, exist_ok=True)
                with open(f"{drc}/{title}.md", "w") as fp:
                    write_item(fp, item)
            page += 1
            if page > ceil(int(res.headers["Total-Count"]) / 100):
                break
            time.sleep(1)


def write_item(fp, item):
    fp.write(f"title: {item['title']}\n")
    fp.write(f"tags: {' '.join(d['name'] for d in item['tags'])}\n")
    fp.write(f"url: {item['url']}\n")
    fp.write(f"created_at: {item['created_at'].replace('T', ' ')}\n")
    fp.write(f"updated_at: {item['updated_at'].replace('T', ' ')}\n")
    fp.write(f"body:\n\n{item['body']}\n")


if __name__ == "__main__":
    downloads_all_items()
