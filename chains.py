import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Add this line to print the GROQ_API_KEY (for debugging, remove in production)
print(f"GROQ_API_KEY: {os.getenv('GROQ_API_KEY')}")

class Chain:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.llm = ChatGroq(temperature=0.6, groq_api_key=api_key, model_name="llama-3.1-70b-versatile")

    def extract_and_generate_email(self, cleaned_text, portfolio_links):
        prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### PORTFOLIO LINKS:
            {portfolio_links}

            ### INSTRUCTION:
            1. Analyze the scraped text and identify the most relevant job posting.
            2. Extract key information such as job title, required skills, and responsibilities.
            3. Write a cold email for the identified job position. The email should:
               - Be addressed to the hiring manager (use a generic title if no specific name is found)
               - Introduce yourself as Engineer from Digital Garage INC
               - Highlight how Digital Garage INC's expertise aligns with the job requirements
               - Mention relevant portfolio links that showcase similar work
               - Express enthusiasm for the role and company
               - Request a follow-up conversation or interview
               - Close professionally

            ### OUTPUT:
            Provide the cold email directly, without any preamble or explanation.
            """
        )
        
        try:
            res = self.llm.invoke(prompt.format(page_data=cleaned_text, portfolio_links=portfolio_links))
            return res.content
        except Exception as e:
            print(f"Error in extract_and_generate_email: {e}")
            return "Error generating email content."
