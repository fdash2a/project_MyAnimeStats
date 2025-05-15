import requests
import json
import time


def get_top_100_anime(limit=100):
    anime_list = []
    per_page = 50
    pages = limit // per_page
    for page in range(1, pages + 1):
        url = f"https://api.jikan.moe/v4/top/anime?page={page}"
        response = requests.get(url)
        data = response.json()
        time.sleep(1)
        for item in data.get('data', []):
            anime = {
                'title': item['title'],
                'score': item['score'],
                'genres': [genre['name'] for genre in item['genres']],
                'year': item['year'],
                'studio': item['producers'][0]['name'] if item['producers'] else None,
                'type': 'top'
            }
            anime_list.append(anime)
    return anime_list


def get_low_rated_anime(page=200, limit=20):
    url = f"https://api.jikan.moe/v4/top/anime?page={page}&type=tv"
    response = requests.get(url)
    data = response.json()
    time.sleep(1)
    low_rated = []
    for item in data.get('data', [])[:limit]:
        anime = {
            'title': item['title'],
            'score': item['score'],
            'genres': [genre['name'] for genre in item['genres']],
            'year': item['year'],
            'studio': item['producers'][0]['name'] if item['producers'] else None,
            'type': 'low'
        }
        low_rated.append(anime)
    return low_rated


def save_to_json(data, filename="anime_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    top_anime = get_top_100_anime()
    low_rated_anime = get_low_rated_anime()
    all_anime = top_anime + low_rated_anime
    save_to_json(all_anime)


if __name__ == "__main__":
    main()
