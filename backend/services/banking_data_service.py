from services.search_service import SearchService
from supabase import create_client
from config import Config
from datetime import datetime

class BankingDataService:
    def __init__(self):
        self.search_service = SearchService()
        self.supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        
        self.banks_list = [
            "State Bank of India (SBI)",
            "HDFC Bank",
            "ICICI Bank",
            "Axis Bank",
            "Punjab National Bank (PNB)",
            "Bank of Baroda",
            "Canara Bank",
            "Union Bank of India",
            "Bank of India",
            "IndusInd Bank",
            "Kotak Mahindra Bank",
            "Yes Bank",
            "IDBI Bank",
            "Central Bank of India",
            "Indian Bank"
        ]
    
    def get_banks_list(self):
        """Return list of supported banks"""
        return self.banks_list
    
    def fetch_latest_updates(self, category="all", limit=20):
        """Fetch latest banking updates from various sources"""
        try:
            updates = []
            
            categories_to_fetch = [category] if category != "all" else [
                "loans", "rbi", "farmers", "insurance", "general"
            ]
            
            for cat in categories_to_fetch:
                results = self.search_service.get_latest_banking_updates(cat)
                
                for result in results:
                    update = {
                        'title': result.get('title', ''),
                        'description': result.get('snippet', ''),
                        'category': cat,
                        'source': result.get('link', ''),
                        'url': result.get('link', ''),
                        'created_at': datetime.utcnow().isoformat()
                    }
                    updates.append(update)
            
            # Store in database
            if updates:
                self._store_updates(updates)
            
            return updates[:limit]
            
        except Exception as e:
            print(f"Error fetching latest updates: {e}")
            return []
    
    def _store_updates(self, updates):
        """Store updates in database"""
        try:
            # Check if updates already exist
            for update in updates:
                existing = self.supabase.table("banking_updates")\
                    .select("id")\
                    .eq("title", update['title'])\
                    .execute()
                
                if not existing.data:
                    self.supabase.table("banking_updates").insert(update).execute()
        except Exception as e:
            print(f"Error storing updates: {e}")
    
    def search_bank_locations(self, query, bank_name=None):
        """Search for bank branches and ATMs"""
        try:
            if bank_name:
                search_query = f"{bank_name} branches ATMs near {query}"
            else:
                search_query = f"bank branches ATMs near {query}"
            
            results = self.search_service.search_web(search_query)
            return results
            
        except Exception as e:
            print(f"Error searching bank locations: {e}")
            return []
    
    def get_bank_specific_info(self, bank_name, info_type):
        """Get specific information about a bank"""
        query_map = {
            'interest_rates': f"{bank_name} interest rates 2025",
            'loan_eligibility': f"{bank_name} loan eligibility criteria",
            'account_types': f"{bank_name} account types and features",
            'credit_cards': f"{bank_name} credit cards benefits",
            'customer_care': f"{bank_name} customer care contact number"
        }
        
        query = query_map.get(info_type, f"{bank_name} {info_type}")
        return self.search_service.search_web(query)
