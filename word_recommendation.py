import openai
import os
import random
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Predefined themes
THEMES = [
    'verbs', 'food', 'household', 'emotions', 'weather',
    'family', 'clothes', 'transport', 'time', 'body'
]

def get_random_theme():
    """Return a random theme from the predefined list"""
    return random.choice(THEMES)

def get_words_for_theme(theme, count=10, used_words=None):
    if used_words is None:
        used_words = set()

    try:
        # Simplified prompt - only asking for words
        prompt = f"""Generate exactly {count} simple, common English words related to the theme '{theme}'.
        Requirements:
        - Words should be suitable for English beginners
        - Only single words, no phrases
        - Use basic forms (singular nouns, present tense verbs)
        - Words should be common in daily life
        - Words must be different from: {', '.join(used_words)}
        
        Return ONLY the list of words, one per line."""

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a word generator that returns simple word lists."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Get just the words as a list
        words = response.choices[0].message.content.strip().split('\n')
        words = [word.strip() for word in words]  # Clean up any extra whitespace
        
        # Filter out duplicates
        filtered_words = [word for word in words 
                         if word.lower() not in used_words]
        
        return filtered_words[:count]

    except Exception as e:
        print(f"Error in get_words_for_theme: {e}")
        return ["error loading words"]