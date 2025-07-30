from dotenv import load_dotenv
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from roadmap_tool import get_career_roadmap
load_dotenv()
client = AsyncOpenAI(
    api_key = os.getenv("gemini_api_key"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                
)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, tracing_disabled=True)
career_agent = Agent(
    name="CareerAgent",
    instructions="You ask about interests of the people then suggest field.",
    model=model
)
skill_agent = Agent(
    name="SkillAgent",
    instructions="You suggest skills for the suggested field by using get_career_roadmap tool.",
    model=model,
    tools= [get_career_roadmap]
)
job_agent= Agent(
    name="JobAgent",
    instructions="You suggest job titles in thechosen career.",
    model=model
)
def main():
    print ("/ Career Mentor Agent /n ")
    interest = input ("What sre your interest? -> ")
    result1 = Runner. run_sync (career_agent, interest, run_config=config)
    field = result1.final_output.strip()
    print ("\n Suggested Career: ", field)
    result2 = Runner. run_sync (skill_agent, field, run_config = config)
    interest = result2.final_output.strip()
    print ("\n Required Skill ", result2.final_output)
    result3 = Runner.run_sync (job_agent, field, run_config=config)
    print ("\n Possible jobs : ", result3.final_output)




if __name__ == "__main__":
    main()
