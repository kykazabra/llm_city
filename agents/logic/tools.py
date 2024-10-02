from langchain_core.tools import tool
from mastodon.models import ProfilePost


@tool
def write_post(title: str, text: str) -> int:
    """
    Функция для того, чтобы написать пост

    Agrs:
    title: Название поста
    text: Текст поста
    """

    post = ProfilePost(title=title, text=text)
    post.post()

    return str(post)