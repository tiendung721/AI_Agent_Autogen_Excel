from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
import os
from dotenv import load_dotenv
import subprocess
import sys
# Đặt lại encoding cho stdout để hỗ trợ tiếng Việt
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

llm_config = {
    "model": "gpt-4o",
    "api_key": os.getenv("OPENAI_API_KEY"),
}

# Define agents
user = UserProxyAgent(
    name="UserProxyAgent",
    human_input_mode="NEVER",  # hoặc ALWAYS nếu muốn chat tương tác
    max_consecutive_auto_reply=5,
)

extractor = AssistantAgent(
    name="ExtractorAgent",
    llm_config=llm_config,
    code_execution_config={"work_dir": "output"},
    function_map={"extract_data": lambda: subprocess.run(["python", "extractor.py"], check=True)},
)

analyzer = AssistantAgent(
    name="AnalyzerAgent",
    llm_config=llm_config,
    code_execution_config={"work_dir": "output"},
    function_map={"analyze_data": lambda: subprocess.run(["python", "analyzer.py"], check=True)},
)

planner = AssistantAgent(
    name="PlannerAgent",
    llm_config=llm_config,
    code_execution_config={"work_dir": "output"},
    function_map={"generate_excel": lambda: subprocess.run(["python", "planner.py"], check=True)},
)

critic = AssistantAgent(
    name="CriticAgent",
    llm_config=llm_config,
    code_execution_config={"work_dir": "output"},
    function_map={"write_text_report": lambda: subprocess.run(["python", "critic.py"], check=True)},
)

reflector = AssistantAgent(
    name="ReflectiveAgent",
    llm_config=llm_config,
    code_execution_config={"work_dir": "output"},
    function_map={"verify_results": lambda: subprocess.run(["python", "reflector.py"], check=True)},
)

# Group chat setup
groupchat = GroupChat(
    agents=[user, extractor, analyzer, planner, critic, reflector],
    messages=[],
    max_round=2,
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Bắt đầu hội thoại
user.initiate_chat(
    manager,
    message="""
Hãy thực hiện pipeline sau:
1. ExtractorAgent.extract_data()
2. AnalyzerAgent.analyze_data()
3. PlannerAgent.generate_excel()
4. CriticAgent.write_text_report()
5. ReflectiveAgent.verify_results()
"""
)
