import streamlit as st
import pandas as pd
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

from gpt_structure import dd_generate_gpt4_basic
from knowledge_structure import *

st.set_page_config(
    page_title="[SNU 스무살의 나] Knowledge & First letter",
    page_icon="📩",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items= {
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': 'SNU 스무살의 나 실험용 플랫폼',
    }
)

# @st.cache_data(ttl=30)
# def load_data(file_name):
#   df = pd.read_csv(file_name)
#   return df

spc_df = pd.read_csv("https://docs.google.com/spreadsheets/d/1DI8Nc1v9qIhFcg2SloNsVj-33nTF8NeAiatnf_7TKwA/export?format=csv&gid=117892638")
authentic_df = pd.read_csv("https://docs.google.com/spreadsheets/d/1h84YK25uLQUQyD4u_TGQOeQEQgDvvQeto8ynkmowK6I/export?format=csv&id=1h84YK25uLQUQyD4u_TGQOeQEQgDvvQeto8ynkmowK6I&gid=902877586")
future_df = pd.read_csv("https://docs.google.com/spreadsheets/d/1o7bkh7SZ7vD-XLDgdoV-DOouDIl64PVx3K13iWLeSCk/export?format=csv&gid=397229261")
pre_df = pd.read_csv("https://docs.google.com/spreadsheets/d/12jnbvjOgdLy96UCeXgc5p2A3-0BWH1RLKD3gF5sqdRU/export?format=csv&gid=1266426431")

streamlit_style = """
			<style>
			@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

			html, body, [class*="css"],g {
			  font-family: Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
      }
			</style>
			"""

st.markdown(streamlit_style, unsafe_allow_html=True)

st.title('[SNU 스무살의 나] Knowledge & First letter')
st.markdown('---')

system_lib_file = 'data/prompt_template/first_letter_sys_prompt.txt'
f = open(system_lib_file, "r")
first_letter_sys_prompt = f.read()
f.close()

with st.form('prompt_selector'):
  user_name = st.radio(
            "Select User Name 👉",
            key="user_name",
            options = spc_df.iloc[:,1].unique() # 이름
  )

  submit = st.form_submit_button('Submit')

if submit:
    main_test = spc_df[spc_df.iloc[:,1] == user_name] # 이름
    authentic_test = authentic_df[authentic_df.iloc[:,1] == user_name] # 이름
    future_test = future_df[future_df.iloc[:,3] == user_name] # 이름
    pre_test = pre_df[pre_df.iloc[:,2] == user_name] # 이름

    with st.spinner('Wait for structuring knowledge...'):
        demo = demo_generate(main_test)
        love_hate = love_hate_generate(main_test)
        bfi = bfi_generate(main_test)
        pvq = pvq_generate(main_test)
        authenticity = authenticity_generate(authentic_test)
        pre_test = pre_test_generate(pre_test)
        future_profile = future_profile_generate(future_test)

        knowledge = demo
        knowledge += "\n"
        knowledge += "\n"
        knowledge += love_hate
        knowledge += "\n"
        knowledge += "\n"
        knowledge += bfi
        knowledge += "\n"
        knowledge += pvq
        knowledge += "\n"
        knowledge += "\n"
        knowledge += authenticity
        knowledge += "\n"
        knowledge += "\n"
        knowledge += pre_test
        knowledge += "\n"
        knowledge += "\n"
        knowledge += future_profile
        knowledge += "\n"
        knowledge += "\n"

        st.subheader("Knowledge")
        st.write(knowledge)

    first_letter_to_agent = "**[First Letter to Twenty-Year-Old Self]**" + "\n" + future_test.iloc[0, 13]
    st.subheader("First Letter to Twenty-Year-Old Self")
    st.write(first_letter_to_agent)

    with st.spinner('Wait for generating first letter...'):
        st.write('---------------------------------')
        reply1 = dd_generate_gpt4_basic(first_letter_sys_prompt,knowledge, first_letter_to_agent)
        st.subheader("3년 후 나의 답장 1")
        st.write(reply1)
        st.write('---------------------------------')
        reply2 = dd_generate_gpt4_basic(first_letter_sys_prompt,knowledge,first_letter_to_agent)
        st.subheader("3년 후 나의 답장 2")
        st.write(reply2)
        st.write('---------------------------------')
        reply3 = dd_generate_gpt4_basic(first_letter_sys_prompt,knowledge,first_letter_to_agent)
        st.subheader("3년 후 나의 답장 3")
        st.write(reply3)
        st.write('---------------------------------')