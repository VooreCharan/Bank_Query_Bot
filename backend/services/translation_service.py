from deep_translator import GoogleTranslator

class TranslationService:
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'te': 'Telugu',
            'ta': 'Tamil',
            'bn': 'Bengali',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi'
        }
    
    def detect_language(self, text):
        """Detect language of input text - simple implementation"""
        try:
            # Check for non-ASCII characters (indicates non-English)
            has_non_ascii = any(ord(char) > 127 for char in text)
            
            if not has_non_ascii:
                return 'en'
            
            # Try to detect using deep-translator
            # For simplicity, return 'hi' for non-English
            # You can enhance this with langdetect library
            return 'hi'
            
        except Exception as e:
            print(f"Error detecting language: {e}")
            return 'en'
    
    def translate(self, text, target_lang='en', source_lang='auto'):
        """Translate text to target language"""
        try:
            if source_lang == 'auto':
                source_lang = self.detect_language(text)
            
            if source_lang == target_lang:
                return text
            
            # Use deep-translator for translation
            translated = GoogleTranslator(
                source=source_lang, 
                target=target_lang
            ).translate(text)
            
            return translated
            
        except Exception as e:
            print(f"Error translating text: {e}")
            return text
    
    def get_supported_languages(self):
        """Return list of supported languages"""
        return self.supported_languages
