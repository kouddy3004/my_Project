import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from dotenv import load_dotenv

# LangChain Imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ... after app = FastAPI() ...


load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Model
api_key = os.getenv("OPENROUTER_API_KEY")

model = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    max_tokens=100, # Very short for chatbot speed
    temperature=0.3, # Low temperature = Faster & More accurate
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Koushik Pro Portfolio",
    }
)


def get_qa_chain(task_type):
    prompts = {
        "ticket": "Convert to Jira ticket. Be concise: {user_input}",
        "gherkin": "Write Gherkin scenarios for: {user_input}",
        "selenium": "Write clean Selenium Python code for: {user_input}",
        "resume_bot": """You are Koushik's Assistant. Answer BRIEFly (max 2 sentences).
        # Inside get_qa_chain function:
            Answer questions using this detailed context:
            - Experience: 8+ years in Automation/Software Engineering[cite: 2, 29].
            - Current Role: Test Automation Engineer at Oracle (OFSAA) specializing in cross-environment validation[cite: 8, 9].
            - Past Role: QA Lead at Genpact, focused on fraud-detection middleware and Java/Selenium automation[cite: 14, 17, 18].
            - Past Role: Associate at Cognizant, specialized in Python/ETL validation (cx_Oracle)[cite: 26, 27].
            - AI Expertise: Built JIRA analyzers and RAG-based chatbots using LangChain[cite: 52, 55].
            - Education: MCA from SSN College of Engineering (Anna University)[cite: 32, 33].
            User Question: {user_input}"""
    }
    prompt = ChatPromptTemplate.from_template(prompts.get(task_type, "{user_input}"))
    return prompt | model | StrOutputParser()


# @app.get("/")
# async def index(request: Request):
#     return templates.TemplateResponse(
#         request=request, name="index.html", context={"request": request}
#     )

current_dir = os.path.dirname(os.path.realpath(__file__))


@app.get("/")
async def read_index():
    # Construct the full path to index.html
    file_path = os.path.join(current_dir, os.path.join("templates","index.html"))

    if not os.path.exists(file_path):
        return {"error": f"File not found at {file_path}"}

    return FileResponse(file_path)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content="", media_type="image/x-icon")


@app.post("/generate")
async def generate_qa_content(task: str = Form(...), user_input: str = Form(...)):
    try:
        chain = get_qa_chain(task)
        result = await chain.ainvoke({"user_input": user_input})
        return {"result": result.strip()}
    except Exception as e:
        return {"result": "The Genie is resting. Try again in a moment."}
