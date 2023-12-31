from typing import List
from langchain.agents import Tool

from assistant.tools.shell import ShellAgent
from .web_copilot import WebCopilot
from .code_copilot import CodeExpert
from ..tools import load_tools, finish_tool


def load_agents(agent_names: List[str], callbacks=None, template_name="openchat_3.5"):
    agent_list = []
    for agent_name in agent_names:
        if agent_name == "Web Copilot":
            agent_func = WebCopilot(
                tools=load_tools(["Google Search", "Browse Website", "Wikipedia"]),
                template_name=template_name,
                callbacks=callbacks,
            )
            agent = Tool(
                name="Web Copilot",
                func=agent_func.run,
                description='a web assistant help you gather information from the web, args: <question>',
            )
            agent_list.append(agent)
        elif agent_name == "Code Copilot":
            agent_func = CodeExpert(
                tools=load_tools(["LLM Code", "Google Search", "Browse Website"]),
                template_name=template_name,
                callbacks=callbacks,
            )
            agent = Tool(
                name="Code Copilot",
                func=agent_func.run,
                description='a coding assistant help you address coding issues, args: <coding issue>',
            )
            agent_list.append(agent)
        elif agent_name == "Shell Copilot":
            agent_func = ShellAgent()
            agent = Tool(
                name="Shell Copilot",
                func=agent_func.run,
                description='a shell assistant help you address shell task, args: <task issue>',
            )
            agent_list.append(agent)
    
    agent_list.append(finish_tool)        
    return agent_list
