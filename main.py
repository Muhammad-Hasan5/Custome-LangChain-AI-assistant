#from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI


from dotenv import load_dotenv
import gradio as gr
import os

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

system_prompt = """
You are FinSight, a smart, trustworthy AI finance assistant. 
Speak clearly and confidently about personal finance, investing,
and stock markets. Keep explanations simple but accurate, give data-driven insights, 
and use real-world examples. Stay professional yet friendly, ask clarifying questions and give precise answers, 
and never promise guaranteed returns — focus on helping users make informed, responsible decisions.
"""

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = gemini_key,
    temperature = 0.5
)

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt),
    (MessagesPlaceholder(variable_name = "history")),
    ("user", "{input}")]
)

chain = prompt | llm | StrOutputParser()

print("FinSight: Hey there! How can I help you?")

history = [] # Chat history list

# while True:
#     user_input = input("You: ")
#     if user_input == "exit":
#         break
#     response = chain.invoke({"input": user_input, "history": history})
#     print(f"FinSight: {response}")
#     history.append(HumanMessage(content = user_input))
#     history.append(AIMessage(content = response))
#
#
# print("FinSight: Bye! See you again.")

page = gr.Blocks(
    title = "Chat with Fin$sight",
    theme = gr.themes.Soft(),
)

with page:
    gr.Markdown(

        """
        # Chat with Fin$sight
        Welcome to the FinSight, you're finance adviser.
        """
    )

    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    button = gr.Button()

page.launch(share = True)