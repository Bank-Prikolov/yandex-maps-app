import gettext


def translate(lang, window):
    translation = gettext.translation('messages', localedir=fr'assets\{window}\locale', languages=[lang])
    translation.install()
    return translation.gettext
