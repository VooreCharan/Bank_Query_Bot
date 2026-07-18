from groq import Groq
from services.search_service import SearchService
from config import Config
import re

class BankingAIAgent:
    def __init__(self):
        try:
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.model_name = "llama-3.3-70b-versatile"

            print("✓ Groq client initialized")
        except Exception as e:
            print(f"✗ Groq initialization failed: {e}")
            self.client = None
            self.model_name = None

        try:
            self.search_service = SearchService()
            print("✓ Search service initialized")
        except Exception as e:
            print(f"Warning: Search service initialization failed: {e}")
            self.search_service = None

    def clean_response(self, text):
        if not text:
            return text
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        return text.strip()

    def detect_location_query(self, query):
        location_keywords = [
            "near me", "nearby", "close to me", "closest",
            "find bank", "find atm", "find branch",
            "locate bank", "locate atm", "locate branch",
            "bank location", "atm location", "branch location",
            "where is", "where can i find",
            "around me", "in my area",
        ]
        q = query.lower()
        return any(k in q for k in location_keywords)

    def _generate(self, prompt: str) -> str:
        """Call Groq chat completion API with a simple helper."""
        if not self.client or not self.model_name:
            return (
                "The AI service is currently unavailable because the Groq API key "
                "is missing or invalid."
            )

        chat = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful banking assistant for Indian banks."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return chat.choices[0].message.content

    def process_query(self, user_id, session_id, query, bank_name=None, language="en"):
        try:
            print(f"[DEBUG] Processing: {query}")

            if not self.client or not self.model_name:
                return {
                    "answer": (
                        "The AI service is currently unavailable because the Groq API "
                        "key or model configuration is not valid."
                    ),
                    "sources": [],
                    "language": "en",
                    "needs_location": False,
                }

            if self.detect_location_query(query):
                return {
                    "answer": (
                        "I can help you find nearby banks and ATMs!\n\n"
                        "Please click the 'Find Locations' button in the chat header, then:\n"
                        "1. Enter your city, area, or address\n"
                        "2. Or click 'Use Current Location' to detect your position\n"
                        "3. View nearby banks and ATMs with distances and directions\n\n"
                        "You can also tell me your specific location "
                        "(e.g., 'Mumbai, Andheri' or 'Bangalore, MG Road')."
                    ),
                    "sources": [],
                    "language": language,
                    "needs_location": True,
                }

            search_results = []
            if self.search_service:
                try:
                    search_results = self.search_service.search_banking_info(query, bank_name)
                    print(f"[DEBUG] Found {len(search_results)} search results")
                except Exception as e:
                    print(f"[WARNING] Search failed: {e}")

            context = ""
            if bank_name:
                context += f"\nBank Context: {bank_name}"
            if search_results:
                context += "\n\nRelevant Information:"
                for idx, result in enumerate(search_results[:3], 1):
                    context += f"\n{idx}. {result.get('title', '')}"
                    context += f"\n   {result.get('snippet', '')}"

            prompt = f"""You are an expert Banking Customer Service AI Assistant for Indian banks.

Your role:
- Answer banking queries accurately and professionally
- Provide step-by-step guidance for banking procedures
- Explain banking terms clearly
- Help with accounts, loans, cards, and digital banking

Guidelines:
- Be polite, professional, and helpful
- Provide accurate information based on context
- If unsure, suggest contacting the bank
- Format answers with bullet points or numbered steps when appropriate
- Use single line breaks between points
- Keep responses concise and well-organized
- Avoid excessive spacing between sections

{context}

User Question: {query}

Provide a clear, well-formatted answer:"""

            print("[DEBUG] Generating response with Groq...")
            raw_answer = self._generate(prompt)
            answer = self.clean_response(raw_answer)
            print(f"[DEBUG] Response generated: {len(answer)} characters")

            return {
                "answer": answer,
                "sources": search_results[:3],
                "language": language,
                "needs_location": False,
            }

        except Exception as e:
            print(f"[ERROR] process_query failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "answer": (
                    "I encountered an internal error while processing your request. "
                    "Please try again later."
                ),
                "sources": [],
                "language": language,
                "needs_location": False,
            }

    def get_banking_faq_answer(self, question, bank_name=None):
        try:
            if not self.client or not self.model_name:
                return (
                    "The AI FAQ service is currently unavailable because the Groq API "
                    "configuration is not valid."
                )

            prompt = f"""Answer this banking question concisely and clearly:

Question: {question}
Bank: {bank_name if bank_name else 'General Banking'}

Provide a clear, well-formatted answer with bullet points or steps if needed."""
            raw = self._generate(prompt)
            return self.clean_response(raw)
        except Exception as e:
            print(f"FAQ error: {e}")
            return "Unable to answer this question right now due to an internal error."

    def format_location_response(self, location_data):
        if not location_data or not location_data.get("results"):
            return "No banks or ATMs found in this area."

        results = location_data["results"][:5]
        response = (
            f"Found {len(results)} banking facilities near "
            f"{location_data.get('location', 'your location')}:\n\n"
        )

        for idx, bank in enumerate(results, 1):
            response += f"{idx}. **{bank['name']}** ({bank['type']})\n"
            response += f"   📍 {bank['address']}\n"
            response += f"   📏 {bank['distance_km']} km away\n"
            if bank.get("phone"):
                response += f"   📞 {bank['phone']}\n"
            if bank.get("opening_hours"):
                response += f"   ⏰ {bank['opening_hours']}\n"
            response += "\n"

        return self.clean_response(response)
