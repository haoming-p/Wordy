#streamlit run main.py

import streamlit as st
from relationships import nltk_relationnship
import pandas as pd
import nltk
from word_recommendation import get_words_for_theme, get_random_theme
from fetch_dictionary import fetch_dictionary_data

nltk.data.path.append('./nltk_data')

# Set up the page
st.set_page_config(page_title="Wordy", layout="wide")

# Custom CSS for dictionary cards
st.markdown("""
<style>
.meaning-card {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs(["Dictionary", "Daily Words"])

with tab1:
    st.title('🐾 You Found Wordy!!')
    user_input = st.text_input('Type in a word, and Wordy will fetch some magic for you! ✨')
    
    if st.button('search'):
        if user_input.strip():
            st.write(f'Yayyy! Wordy found something interesting for {user_input}! ✨')
            
            # WordNet
            st.markdown('💓 **NLTK WordNet**')
            relationships = nltk_relationnship(user_input)
            if not relationships:
                st.write(f"Sorry, we couldn't find anything for **'{user_input}'**. Try another word! 🐾")
            else:
                data = []
                for r in relationships:
                    data.append({
                        'Definition': r['definition'],
                        'Example': r['example']['top'] if r['example']['top'] else '',
                        'Synonym': ', '.join(r['synonym']['top']),
                        'Hyponyms': ', '.join(r['hyponyms']['top']),
                        'Siblings': ', '.join(r['siblings']['top']),
                        'Metonyms': ', '.join(r['metonym']['top']),
                    })
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
            
            # Dictionary
            st.markdown('📚 **Dictionary**')
            dict_data, error = fetch_dictionary_data(user_input)
            
            if error:
                st.error(error)
            else:
                # Display the most common Chinese translation
                st.markdown(f"### {user_input} 的中文: {dict_data['chinese_word']}")
                
                # Display up to 3 meanings in expandable cards (default expanded)
                for i, meaning in enumerate(dict_data['meanings'][:3]):
                    with st.expander(f"Meaning {i+1}: {meaning['partOfSpeech']} ({meaning['chinese_pos']})", expanded=True):
                        # Phonetics and audio
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if meaning.get('phonetic'):
                                st.write(f"🔊 {meaning['phonetic']}")
                        with col2:
                            if meaning.get('audio'):
                                st.audio(meaning['audio'], format='audio/mp3')
                        
                        # Definition
                        st.markdown("**Definition**")
                        st.write(meaning['english_definition'])
                        st.write(f"🇨🇳 {meaning['chinese_definition']}")
                        
                        # Example
                        if meaning.get('english-example'):
                            st.markdown("**Example**")
                            st.write(f"*{meaning['english-example']}*")
                            st.write(f"🇨🇳 *{meaning['chinese_example']}*")

with tab2:
    # Initialize session state (same as before)
    if 'theme' not in st.session_state:
        st.session_state['theme'] = get_random_theme()
    if 'word_sets' not in st.session_state:
        st.session_state['word_sets'] = {}
    if 'completed_sets' not in st.session_state:
        st.session_state['completed_sets'] = set()
    if 'all_used_words' not in st.session_state:
        st.session_state['all_used_words'] = set()

    st.header("📚 Daily Word Sets")
    st.subheader(f"Today's Theme: {st.session_state['theme'].upper()}")
    
    # Create 5 columns for word sets
    cols = st.columns(5)
    for i, col in enumerate(cols, 1):
        with col:
            st.write(f"Set {i}")
            if i in st.session_state['completed_sets']:
                st.success("✅ Completed")
                if i in st.session_state['word_sets']:
                    # Changed: directly use the word since it's now a string
                    for idx, word in enumerate(st.session_state['word_sets'][i], 1):
                        st.write(f"{idx}. {word}")
            else:
                if st.button(f"Show Set {i}"):
                    if i not in st.session_state['word_sets']:
                        words = get_words_for_theme(
                            st.session_state['theme'], 
                            10, 
                            st.session_state['all_used_words']
                        )
                        st.session_state['word_sets'][i] = words
                        # Changed: directly use words since they're now strings
                        st.session_state['all_used_words'].update(w.lower() for w in words)
                    
                    # Changed: directly use the word since it's now a string
                    for idx, word in enumerate(st.session_state['word_sets'][i], 1):
                        st.write(f"{idx}. {word}")
                    
                    if st.button(f"Mark Set {i} Complete"):
                        st.session_state['completed_sets'].add(i)
                        if len(st.session_state['completed_sets']) == 5:
                            st.balloons()
                            st.success("真棒！马上就要来美国玩啦！")
                        else:
                            st.success(f"{len(st.session_state['completed_sets'])}/5 for today")
                        st.rerun()

    # Change theme button (same as before)
    if st.button('Try Another Theme'):
        st.session_state['theme'] = get_random_theme()
        st.session_state['word_sets'] = {}
        st.session_state['completed_sets'] = set()
        st.session_state['all_used_words'] = set()
        st.rerun()