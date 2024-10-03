from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from application.database.logic import load_agent_profile
from typing import List, Dict
import os
import re


class CityVillager:
    """
    Базовый класс для
    """

    def __init__(
            self,
            llm: BaseChatModel,
            tools: List[Tool],
            profile_id: int
    ) -> None:

        self.llm = llm
        self.tools = tools
        self._load_profile(profile_id)
        self._create_prompt()
        self._init_agent()

    def _load_profile(self, profile_id: int) -> None:
        self.profile = load_agent_profile(profile_id)

    def _create_prompt(self) -> None:
        self.system_prompt = SystemMessage(content=re.sub(r' {2,}', '', f"""
        Тебя зовут: {self.profile.full_name}. 
        Твоя биография: {self.profile.bio}.
        """).strip())

        # self.prompt = ChatPromptTemplate.from_messages([
        #     self.system_prompt,
        #     ("human", "{user_input}"),
        #     MessagesPlaceholder(variable_name="agent_scratchpad")
        # ])

    def _init_agent(self) -> None:
        # agent = create_tool_calling_agent(
        #     llm=self.llm,
        #     tools=self.tools,
        #     prompt=self.prompt
        # )
        #
        # self.agent = AgentExecutor(
        #     agent=agent,
        #     tools=self.tools,
        #     verbose=True
        # )

        self.agent = self.llm.bind_tools(self.tools)

    def invoke(self, task: int) -> Dict:
        return self.agent.invoke([self.system_prompt, HumanMessage(content=task)]).additional_kwargs.get('tool_calls')[0].get('function')