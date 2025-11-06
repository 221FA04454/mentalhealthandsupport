from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# LangChain imports
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI

load_dotenv()

app = FastAPI()

# Load secret keys if needed
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the LLM
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)

# Define a prompt template
prompt = PromptTemplate(
    input_variables=["message"],
    template="You are a compassionate mental health assistant. A student says: '{message}'. Respond supportively and helpfully."
)

# Create a chain with the LLM and prompt
chain = LLMChain(llm=llm, prompt=prompt)

@app.get("/")
def read_root():
    return {"message": "Mental Health Support API is running!"}

class StudentQuery(BaseModel):
    message: str

@app.post("/chat/")
def chat(query: StudentQuery):
    user_message = query.message
    response = chain.run(message=user_message)
    return {"reply": response}
