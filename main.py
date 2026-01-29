import streamlit as st
import json 
from datetime import datetime
from zoneinfo import ZoneInfo
import time

TEHRAN_TZ = ZoneInfo("Asia/Tehran")

def tehran_now():
    return datetime.now(TEHRAN_TZ)

st.set_page_config(page_title="Alice & Bob", initial_sidebar_state="expanded")

st.markdown("""<style> body {direction: rtl; text-align: right;}</style>""", unsafe_allow_html=True)
# st.markdown("""<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True) 

if "api_key" not in st.session_state:
    st.session_state['api_key'] = None

if "role" not in st.session_state:
    st.session_state['role'] = None

if not st.session_state.api_key:
    api_key_input = st.text_input(label="2312", value=st.session_state.api_key, type="password", placeholder="api key", label_visibility="hidden")
    if st.button("Login", use_container_width=True):
        if st.secrets["ALICE"] == api_key_input:
            st.session_state.role = "alice"
            st.session_state.api_key = api_key_input
        elif st.secrets["BOB"] == api_key_input:
            st.session_state.role = "bob"
            st.session_state.api_key = api_key_input
        else:
            st.error("Wrong Credentials.")
        st.rerun()

if st.session_state.api_key: 
    if "messages" not in st.session_state:
        with open('db.json', "r") as file:
            st.session_state['messages'] = json.load(file)
    for message in st.session_state['messages']:
        seen_status = "☑️"
        if "seen" in message.keys():
            if message["seen"]:
                seen_status = "✅️"
                                                                                    
        if message["role"] == 'bob':
            if st.session_state.role == "alice":
                message["seen"] = True
            with st.chat_message("ai", avatar="🧔🏼‍♂️"):
                st.markdown(f"*{message['time']}*\t{seen_status}\n\n**{message['content'].strip()}**")
        elif message["role"] == 'alice':
            if st.session_state.role == "bob":
                message["seen"] = True
            with st.chat_message("human", avatar="✨"):
                st.markdown(f"*{message['time']}*\t{seen_status}\n\n**{message['content'].strip()}**")
        with open('db.json', "w") as file:
            json.dump(st.session_state['messages'][-50:], file)

    if prompt := st.chat_input(""):
        st.session_state['messages'].append({"role": st.session_state.role, "content": prompt, "time": tehran_now().isoformat(sep="|", timespec="minutes")[:16], "seen": False})
        with open('db.json', "w") as file:
            json.dump(st.session_state['messages'][-50:], file)
        st.rerun()

if st.session_state.api_key:
    while True:
        time.sleep(3)
        with open('db.json', "r") as file:
            a = json.load(file)
        if len(a) != len(st.session_state['messages']):
            st.session_state['messages'] = a
            st.rerun()
        if a[-1]["seen"] != st.session_state['messages'][-1]["seen"]:
            st.session_state['messages'] = a
            st.rerun()
