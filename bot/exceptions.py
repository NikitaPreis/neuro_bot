class DataBaseException(Exception):
    """Database exception."""
    detail = 'Не удалось получить данные из базы данных.'


class GPTUnavaibleException(Exception):
    """GPT is temporarily unavailable."""
    detail = 'Нейросеть временно недоступна.'


class GPTClientException(Exception):
    """GPT client exception."""
    detail = 'Ошибка GPT клиента.'


class GPTClientHTTPException(Exception):
    """GPT client http exception."""
    detail = 'Ошибка в запросе клиента к GPT.'


class GPTClientAccessTokenException(Exception):
    """GPT client access token exception."""
    detail = 'Токен доступа для GPT клиента отсутсвует или невалиден.'
