import requests
import os
import json
import sys
from collections import Counter

PAGE_LIMIT = 10
DATA_DIRECTORY = 'data'
GITHUB_API_BASE = 'https://api.github.com'
API_USERNAME_ENDPOINT = GITHUB_API_BASE + '/users/{}'
API_STARRED_REPO_ENDPOINT = GITHUB_API_BASE + '/users/{}' + '/starred'


def user_exists(username):
    url = API_USERNAME_ENDPOINT.format(username)
    user_response = requests.get(url)
    return user_response.status_code == 200


def create_data_filename(username):
    return DATA_DIRECTORY + '/' + username + '.json'


def find_next_link(link_header):
    links = requests.utils.parse_header_links(link_header.rstrip('>').
                                              replace('>,<', ',<'))
    for link in links:
        if link['rel'] == 'next':
            return link['url']
    return ''


def fetch_repos(username):
    url = API_STARRED_REPO_ENDPOINT.format(username)

    repos = []

    page = 1

    print("Fetching starred repos for user: {}".format(username))

    while True:
        print("Getting Page: {}, Url: {}".format(page, url))
        response = requests.get(url)
        repos.extend(response.json())
        next_link = find_next_link(response.headers['Link'])
        if next_link == '':
            break
        url = next_link
        page += 1
        if page > PAGE_LIMIT:
            print("Page limit reached. Ending search.")
            break

    print("Fetching Complete. Fetched {} repos".format(len(repos)))

    return repos


def find_data_file(username):
    file_name = create_data_filename(username)
    if os.path.exists(file_name):
        print("Found data file: {}".format(file_name))
        repos = []
        with open(file_name) as f:
            repos = json.load(f)
        return repos
    raise FileNotFoundError


def save_data_file(username, repos):
    if not os.path.exists(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY, 493)
    file_name = create_data_filename(username)
    with open(file_name, 'w') as outfile:
        json.dump(repos, outfile)


def print_languages_profile(repos):
    languages = [repo['language'] for repo in repos]
    language_counter = Counter(languages)
    language_dict = dict(language_counter)
    language_dict.pop(None, None)
    sorted_language_profile = [(k, language_dict[k]) for k in sorted(
        language_dict, key=language_dict.get, reverse=True)]
    for k, v in sorted_language_profile:
        print("{:12} : {}".format(k, v))


def main():
    if len(sys.argv) != 2:
        print("You need to supply your Github username.\n" +
              "Usage: python3 telescope.py <username>")
        raise SystemExit

    username = sys.argv[1]
    print("Username: {}".format(username))

    if not user_exists(username):
        print("User {} doesn't exist".format(username))
        raise SystemExit

    repos = []

    try:
        repos = find_data_file(username)
    except FileNotFoundError:
        print("Data file not found. Preparing to fetch")
        repos = fetch_repos(username)
        save_data_file(username, repos)

    print("Total starred repos: {}".format(len(repos)))
    print_languages_profile(repos)


if __name__ == '__main__':
    main()
