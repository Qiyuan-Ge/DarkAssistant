from langchain.agents import Tool

finish_tool = Tool(
    name="Final Response",
    func=lambda x: None,
    description='response to user if you know the final answer or complete all tasks, args: <your final answer in markdown format>',
    )
