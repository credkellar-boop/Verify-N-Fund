import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Crucial Step: Define the System Instruction to lock Gemini to the project domain
VERIFY_N_FUND_PROMPT = """
You are the proprietary AI Assistant for the 'Verify-N-Fund' platform. 
Your sole purpose is to help companies, compliance officers, and tellers verify checks, understand fraud risks, and navigate financial verification workflows.

CRITICAL RULE: You must ONLY answer questions directly related to the Verify-N-Fund project, check verification protocols, identity validation, routing/MICR numbers, or financial compliance. 

If the user asks an off-topic question (e.g., world history, general coding, creative writing, recipe advice, general banter), you must reply with exactly this message:
"I am programmed strictly to handle Verify-N-Fund and check verification queries. I cannot assist with outside topics."
"""

def query_verify_agent(user_question: str) -> str:
    """
    Queries the Gemini model with strict guardrails to assist busy companies.
    """
    try:
        # Utilizing gemini-2.5-flash for fast, cost-effective enterprise operations
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=VERIFY_N_FUND_PROMPT
        )
        
        response = model.generate_content(user_question)
        return response.text
        
    except Exception as e:
        return f"System Error: Unable to process verification query. Details: {str(e)}"

# Example Usage
if __name__ == "__main__":
    # Test Case 1: On-topic query
    print("--- Testing On-Topic Query ---")
    on_topic = "What features should our tellers look for to spot a fake MICR line?"
    print(f"User: {on_topic}")
    print(f"Gemini: {query_verify_agent(on_topic)}\n")
    
    # Test Case 2: Off-topic query (Should be blocked)
    print("--- Testing Off-Topic Query ---")
    off_topic = "Can you write a python script to scrape a weather website?"
    print(f"User: {off_topic}")
    print(f"Gemini: {query_verify_agent(off_topic)}")
