import json
import database.main as db

#language variables
with open('lang/en.json', 'r', encoding='utf-8') as file:
    en = json.load(file)
with open('lang/ru.json', 'r', encoding='utf-8') as file:
    ru = json.load(file)
with open('lang/ua.json', 'r', encoding='utf-8') as file:
    ua = json.load(file)
with open('lang/de.json', 'r', encoding='utf-8') as file:
    de = json.load(file)
with open('lang/fr.json', 'r', encoding='utf-8') as file:
    fr = json.load(file)

def translate(id, key):
    usr_lang = db.get_lang(id)[0]
    if usr_lang == "en":
        return en[key]
    elif usr_lang == "ru":
        return ru[key]
    elif usr_lang == "ua":
        return ua[key]
    elif usr_lang == "de":
        return de[key]
    elif usr_lang == "fr":
        return fr[key]