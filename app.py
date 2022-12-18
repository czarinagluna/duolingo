import streamlit as st
import pandas as pd
import base64
from google_trans_new import google_translator
from constant import LANGUAGES

st.set_page_config(
     page_title='Duo Dictionary',
     page_icon='favicon.png',
    #  initial_sidebar_state='expanded',
    #  menu_items={
    #      'Get Help': 'https://www.extremelycoolapp.com/help',
    #      'Report a bug': "https://www.extremelycoolapp.com/bug",
    #      'About': "# This is a header. This is an *extremely* cool app!"
    #  }
)

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64('background.png')

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: 70vw;
background-position: bottom;
background-repeat: no-repeat;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title('Duolingo Dictionary')

# df = pd.DataFrame(columns=['Name', 'Language', 'Translation', 'English'])
# df.to_csv('data.csv', index=False)

df = pd.read_csv('data.csv')

with st.expander('Enter data'):
    user = st.text_input('Name')
    language = st.text_input('Language')
    translation = st.text_input(language)
    english = st.text_input('English')

    col1, col2 = st.columns(2)
    if col1.button('Add'):
        row = {'Name': user, 'Language': language, 'Translation': translation, 'English': english}
        df = pd.read_csv('data.csv')
        df = df.append(row, ignore_index=True)
        df.to_csv('data.csv', index=False)
        df = pd.read_csv('data.csv').drop_duplicates()
        data = df.loc[(df['Name']==user) & (df['Language']==language), ['English', 'Translation']]
        st.write(data)

    if col2.button('Remove'):
        row = {'Name': user, 'Language': language, 'Translation': translation, 'English': english}
        df = df.drop(df.loc[(df['Name']==user) & 
                            (df['Language']==language) &
                            (df['Translation']==translation) &
                            (df['English']==english)].index)
        df.to_csv('data.csv', index=False)
        df = pd.read_csv('data.csv')
        data = df.loc[(df['Name']==user) & (df['Language']==language), ['Translation', 'English']]
        st.write(data)

with st.expander('Display data'):
    name = st.text_input('Enter user')
    luser = st.text_input('Enter language')

    if st.button('Display'):
        df = pd.read_csv('data.csv').drop_duplicates()
        data = df.loc[(df['Name']==name) & (df['Language']==luser), ['Translation', 'English']]
        st.write(data)

with st.expander('Search data'):
    term = st.text_input('Search')
    if term:
        df = pd.read_csv('data.csv').drop_duplicates()
        result = df.loc[(df['English'].str.contains(term, case=False)) | (df['Translation'].str.contains(term, case=False)), ['Translation', 'English']]
        st.write(result)

translator = google_translator()  

languages = [' ']
languages.extend(list(LANGUAGES.values()))

map = {val: key for key, val in LANGUAGES.items()}

with st.expander('Translate data'):
    from_ = st.selectbox('From',
        ('English', 
        'Spanish', 
        'Portuguese',
        'Polish',
        'Other'))
    
    if from_ == 'Other':
        from_ = st.text_input('Other language')

    if from_.lower() not in languages:
        st.write('Language may not be supported by the API. Check the list of supported languages below.')

    to_ = st.selectbox('To',
        ('English', 
        'Spanish', 
        'Portuguese',
        'Polish',
        'Other'))
    
    if to_ == 'Other':
        to_ = st.text_input('Other language ')

    if to_.lower() not in languages:
        st.write('Language may not be supported by the API. Check the list of supported languages below.')

    text_ = st.text_area('Text')

    if st.button('Translate'):
        src_ = map[from_.lower()]
        tgt_ = map[to_.lower()]
        result = translator.translate(lang_src=src_, text=text_, lang_tgt=tgt_)  
        st.write(result)

    st.selectbox('(Search supported languages)', 
    languages)
