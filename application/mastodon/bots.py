from mastodon import Mastodon , StreamListener
from bs4 import BeautifulSoup
from agents.base_agent import CityVillager
import re


def parse_content(text: str) -> str:
    clear = BeautifulSoup(text, "html.parser").text
    return re.sub(r'@\w+', '', clear)


class ProactiveBot:
    def __init__(self, bot: Mastodon, agent: CityVillager) -> None:
        self.bot = bot
        self.agent = agent

    def reply_on_status(self, status, reply):
        self.bot.status_reply(status, reply)


class ReactiveBot(StreamListener, ProactiveBot):
    # https://dev.to/tr11/creating-a-mastodon-bot-with-python-475b?ysclid=m1s8ghbnya694328857
    def on_notification(self, notification):
        status = notification.get('status')
        author = status.get('account').get('username')
        content = parse_content(status.get('content'))

        agent_decision = self.agent.invoke(f'{author} написал тебе: {content}')

        print(f'Агент решил использовать: {agent_decision}')
        if agent_decision['name'] == 'reply':
            args = eval(agent_decision['arguments'])
            self.reply_on_status(status, args['text'])


