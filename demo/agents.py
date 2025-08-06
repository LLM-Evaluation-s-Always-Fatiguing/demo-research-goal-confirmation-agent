from enum import Enum
from textwrap import dedent

from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.tools import tool

from .settings import settings


DEFAULT_DESCRIPTION = dedent(
    """\
    # Role

    You are an excellent researcher that can research in-depth on a given research goal.

    ## Skills

    - Persuasive and tactful, skilled at guiding users to provide more information in a non-intrusive way
      - trigger at: clarify research goal
    - Multi-dimensional exploration, adept at conducting comprehensive and in-depth research and analysis from multiple (preferably orthogonal) perspectives
      - trigger at: execute deep research
    """
)


class UserInteractionStrategy(Enum):
    CHITCHAT = "chitchat"
    CLARIFY_GOAL = "clarify_goal"
    CONFIRM_GOAL = "confirm_goal"
    END_INTERACTION = "end_interaction"


@tool(
    name="choose_user_interaction_strategy",
    strict=False,
    instructions=dedent(
        """\
        You have access to the `choose_user_interaction_strategy` tool to determine the most appropriate user interaction strategy based on the current situation.

        ## Tool Use Guidelines:
        - Purpose: Choose the most appropriate user interaction strategy based on the current situation.
        - Usage: Call `choose_user_interaction_strategy` with the strategy to choose to interact with the user.
        - Timing: ALWAYS call this tool before responding to the user.
        - Strategy selection guidelines:
          - `chitchat`: when the user not start to talk about the research goal.
          - `clarify_goal`: 
            - when you are talking about what to research and not all possible aspects of the research goal are covered.
            - when you have tried to confirm the goal but the user is not satisfied, not approve the goal, or provide more details to the goal.
          - `confirm_goal`: when you think the research goal is clear and all possible aspects are covered.
          - `end_interaction`: when the user confirm or approve the goal.
        """
    ),
    add_instructions=True,
)
def choose_user_interaction_strategy(strategy: UserInteractionStrategy) -> str:
    """Use this tool to determine the most appropriate user interaction strategy based on the current situation.

    Args:
        strategy: The strategy to choose to interact with the user.

    Returns:
        str: A corresponding instruction to guide the pattern of your interaction with the user under the chosen strategy.
    """
    match strategy:
        case UserInteractionStrategy.CHITCHAT:
            return "[Interaction Pattern] Smartly respond to the user's message and strategically guide the user to talk about the research goal."
        case UserInteractionStrategy.CLARIFY_GOAL:
            return "[Interaction Pattern] Ask the user to provide more details about those uncovered aspects of the research goal, provide some suggestions if possible."
        case UserInteractionStrategy.CONFIRM_GOAL:
            return "[Interaction Pattern] Summarize the research goal on your own words and ask the user to confirm the goal and provide more details if possible."
        case UserInteractionStrategy.END_INTERACTION:
            return "[Interaction Pattern] Thank the user, inform the user that you have complete the research goal clarification, provide the final refined research goal, and inform the user that you will start researching immediately."
        case _:
            raise ValueError(f"Invalid user interaction strategy: {strategy}")


class ResearchGoalClarificationAgentBuilder:
    def __init__(
        self,
        description: str = DEFAULT_DESCRIPTION,
    ):
        self._description = description
        
    
    def build_agent(self) -> Agent:
        return Agent(
            name="research_goal_clarification_agent",
            agent_id="research_goal_clarification_agent",
            description=self._description,
            create_default_system_message=True,
            goal="- Currrent Phase: clarify research goal\nStrategically interact with the user to gradually clarify and refine the user's real research goal.",
            instructions=[
                "Consider into all the possible aspects that may influence the research goal during your interaction with the user.",
                "Be polite and patient during the interaction.",
                "Be helpful and provide valuable suggestions during the interaction.",
            ],
            tools=[
                choose_user_interaction_strategy,
            ],
            show_tool_calls=True,
            tool_call_limit=1,
            model=OpenAIChat(id="gpt-4.1-mini", api_key=settings.openai_api_key),
            enable_session_summaries=True,
            storage=SqliteStorage(
                table_name="research_goal_clarification_agent",
                db_file=settings.storage_uri,
                mode="agent",
            ),
            stream=True,
            stream_intermediate_steps=True,
            add_history_to_messages=True,
            num_history_runs=20,
            add_datetime_to_instructions=True,
            debug_mode=True,
        )


__all__ = [
    "ResearchGoalClarificationAgentBuilder"
]
