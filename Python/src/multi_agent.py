import os
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies import (
    KernelFunctionSelectionStrategy,
    KernelFunctionTerminationStrategy,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistoryTruncationReducer
from semantic_kernel.functions import KernelFunctionFromPrompt

# Add Logger
logger = logging.getLogger(__name__)

# Find and load the .env file from the src directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

def create_kernel():
    """Creates a Kernel instance with an Azure OpenAI ChatCompletion service."""
    kernel = Kernel()
    kernel.add_service(service=AzureChatCompletion())
    return kernel

async def run_multi_agent(user_input: str):
    """
    Run a multi-agent collaboration with Business Analyst, Software Engineer, and Product Owner.
    
    Args:
        user_input (str): The user's request for application development
    """
    # Create a single kernel instance for all agents
    kernel = create_kernel()
    
    # Define agent names as constants
    # IMPORTANT: These names must match the ones used in the selection function
    # as they are used in the UI to help change how the agents are displayed
    BUSINESS_ANALYST_NAME = "BusinessAnalyst"
    SOFTWARE_ENGINEER_NAME = "SoftwareEngineer" 
    PRODUCT_OWNER_NAME = "ProductOwner"
    
    # TODO: Step 1 - Create ChatCompletionAgents
    # Create three ChatCompletionAgent instances using the personas provided in the challenge
    # Each agent needs: kernel, name, and instructions
    # Use the BUSINESS_ANALYST_NAME, SOFTWARE_ENGINEER_NAME, and PRODUCT_OWNER_NAME constants
    
    
    # TODO: Step 2 - Define a selection function to determine which agent should take the next turn
    selection_function = KernelFunctionFromPrompt(
        function_name="agent_selection",
        prompt=f"""
            Examine the provided RESPONSE and choose the next participant.
            State only the name of the chosen participant without explanation.
            Never choose the participant named in the RESPONSE.

            Choose only from these participants:
            - {BUSINESS_ANALYST_NAME}
            - {SOFTWARE_ENGINEER_NAME}
            - {PRODUCT_OWNER_NAME}

            Rules:
            - If RESPONSE is user input, it is {BUSINESS_ANALYST_NAME}'s turn.
            - If RESPONSE is by {BUSINESS_ANALYST_NAME}, it is {SOFTWARE_ENGINEER_NAME}'s turn.
            - If RESPONSE is by {SOFTWARE_ENGINEER_NAME}, it is {PRODUCT_OWNER_NAME}'s turn.
            - If RESPONSE is by {PRODUCT_OWNER_NAME} and contains criticism, it is {SOFTWARE_ENGINEER_NAME}'s turn.

            RESPONSE:
            {{{{$lastmessage}}}}
            """,
    )

    
    # TODO: Step 3 - Define a termination function
    # Create a KernelFunctionFromPrompt that checks if the Product Owner has approved the work
    # The termination keyword is "%APPR%"
    # The function should respond with the termination keyword when the Product Owner approves
    termination_keyword = "%APPR%"
    
    termination_function = KernelFunctionFromPrompt(
        function_name="termination_check",
        prompt=f"""
            Examine the RESPONSE and determine whether the Product Owner has approved the work.
            If the work is approved, respond with a single word without explanation: {termination_keyword}.
            If the Product Owner is still providing feedback or criticism, it is not approved.
            If the Product Owner says "%APPR%", it is approved.

            RESPONSE:
            {{{{$lastmessage}}}}
            """,
    )
    
    
    # TODO: Step 4 - Create history reducer to save tokens
    # Create a ChatHistoryTruncationReducer with target_count=3 to limit conversation history
    history_reducer = ChatHistoryTruncationReducer(target_count=3)
    
    
    # TODO: Step 5 - Create the AgentGroupChat
    
    
    # TODO: Step 6 - Add the user's initial request to the chat
    
    
    responses = []
    
    # TODO: Step 7 - Invoke the group chat and collect agent responses
    # Use an async for loop to iterate through group_chat.invoke()
    # Collect responses in the format: {"role": response.name, "message": response.content}
    try:
        # Start: Invoke the group chat and collect agent responses
        async for response in group_chat.invoke():
            if response is None or not response.name:
                    continue
            responses.append({"role": response.name, "message": response.content})
        # End: Invoke the group chat and collect agent responses
    except Exception as e:
        responses.append({
            "role": "System", 
            "message": f"❌ Error during multi-agent collaboration: {e}"
        })
    
    logger.info("Multi-agent conversation complete.")
    return responses
