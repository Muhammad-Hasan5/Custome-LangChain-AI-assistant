from langchain_core.messages import HumanMessage, AIMessage
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


def chat(user_input, history):
    langchain_history = []
    for item in history:
        if item["role"] == "user":
            langchain_history.append(HumanMessage(content = item["content"]))
        elif item["role"] == "assistant":
            langchain_history.append(AIMessage(content = item["content"]))

    response = chain.invoke({"input": user_input, "history": langchain_history})

    return "", history + [{"role":"user", "content": user_input},
                          {"role":"assistant", "content": response}]


page = gr.Blocks(
    title = "Chat with FinSight",
    theme = gr.themes.Soft(),
)


def clear_chat():
    return "", []

#GUI
with page:
    gr.Markdown(

        """
        # Chat with FinSight
        Welcome to the FinSight, you're finance adviser.
        """
    )

    chatbot = gr.Chatbot(type = "messages",
                         show_label = False,
                         avatar_images = [None, 'finsight.jpg'])

    msg = gr.Textbox(show_label = False,
                     placeholder = "Ask FinSight...")

    msg.submit(chat, [msg, chatbot], [msg, chatbot])

    clear = gr.Button("Clear Chat", variant = "Secondary")
    clear.click(clear_chat, outputs = [msg, chatbot])

page.launch(share = True)