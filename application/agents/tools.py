from langchain_core.tools import tool


@tool
def reply(text: str) -> int:
    """
    Функция для того, чтобы ответить на пост

    Agrs:
    text: Текст ответа
    """

    return {'action': 'reply', 'text': text}
