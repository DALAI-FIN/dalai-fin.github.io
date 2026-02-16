import csv
import sys
import os
import shutil
from dateutil import parser

LANGUAGES = ['en', 'fi', 'zh']
META_ENTRIES = ['title', 'tagline', 'categories', 'image', 'meta']
EXAMPLE_CSV_FILE = 'dalai-fin_blog - example.csv'

POST_TEMPLATE = """---
layout: post
{metadata}
---

{content}

"""

if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else EXAMPLE_CSV_FILE
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' does not exist.")
        sys.exit(1)
    for lang in LANGUAGES:
        shutil.rmtree(f"_posts/{lang}", ignore_errors=True)
        os.makedirs(f"_posts/{lang}", exist_ok=True)
    with open(csv_file, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for lang in LANGUAGES:
                if lang not in row or not row[lang]:
                    continue
                metadata = f'lang: {lang}\n'
                date = parser.parse(row['date'])
                filename = f"{date.strftime('%Y-%m-%d')}-{row['title'].lower().replace(' ', '-')}.md"
                handle = f'{date.strftime("%Y/%m/%d")}/{row["title"].lower().replace(" ", "-")}'
                if 'categories' in row and row['categories']:
                    handle = row['categories'].lower().replace(' ', '-') + '/' + handle
                metadata += f"handle: {handle}\n"
                for entry in META_ENTRIES:
                    if entry not in row or not row[entry]:
                        continue
                    metadata += f"{entry}: {row[entry]}\n"
                print(f"Creating post: {filename}")
                with open(f"_posts/{lang}/{filename}", "w", encoding="utf-8") as post_file:
                    post_file.write(POST_TEMPLATE.format(metadata=metadata, content=row[lang]))