import os
from datetime import datetime
from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# LangChain Imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

app = FastAPI()

# --- DYNAMIC EXPERIENCE CALCULATION ---
# You joined the industry in 2014.
# This logic ensures your portfolio stays current every year without manual updates.
START_YEAR = 2014
current_year = datetime.now().year
experience_years = current_year - START_YEAR

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Model
api_key = os.getenv("OPENROUTER_API_KEY")

model = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    max_tokens=150,  # Increased slightly for better resume answers
    temperature=0.3,
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Koushik Pro Portfolio",
    }
)


def get_qa_chain(task_type):
    # Professional context derived from your career history
    resume_context = f"""
    You are 'QA Genie,' the professional AI assistant for Koushik Subramanian. 
    Koushik is a Senior Software Engineer and QA Lead with {experience_years} years of experience.

    KEY PROFESSIONAL FACTS:
    - Experience: {experience_years} years specializing in Test Automation and Data Validation.
    - Tech Stack: Expert in Python (FastAPI), Preact, LangChain, and Selenium.
    - Career History: Previously a Lead Consultant at Genpact (Banking/Fraud UI) and Associate at Cognizant (ETL/Oracle).
    - Education: MCA from SSN College of Engineering.
    - Recent Projects: Built 'QA-Genie' (AI Testing Suite) and JIRA ticket analyzers using RAG concepts.
    
    USE THIS RESUME CONTEXT TO ANSWER:
            {RESUME_TEXT}
    
    INSTRUCTIONS:
    - Answer as a helpful assistant. Use 'Koushik' or 'He' to refer to the candidate.
    - Be concise (max 3 sentences).
    - If asked about experience, highlight the {experience_years} years of industry expertise.
    """

    prompts = {
        "ticket": "Convert the following requirement into a professional Jira ticket. Be concise: {user_input}",
        "gherkin": "Write clean BDD Gherkin scenarios for the following feature: {user_input}",
        "selenium": "Write optimized Selenium Python code using POM for: {user_input}",
        "resume_bot": f"{resume_context}\nUser Question: {{user_input}}"
    }

    prompt = ChatPromptTemplate.from_template(prompts.get(task_type, "{user_input}"))
    return prompt | model | StrOutputParser()

# Load Resume Details from PDF
def load_resume_context():
    try:
        # Path to your PDF inside the container
        resume_path = os.path.join("static", "Koushik_Subramanian_Resume.pdf")
        loader = PyPDFLoader(resume_path)
        pages = loader.load_and_split()
        # Combine the first few pages into one context string
        return "\n".join([page.page_content for page in pages[:3]])
    except Exception:
        return "Senior SDET with expertise in Python, Selenium, and AI Automation."

RESUME_TEXT = load_resume_context()

current_dir = os.path.dirname(os.path.realpath(__file__))


@app.get("/")
async def read_index():
    # Targets the 'templates' folder for your UI
    file_path = os.path.join(current_dir, "templates", "index.html")

    if not os.path.exists(file_path):
        return {"error": f"UI File not found at {file_path}"}

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
        # Graceful error handling for the UI
        return {"result": "The Genie is temporarily offline. Please try again in a moment."}