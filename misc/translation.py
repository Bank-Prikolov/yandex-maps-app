import gettext


def translate(lang, window):
    translation = gettext.translation('messages', localedir=fr'assets\{window}\locale', languages=[lang])
    translation.install()
    return translation.gettext


def format_lang(language):
    if language == 'en':
        lang = 'en_RU'
    elif language == 'ru':
        lang = 'ru_RU'
    else:
        lang = 'be_BY'
    return lang
