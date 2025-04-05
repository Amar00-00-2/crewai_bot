from crewai import Agent, Crew, Task
from crewai_fastapi_agent_chat.tools.custom_tool import RouterTool

from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
from langchain_openai import ChatOpenAI
import os


# src/latest_ai_development/crew.py
llm_openai = ChatOpenAI(model="gpt-4o", openai_api_key=os.environ['OPENAI_API_KEY'], temperature=0)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@CrewBase
class LatestAiDevelopmentCrew():
  """LatestAiDevelopment crew"""

  @before_kickoff
  def before_kickoff_function(self, inputs):
    print(f"Before kickoff function with inputs: {inputs}")
    return inputs # You can return the inputs or modify them as needed

  @after_kickoff
  def after_kickoff_function(self, result):
    print(f"After kickoff function with result: {result}")
    return result # You can return the result or modify it as needed


@CrewBase
class EmailRagAgent:
    """EmailRagAgent crew"""
    
    agents_config_path = 'config/agents.yaml'
    tasks_config_path = 'config/tasks.yaml'
    
    @agent
    def router_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['router_agent'],
			verbose=True,
			# allow_delegation=True,
			tools=[RouterTool()],
			llm=llm_openai
		)

    @task
    def router_task(self) -> Task:
        return Task(
			config=self.tasks_config['router_task'],
		)
        
    @crew
    def crew(self):
        """Creates the EmailRagAgent crew"""
    
        return Crew(
            agents=[self.router_agent()],  
            tasks=[self.router_task()],
            verbose=True,
        )

