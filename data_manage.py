def save_results(data_array, mode='txt'):
    '''
    :param data_array:
    :param mode:
    :return:
    '''
    if mode == 'txt':
        with open('parsed_pikabu.txt', 'a') as file:
            for each in data_array:
                file.write(' '.join(each) + "\n")
    elif mode == 'db':
        pass

