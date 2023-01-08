import requests
from bs4 import BeautifulSoup

def inf_scr_prs(parse_from="https://pikabu.ru/", page_num=1):
    '''
    :param parse_from:
    :param page_num:
    :return: data array, posts number, creates a txt file with parsed info.
    status = -1 in case error
    '''

    #get the feedkey
    # Chrome/108.0.0.0 or Mozilla/5.0
    dat = {'q': 'goog'}
    r = requests.get(parse_from, params=dat, headers={'User-Agent': 'Chrome/108.0.0.0'})

    try:
        soup = BeautifulSoup(r.text, "lxml")
        all_stats = soup.find('main', class_='main__inner').find('script').text
        feed_key = all_stats[all_stats.find('feedKey') + 10:-2]
    except: return (-1, 'Feedkey get error')

    #parse with good feedkey
    success_data = []
    try:
        for i in range(1, page_num + 1):
            url_to_parse = f'https://pikabu.ru/ajax/?key={feed_key}&page={i}'
            dat = {'q': 'goog'}
            r1 = requests.get(url_to_parse, params=dat, headers={'User-Agent': 'Chrome/108.0.0.0'})

            # split to stories
            raw_separated_posts = r1.text.split('<!--story_')[1::2]

            #skip adds, keep posts
            for j in range(len(raw_separated_posts)):
                if "story story_tags-at-top" in raw_separated_posts[j]: pass
                else: success_data.append(raw_to_useful(raw_separated_posts[j]))
        #write data to file
        with open('parsed_pikabu.txt', 'a') as file:
            for each in success_data: file.write(' '.join(each) + "\n")
        return (success_data, len(success_data))
    except: return (-1, 'Long parsing error')
def raw_to_useful(raw_post):
    #todo works good but need to check
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

    # очистка ссылки
    good_link = useful_data[3].replace(f'%2F', f'/').replace(f'%3A', f':')
    useful_data[3] = good_link

    return useful_data