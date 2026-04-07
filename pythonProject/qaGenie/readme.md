# 🧞 QA Genie: AI-Powered Test Orchestration Suite

QA Genie is an intelligent multi-agent AI tool designed to bridge the gap between business requirements and test
execution. By leveraging Large Language Models (LLMs), it automates the most time-consuming aspects of the QA
lifecycle—transforming raw text into structured Jira tickets, BDD scenarios, and executable automation scripts.

---

## 🚀 Core Features

* **Jira Ticket Generator:** Converts high-level feature requests into professional user stories with "Given-When-Then"
  acceptance criteria.
* **Gherkin BDD Scenarios:** Automatically maps requirements to feature files, ensuring 100% requirement traceability.
* **Selenium Script Architect:** Generates boilerplate Python/Java Selenium code directly from BDD steps, following Page
  Object Model (POM) best practices.
* **Interactive UI:** A modern, dark-themed dashboard built with FastAPI and integrated into a professional SDET
  portfolio.

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **AI Orchestration:** LangChain / OCI GenAI (or OpenAI)
* **Frontend:** HTML5, CSS3 (Modern Navy/Teal Theme), JavaScript (ES6)
* **Deployment:** Render / Docker

---

## 📝 Sample Input & Output

To see the "Magic" in action, try the following sample input in the QA Genie modal:

### **Sample Input (Requirement)**

> "As a user, I want to be able to reset my password using my registered email address so that I can regain access to my
> account if I forget my credentials."

### **Generated Magic (Example Output)**

#### **1. Jira Ticket**

**Summary:** Implement Password Reset Functionality  
**Description:** Enable users to trigger a password reset link via email.  
**Acceptance Criteria:** - Verify a 'Forgot Password' link exists on the login page.

- Verify an email is sent only to registered users.
- Reset link must expire after 24 hours for security.

#### **2. Gherkin BDD**

```gherkin
Feature: Password Recovery
  Scenario: Successful password reset request
    Given the user is on the login page
    When the user clicks on "Forgot Password"
    And enters a valid registered email "test@example.com"
    Then a reset link should be sent to the email


📦 Installation & Local Setup
1. Prerequisites
    Python 3.9+
    An OCI (Oracle Cloud) account or OpenAI API Key
    Git installed on your local machine2. Clone the Repository

    Bash
    git clone https://github.com/kouddy3004/my_Project.git
    cd pythonProject/qa-genie

3. Create a Virtual Environment
Bash
# Create the environment
python -m venv venv
# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

4. Install Dependencies
Bash
pip install -r requirements.txt

5. Environment Configuration
Create a .env file in the root directory and add your credentials:
Code snippet
OPENROUTER_API_KEY={Your API Key}
# Add other keys as required by your specific LangChain implementation

6. Run the Application
Bash
uvicorn main:app --reload
Once started, open your browser and navigate to: http://127.0.0.1:8000

👨‍💻 Author
Koushik S. Senior SDET | Automation Architect LinkedIn | GitHub