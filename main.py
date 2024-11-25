#streamlit run main.py

import streamlit as st
from relationships import nltk_relationnship
import pandas as pd
import nltk

nltk.data.path.append('./nltk_data')

st.set_page_config(page_title="Wordy - NLTK WordNet Explorer", layout="wide")

st.title('🐾 You Found Wordy!!')
user_input = st.text_input('Type in a word, and Wordy will fetch some magic for you! ✨')
if st.button('search'):
    if user_input.strip():
        st.write(f'Yayyy!found something interesting for {user_input}')
        
        st.markdown('🐾**NLTK WordNet**')
        relationships = nltk_relationnship(user_input)
        
        if not relationships:
            st.write(f"Sorry, we couldn't find anything for **'{user_input}'**. Try another word! 🐾")

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
        