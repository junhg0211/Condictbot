import json
import pickle

with open('./token.pickle', 'rb') as file:
    BOT_TOKEN = pickle.load(file)

DEBUG = False
DEVELOPER_USER_IDS = (
    697316460237946890,  # ITSELF
    366565792910671873  # SCH
)

NAME = 'Tobcidnock'

COMMAND_IDENTIFIER = '@@'
SEARCH_IDENTIFIER = '@?'

AGREED_EMOJI = '⭕'
DISAGREED_EMOJI = '❌'
WORK_END_EMOJI = '☑️'

COLOR = 0x7255D1

with open('./res/language/english.json', 'r') as file:
    ENGLISH_LAN = json.load(file)
with open('./res/language/korean.json', 'r') as file:
    KOREAN_LAN = json.load(file)
with open('./res/language/japanese.json', 'r') as file:
    JAPANESE_LAN = json.load(file)
