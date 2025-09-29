import os
from dotenv import load_dotenv
from groq import Groq

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

#Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Groq_API_KEY not found in .env file")

#Initialize Groq client
mikey = Groq(api_key=GROQ_API_KEY)


prompt_template_string = """
You are a lightweight but reliable assistant built to help users quickly find accurate answers from the provided knowledge base.

Your priorities:
1. Always ground your answers in the context or knowledge provided. If the answer is not available, clearly say: “I don't know from the current knowledge base.”
2. Be concise and clear.
3. Maintain a professional yet approachable tone.
4. Focus on the user’s actual question.
5. Never invent facts or speculate.
6. Provide step-by-step guidance if asked.
7. Politely explain limitations if the question goes beyond your knowledge base.
8. If the answer is not found in the knowledge base, politely say so using different phrasing each time.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template_string
)


class GroqLLM:
    def __init__(self, client, prompt_template, model="llama-3.1-8b-instant"):
        self.client = client
        self.model = model
        self.prompt_template = prompt_template

    def __call__(self, inputs: dict) -> str:
        prompt_text = self.prompt_template.format(**inputs)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

llm = GroqLLM(mikey, prompt)
rag_chain = llm | StrOutputParser()

def call_llm(query: str, context: str) -> str:
    inputs = {"context": context, "question": query}
    try:
        return rag_chain.invoke(input=inputs)
    except Exception as e:
        print("Groq API error:", e)
        return "Oops! Something went wrong generating the response."