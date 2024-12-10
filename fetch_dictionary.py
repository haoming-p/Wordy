import requests
from googletrans import Translator

def fetch_dictionary_data(word):
    pos_map = {
        'noun': '名词',
        'verb': '动词',
        'adjective': '形容词',
        'adverb': '副词',
        'preposition': '介词',
        'conjunction': '连词',
        'interjection': '感叹词'
    }
    
    # fetch dictionary api
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)

    if response.status_code != 200:
        return None, f"error: {response.json().get('message', 'word not found')}"
    
    data = response.json()
    print("API Meanings:", data[0]['meanings'])
    translator = Translator()

    try:
        formatted_meanings = []
        # 3 top usage
        for word_entry in data:
            # phonetic, audio
            phonetics = word_entry.get('phonetics', [])
            if phonetics:
                phonetic = phonetics[0].get('text')
                audio = phonetics[0].get('audio')

            if word_entry.get('meanings'):
                # 1 definition's pos, definition, example
                meaning = word_entry['meanings'][0]
                pos = meaning.get('partOfSpeech', '')
                pos_chinese = pos_map.get(pos, pos)

                if meaning.get('definitions'):
                    definition = meaning.get('definitions')[0]
                    english_definition = definition.get('definition')
                    chinese_definition = translator.translate(english_definition, src='en', dest='zh-cn').text if english_definition else ''
                    english_example = definition.get('example')
                    chinese_example = translator.translate(english_example, src='en', dest='zh-cn').text if english_example else ''
        
                    
            formatted_meanings.append({
                'phonetic': phonetic,
                'audio': audio,
                'partOfSpeech': pos,
                'chinese_pos': pos_chinese,
                'english_definition': english_definition,
                'chinese_definition': chinese_definition,
                'english-example': english_example,                    
                'chinese_example': chinese_example
                })

        return {
            'chinese_word': translator.translate(word, src='en', dest='zh-cn').text,
            'meanings': formatted_meanings
        }, None
    

    
    
    except Exception as e:
        return None, f"Error processing dictionary data: {str(e)}"
    