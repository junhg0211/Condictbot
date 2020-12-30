import json
import pickle
from re import findall

from discord import DMChannel, User

from util.constants import ENGLISH_LAN, KOREAN_LAN, JAPANESE_LAN


def tokenize(string: str) -> list:
    result = string.split(' ')

    i = 0
    word_starter = -1

    while i < len(result):
        if result[i].startswith('"'):
            word_starter = i
        elif result[i].endswith('"'):
            result[word_starter:i+1] = [' '.join(result[word_starter:i+1])[1:-1]]
        i += 1

    return result


def is_available_dictionary_name(name: str) -> bool:
    _name = findall(r'[A-Za-z \d]{,50}', name)
    if _name:
        return _name[0] == name
    return False


def is_dm_channel(channel) -> bool:
    return isinstance(channel, DMChannel)


def ordered(decimal: int) -> str:
    date_suffix = ["th", "st", "nd", "rd"]

    if decimal % 10 in [1, 2, 3] and decimal not in [11, 12, 13]:
        return f'{decimal}{date_suffix[decimal % 10]}'
    else:
        return f'{decimal}{date_suffix[0]}'


def get_language(tobcidnock, user: User) -> dict:
    if user.id not in tobcidnock.settings['USER'].keys():
        tobcidnock.settings['USER'][user.id] = {'LANGUAGE': 'ENGLISH'}

    if tobcidnock.settings['USER'][user.id]['LANGUAGE'] == 'ENGLISH':
        return ENGLISH_LAN
    elif tobcidnock.settings['USER'][user.id]['LANGUAGE'] == 'KOREAN':
        return KOREAN_LAN
    elif tobcidnock.settings['USER'][user.id]['LANGUAGE'] == 'JAPANESE':
        return JAPANESE_LAN


def pickle_to_json(path):
    with open(path, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    json_path = path[::-1].split('.', 1)[1][::-1] + '.json'
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file)
    return json_path


if __name__ == '__main__':
    print(tokenize("word 'je zacokespika' is for making good stuffs."))
    print(tokenize(input()))
