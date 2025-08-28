import openai
import requests

class AIChatAssistant:
    def __init__(self, api_key):
        openai.api_key = api_key
        
    def moderate_content(self, text):
        """
        Moderate content using OpenAI's moderation API
        """
        try:
            response = openai.Moderation.create(input=text)
            result = response["results"][0]
            
            return {
                "flagged": result["flagged"],
                "categories": result["categories"],
                "category_scores": result["category_scores"],
                "reason": self._get_moderation_reason(result["categories"])
            }
        except Exception as e:
            # Fallback to simple content check if API fails
            return self._simple_content_check(text)
    
    def _simple_content_check(self, text):
        """
        Simple content check as fallback
        """
        inappropriate_words = ['naked', 'nude', 'explicit', 'xxx', 'porn', 'nude', 'naked']
        text_lower = text.lower()
        
        for word in inappropriate_words:
            if word in text_lower:
                return {
                    "flagged": True,
                    "categories": {"sexual": True},
                    "category_scores": {"sexual": 0.9},
                    "reason": "Contains inappropriate content"
                }
        
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "reason": ""
        }
    
    def _get_moderation_reason(self, categories):
        """
        Generate a human-readable reason for moderation
        """
        reasons = []
        for category, flagged in categories.items():
            if flagged:
                reasons.append(category)
        
        if reasons:
            return f"Content flagged for: {', '.join(reasons)}"
        return ""
    
    def generate_response(self, conversation_history):
        """
        Generate AI response based on conversation history
        """
        try:
            # Format conversation for OpenAI
            messages = []
            for msg in conversation_history:
                role = "user" if msg["role"] == "user" else "assistant"
                messages.append({"role": role, "content": msg["content"]})
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message['content'].strip()
        except Exception as e:
            # Fallback responses if AI fails
            fallback_responses = [
                "I'm sorry, I didn't understand that.",
                "Could you please rephrase that?",
                "I'm having trouble processing your request right now.",
                "Let's talk about something else.",
                "That's interesting! Tell me more."
            ]
            
            import random
            return random.choice(fallback_responses)
    
    def translate_message(self, text, target_language):
        """
        Translate message using AI
        """
        try:
            prompt = f"Translate the following text to {target_language}:\n\n{text}"
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                temperature=0.3
            )
            
            return response.choices[0].text.strip()
        except Exception as e:
            return text  # Return original text if translation fails
