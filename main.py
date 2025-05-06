from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool
from typing import cast
import chainlit as cl
import re
from instructions import instructions
from agents_tools import availableRooms, booking_agent
from customer_support.FAQs import FAQs_retreivel
from customer_support.available_rooms import get_rooms_availability, check_room_status
from chainlit.input_widget import TextInput
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print("Instruction", instructions)

# external_client = AsyncOpenAI(
#     api_key=GOOGLE_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True

# )

# agent = Agent(
#     name="Innovia",
#     instructions=instructions
# )

# @function_tool
# def userInfo(name: str, email: str):
#     return {"name": name, "email": email}


def extract_name_and_email(text: str):
    # Try to extract name (basic heuristic)
    name_match = re.search(r"\bname is ([A-Z][a-z]+(?: [A-Z][a-z]+)*)", text, re.IGNORECASE)
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

    name = name_match.group(1).strip() if name_match else None
    email = email_match.group(0).strip() if email_match else None

    return name, email


@cl.on_chat_start
async def start():
    # 🔹 Ask for name
    # name = await cl.AskUserMessage(content="What is your name?", timeout=30).send()
    # if not name or not name.get("output"):
    #     await cl.Message(content="⚠️ You did not provide a name. Please refresh the chat to try again.").send()
    #     return  # Stop further execution

    # name_value = name["output"]

    # # 🔹 Ask for email
    # email = await cl.AskUserMessage(content="What is your email?", timeout=30).send()
    # if not email or not email.get("output"):
    #     await cl.Message(content="⚠️ You did not provide an email. Please refresh the chat to try again.").send()
    #     return  # Stop further execution

    # email_value = email["output"]

    # # 🔹 Store in session
    # cl.user_session.set("user_name", name_value)
    # cl.user_session.set("user_email", email_value)

    # 🔹 Setup Gemini client and Agent
    external_client = AsyncOpenAI(
        api_key=GOOGLE_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)

    agent = Agent(name="Innovia", instructions=instructions, tools=[
        booking_agent.booking_agent.as_tool(
            tool_name="Booking_tool",
            tool_description="Book a room"
        ),
        get_rooms_availability,
        check_room_status,
        FAQs_retreivel
    ])


    cl.user_session.set("agent", agent)

#     await cl.Message(content=f"""👋 Hi **{name_value}**, welcome to Ainnovate Solutions!

# I'm Innovia, your AI business consultant. Just tell me a bit about your business, and I’ll help you explore AI-powered solutions — completely free of charge!
# """).send()



@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(starting_agent = agent,
                    input=history,
                    run_config=config)
        
        response_content = result.final_output
        
        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()
        #  history.append({"role": "assistant", "content": msg.content})
    
        # Update the session with the new history.
        cl.user_session.set("chat_history", result.to_input_list())
        
         # 🧠 Attempt to extract name and email
        name, email = extract_name_and_email(response_content)

        if name and not cl.user_session.get("user_name"):
            cl.user_session.set("user_name", name)
            print(f"[Extracted Name] {name}")

        if email and not cl.user_session.get("user_email"):
            cl.user_session.set("user_email", email)
            print(f"[Extracted Email] {email}")
        
        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")