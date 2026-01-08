# ResponseService contains the logic for generating responses based on detected intents.
class ResponseService:
    """
    Architecture: Service layer for response generation.
    """
    
    def __init__(self, response_map, fallback):
        self.response_map = response_map
        self.fallback = fallback
    
    def get_response(self, intent):
        """
        Get response for detected intent.
        """
        if intent and intent in self.response_map:
            return self.response_map[intent]
        return self.fallback