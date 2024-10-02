from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from database.logic import load_agent_profile
from typing import List
import os
import re


class CityVillager:
    def __init__(
            self,
            llm: BaseChatModel,
            tools: List[Tool]
    ) -> None:

        self.llm = llm
        self.tools = tools
        self._load_profile()
        self._create_prompt()
        self._init_agent()

    def _load_profile(self) -> None:
        self.profile = load_agent_profile(str(os.environ.get('AGENT_UID')))

    def _create_prompt(self) -> None:
        system_prompt = SystemMessage(content=re.sub(r' {2,}', '', f"""
        Тебя зовут: {self.profile.full_name}. 
        Твоя биография: {self.profile.bio}.
        """).strip())

        self.prompt = ChatPromptTemplate.from_messages([
            system_prompt,
            ("human", "{user_input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

    def _init_agent(self) -> None:
        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        self.agent = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True
        )

    def summarize_history(self) -> None:
        pass

    def make_action(self) -> None:
        pass