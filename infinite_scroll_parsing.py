import requests
from bs4 import BeautifulSoup

def inf_scr_prs(parse_from="https://pikabu.ru/", page_num=1):
    '''
    :param parse_from:
    :param page_num:
    :return: data array, posts number / -1, error name
    '''

    # get the feedkey
    # Chrome/108.0.0.0 or Mozilla/5.0
    try:
        r = requests.get(parse_from, params={'q': 'goog'}, headers={'User-Agent': 'Chrome/108.0.0.0'})
        soup = BeautifulSoup(r.text, "lxml")
        all_stats = soup.find('main', class_='main__inner').find('script').text
        feed_key = all_stats[all_stats.find('feedKey') + 10:-2]
    except: return -1, 'Feedkey get error'

    # parse with good feedkey
    success_data = []
    try:
        for i in range(1, page_num + 1):
            url_to_parse = f'https://pikabu.ru/ajax/?key={feed_key}&page={i}'
            r1 = requests.get(url_to_parse, params={'q': 'goog'}, headers={'User-Agent': 'Chrome/108.0.0.0'})

            # split to stories
            raw_separated_posts = r1.text.split('_start-->')[1:]

            # skip adds, keep posts
            for j in range(len(raw_separated_posts)):
                if "story story_tags-at-top" in raw_separated_posts[j]:
                    pass
                else:
                    # success_data.append(raw_to_useful(raw_separated_posts[j]))
                    success_data.append(raw_separated_posts[j])
            print(f'page {i} is parsed')
    except: return -1, 'Long parsing error'

    for i in range(len(success_data)):
        success_data[i] = raw_to_useful(success_data[i])
    return success_data, len(success_data)

def raw_to_useful(raw_post):
    # todo works good but need to check
    '''
    :param raw_post:
    :return: useful_data
    '''
    raw_post = raw_post.replace('\\"', '').replace('  ', ' ').split(' ')
    search_data = ['data-story-id=',
                   'data-rating=',
                   'data-author-name=',
                   'data-url='
                   ]
    useful_data = []
    for data in search_data:
        for each in raw_post:
            if data in each:
                useful_data.append(each)
                break

    # очистка полезной инфы, оставляем только значение
    for i in range(len(useful_data)):
        useful_data[i] = useful_data[i].split('=')[1]

    # для постов из свежего добавляеи дата рейтинг 0

    if len(useful_data) == 3:
        useful_data.insert(1, '0')

    if useful_data[2] == '\\u0410\\u043d\\u043e\\u043d\\u0438\\u043c':
        useful_data[2] = f"Anonim"

    # очистка ссылки
    good_link = useful_data[3].replace(f'%2F', f'/').replace(f'%3A', f':')
    useful_data[3] = good_link


    return useful_data

