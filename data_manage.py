import sqlite3


def save_results(data_array, mode='txt'):
    '''
    :param data_array:
    :param mode:
    :return:
    '''
    if mode == 'txt':
        # todo put an exception
        with open('parsed_pikabu.txt', 'a') as file:
            for each in data_array:
                file.write(' '.join(each) + "\n")
    elif mode == 'db':
        pass

def load_results_txt():
    try:
        with open("parsed_pikabu.txt", "r") as file:
            data = file.readlines()
        data_to_work_with = []
        for each in data:
            data_to_work_with.append(each[:-1].split(" "))
        return data_to_work_with
    except:
        return -1
