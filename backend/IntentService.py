# ============================================
# SERVICE LAYER (Intent Detection)
# This layer uses fuzzy matching to classify user intents.
# ============================================

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
CONFIDENCE_THRESHOLD = 75  # Minimum score to accept an intent match

class IntentService:
    """
    Architecture: Service layer for intent classification.
    Separates NLU logic from request handling.
    """
    
    def __init__(self, intent_map, threshold=CONFIDENCE_THRESHOLD):
        self.intent_map = intent_map
        self.threshold = threshold
    
    def detect_intent(self, user_text):
        """
        Detect user intent using fuzzy matching.
        Returns: (intent_name, confidence_score) or (None, 0)
        """
        if not user_text:
            return None, 0
        
        user_text_lower = user_text.lower()
        detected_intent = None
        highest_score = 0
        
        for intent, phrases in self.intent_map.items():
            # Find best match among synonyms
            best_match, score = process.extractOne(
                user_text_lower, 
                phrases, 
                scorer=fuzz.partial_ratio
            )
            
            if score > highest_score:
                highest_score = score
                detected_intent = intent
        
        if highest_score >= self.threshold:
            return detected_intent, highest_score
        
        return None, highest_score