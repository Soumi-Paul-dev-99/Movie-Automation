
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

from dotenv import load_dotenv
import os

from tools import (
    show_all_movies,
    show_movies_by_multiplex,
    show_halls_by_multiplex,
    show_movie_details
)

load_dotenv()


# OpenAI Model
model_client = OpenAIChatCompletionClient(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)


# Create Tools
movie_tool = FunctionTool(
    show_all_movies,
    description="Show all available movies with their genre and time."
)

multiplex_tool = FunctionTool(
    show_movies_by_multiplex,
    description="Show all movies available in a given multiplex. Requires multiplex_id."
)

hall_tool = FunctionTool(
    show_halls_by_multiplex,
    description="Show all hall IDs in a given multiplex. Requires multiplex_id."
)

details_tool = FunctionTool(
    show_movie_details,
    description="Show complete movie details using multiplex_id and hall_id."
)


# Create AI Agent
movie_agent = AssistantAgent(
    name="MovieAutomationAgent",
    model_client=model_client,
    tools=[
        movie_tool,
        multiplex_tool,
        hall_tool,
        details_tool
    ],
    system_message="""
    You are a Movie Automation AI Assistant.

    Your job is to manage movie information using database tools.

    Rules:

    1. If user asks for all movies,
       call show_all_movies.

    2. If user asks movies by multiplex,
       call show_movies_by_multiplex.

    3. If user asks halls by multiplex,
       call show_halls_by_multiplex.

    4. If user asks movie details by multiplex and hall,
       call show_movie_details.

    5. Never invent movie information.

    6. Always use database tool results.

    7. Give answers in simple and clear format.

    8. If required IDs are missing,
       ask the user to provide them.
    """
)


# Function to communicate with Agent

async def ask_movie_agent(user_prompt):

    model_client = OpenAIChatCompletionClient(
        model="gpt-4.1-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    try:

        movie_agent = AssistantAgent(
            name="MovieAutomationAgent",
            model_client=model_client,
            tools=[
                movie_tool,
                multiplex_tool,
                hall_tool,
                details_tool
            ],
            system_message="""
            You are a Movie Automation AI Assistant.

            Use database tools to answer questions.

            Call the correct tool based on the user prompt.

            Never invent movie information.

            If IDs are missing, ask the user.

            Give clear and simple answers.
            """
        )

        result = await movie_agent.run(
            task=user_prompt
        )

        return result.messages[-1].content

    finally:

        await model_client.close()

