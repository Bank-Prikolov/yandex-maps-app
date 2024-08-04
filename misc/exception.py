import sys


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def format_exception(action, lang, error=None, reason=None):
    result = None
    if action == 'map_error':
        if lang == 'ru':
            result = (action,
                      'К сожалению, в данной области нет организации')
        elif lang == 'be':
            result = (action,
                      'К сожалені, в гэтай вобласці няма організацыі')
        elif lang == 'en':
            result = (action,
                      'Unfortunately, there is no organization in this area')
    elif action == 'req_error':
        if error is None:
            if lang == 'ru':
                result = (action,
                          f'Ошибка запроса! Местоположение по запросу "{reason}" не найдено')
            elif lang == 'be':
                result = (action,
                          f'Памылка запысу! Месцаположэнне па запысу "{reason}" не знойдзены')
            elif lang == 'en':
                result = (action,
                          f'Request error! Location "{reason}" not found')
        else:
            if lang == 'ru':
                result = (action,
                          f'Ошибка запроса: {error}\n'
                          f'Причина: {reason}')
            elif lang == 'be':
                result = (action,
                          f'Памылка запысу: {error}\n'
                          f'Памылка: {reason}')
            elif lang == 'en':
                result = (action,
                          f'Request error: {error}\n'
                          f'Reason: {reason}')
    return result
