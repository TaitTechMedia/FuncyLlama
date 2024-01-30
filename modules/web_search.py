from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun
import os
from dotenv import load_dotenv
load_dotenv()

search_tool = DuckDuckGoSearchRun()

def web_search(query):
    """
    This tool can be used to search the internet.

    This can also be used to read the contents of any url that is NOT a youtube url.

    Args:
    query (str): The user query.

    Returns:
    string: The answer to the user's query.
    """
    openhermes = Ollama(model="openhermes", base_url=os.getenv('OLLAMA_BASE_URL'))

    # Define your agents with roles and goals
    researcher = Agent(
    role='Senior Research Analyst',
    goal=query,
    backstory="""You are a Senior Research Analyst at a leading tech think tank.
    Your expertise lies in identifying complex topics and breaking them down.
    You have a knack for dissecting complex data and presenting actionable insights.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=openhermes
    )
    writer = Agent(
    role='Tech Writer',
    goal='Write a compelling blog post based on the research you were given from the Senior Research Analyst',
    backstory="""You are a renowned Tech Writer, known for your insightful
    and engaging articles on technology and innovation. With a deep understanding of
    the tech industry, you transform complex concepts into compelling narratives. 
    You will take your researcher's report and write a long, detailed blog post.
    YOU WILL NOT USE ANY TOOLS!""",
    verbose=True,
    allow_delegation=False,
    llm=openhermes
    )

    # Create tasks for your agents
    task1 = Task(
    description=f"""Conduct a comprehensive analysis of {query}.
    Identify key trends, breakthrough technologies, and potential industry impacts.
    Compile your findings in a detailed report.""",
    agent=researcher
    )

    task2 = Task(
    description="""Using the insights from the researcher's report, develop an engaging blog
    post that highlights the most significant details about the report.
    Your post should be informative yet accessible, catering to a tech-savvy audience.
    Aim for a narrative that captures the essence of these breakthroughs and their
    implications for the future. YOU WILL NOT USE ANY TOOLS!""",
    agent=writer
    )

    # Instantiate your crew with a sequential process
    crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=2, # Crew verbose more will let you know what tasks are being worked on, you can set it to 1 or 2 to different logging levels
    process=Process.sequential, # Sequential process will have tasks executed one after the other and the outcome of the previous one is passed as extra content into this next.
    )

    # Get your crew to work!
    result = crew.kickoff()

    print("######################")
    print({
    'Blog Post': result
    })

    filename = 'blog_post.md'
    with open(filename, 'w') as file:
        file.write(f"# Blog Post\n\n{result}\n")
    print(f"Blog post saved as {filename}")