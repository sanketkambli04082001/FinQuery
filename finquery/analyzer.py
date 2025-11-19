import os
import fitz
import json
from dotenv import load_dotenv

import google.generativeai as genai
from google.generativeai import types

# ------------------------------------------------------------------------

load_dotenv()

class ReportAnalyzer:

    def __init__(self):
        
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("API key 'GOOGLE_API_KEY' not found in .env file.")
        
        genai.configure(api_key=self.google_api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]


# ======================summarize text block====================================================================================
    def summarize_text(self, text_to_summarize):
        prompt = (
                "You are a senior equity research analyst who explains financials in simple, beginner-friendly English.\n"
                "Rewrite the text into EXACTLY 5 bullet points.\n\n"
                
                "STRICT FORMAT (follow exactly):\n"
                "- Headline: <1 short sentence summarizing the idea>.\n"
                "  Details:\n"
                "  • <Metric Label>: <Value>\n"
                "  • <Metric Label>: <Value>\n"
                "  • <Optional 3rd bullet if needed>\n\n"
                
                "STYLE RULES:\n"
                "1) Each bullet must express ONE big idea only (growth, profitability, segments, balance sheet, risks, etc).\n"
                "2) Use VERY simple English — assume the reader is new to finance.\n"
                "3) Use the ₹ symbol correctly — NEVER output 'J'.\n"
                "4) Group related numbers together (e.g., all revenue numbers in one bullet).\n"
                "5) Never dump too many numbers — 2 to 3 metrics per bullet maximum.\n"
                "6) Use commas in Indian format (₹1,54,119 crore).\n"
                "7) No extra text, no intros, no outros — ONLY the 5 bullets.\n"
                "8) Explain context in the headline, numbers in the details.\n\n"
                
                "Your goal: Make the summary feel like a clean, human-written research note intro.\n\n"
                
                "TEXT TO SUMMARIZE:\n"
                f"{text_to_summarize}"
            )

        print("--- Calling AI for summary... ---")
        try:
            response = self.model.generate_content(prompt,
                safety_settings=self.safety_settings)
            return response.text
        except Exception as e:
            print(f"An error occurred while calling the AI: {e}")
            return "Error: Could not generate summary."


# ======================extract text block====================================================================================
    def extract_text_from_pdf(self,pdf_file_path):
        print(f"--- Extracting from {pdf_file_path} ---")
        try:
            doc = fitz.open(pdf_file_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()

            doc.close()
            return full_text
        except Exception as e:
            print(f"An error occured while extracting text from pdf")
            return None

# ======================extract text block====================================================================================        
    def get_competitors(self,text_to_analyze):
        prompt = (
            "Step 1: Identify the main company discussed in the following text.\n"
            "Step 2: Based on your general knowledge, identify 3 major publicly traded competitors for that company.\n"
            "Step 3: Return ONLY a raw JSON object with exactly two keys: 'main_ticker' (string) and 'competitors' (list of strings).\n"
            "Example: { \"main_ticker\": \"MSFT\", \"competitors\": [\"GOOG\", \"AMZN\"] }\n\n"
            "TEXT TO ANALYZE:\n"
            f"{text_to_analyze}"
        )
        print("--- Calling AI to find compitators.. ---")
        try:
            response = self.model.generate_content(prompt,
                safety_settings=self.safety_settings)
            
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            company_data = json.loads(clean_json)
            return company_data
        except Exception as e:
            print(f"an error occurred : {e}")
            return {"main_ticker": "UNKNOWN", "competitors": []}

# ======================user query block====================================================================================        
    def answer_question(self, text_to_analyze, user_question):
        prompt = (
                        f"""
            You are a concise financial analyst. Answer ONLY from the REPORT TEXT below.

            INSTRUCTIONS (must follow exactly):
            1) FIRST LINE — give a one-sentence short answer (<= 30 words).
            2) If the user needs more detail, include a small 'Details:' section with at most 4 bullet points (each bullet max 2 short sentences).
            3) When numbers appear, show value + simple explanation, e.g. "Revenue: ₹10,71,174 crore (US$125.3B) — up 7.1% YoY."
            4) If the question is about investing (safe? buy? sell? hold?), do NOT give investment advice. Instead reply:
            "The report does not give investment advice, but here is what it says:" followed by facts.
            5) If the information is NOT in the text, reply exactly: "The report does not mention this."
            6) Use simple, beginner-friendly English. Keep everything short and clear.
            7) Do NOT invent facts or add outside knowledge.

            USER QUESTION:
            {user_question}

            REPORT TEXT:
            {text_to_analyze}
            """
        )

        print(f"--- Asking AI for Q&A: '{user_question}' (text chars: {len(text_to_analyze)}) ---")
        try:
            response = self.model.generate_content(prompt, safety_settings=self.safety_settings)
            return response.text
        except Exception as e:
            print(f"An error occurred while answering question: {e}")
            return "Error: Could not generate answer."
        

# ======================Chart analysis block====================================================================================        
    def extract_financial_table(self, text_to_analyze):
        prompt = (
            "Extract the revenue figures from the text below. "
            "If quarterly data is available return quarterly keys like "
            "{\"Q1 FY25\": 62613, \"Q2 FY25\": 64000}. "
            "If quarterly is NOT available but annual data is present, "
            "return annual keys like {\"FY21\": 45000, \"FY22\": 52000}. "
            "Return ONLY a raw JSON object and nothing else (no words, no explanation).\n\n"
            "TEXT TO ANALYZE:\n" + text_to_analyze
        )

        print("--- Calling AI to extract table data... ---")
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            raw_text = response.text or ""
            clean_json_text = raw_text.replace("```json", "").replace("```", "").strip()

    
            try:
                chart_data = json.loads(clean_json_text)
                print("--- [Analyzer] Table JSON parsed successfully.")
                return chart_data
            except Exception as e:
                print(f"--- [Analyzer] JSON parsing failed: {e}")
                print("--- [Analyzer] AI output was:\n", clean_json_text)
               
                return {}

        except Exception as e:
            print(f"An error occurred while extracting table: {e}")
            return {}