"""
DME - Dumbest Messenger Ever

This code prefers simplicity over cleverness.
If something looks naive, it probably is — on purpose.
"""

import os
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from dotenv import load_dotenv

load_dotenv() 
ALICE_KEY = os.getenv("ALICE_KEY", "alice-default")
BOB_KEY = os.getenv("BOB_KEY", "bob-default")
ALICE_AVATAR = os.getenv("ALICE_AVATAR", "✨")
BOB_AVATAR = os.getenv("BOB_AVATAR", "🧔🏼‍♂️")
DB_FILE = os.getenv("DB_FILE", "db.json")
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 3))
MESSAGE_HISTORY_LIMIT = int(os.getenv("MESSAGE_HISTORY_LIMIT", 50))
TIMEZONE = os.getenv("TIMEZONE", "Asia/Tehran")
IS_RTL = bool(os.getenv("IS_RTL", "False"))

TEHRAN_TZ = ZoneInfo(TIMEZONE)
def time_now():
    return datetime.now(TEHRAN_TZ)

if IS_RTL:
    st.set_page_config(page_title="DME - Dumbest Messenger Ever", initial_sidebar_state="expanded")

if "api_key" not in st.session_state:
    st.session_state['api_key'] = None

if "role" not in st.session_state:
    st.session_state['role'] = None

if not st.session_state.api_key:
    api_key_input = st.text_input(label="2312", value=st.session_state.api_key, type="password", placeholder="api key", label_visibility="hidden")
    st.write(ALICE_KEY)
    if st.button("Login", use_container_width=True):
        st.write(api_key_input)
        if ALICE_KEY == api_key_input:
            st.session_state.role = "alice"
            st.session_state.api_key = api_key_input
        elif BOB_KEY == api_key_input:
            st.session_state.role = "bob"
            st.session_state.api_key = api_key_input
        else:
            st.error("Wrong Credentials.")
        st.rerun()

if st.session_state.api_key:
    if "messages" not in st.session_state:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as file:
                st.session_state['messages'] = json.load(file)
        else:
            st.session_state['messages'] = []

    for message in st.session_state['messages']:
        seen_status = "☑️"
        if message.get("seen"):
            seen_status = "✅️"
        if message["role"] == 'bob':
            if st.session_state.role == "alice":
                message["seen"] = True
            with st.chat_message("ai", avatar=BOB_AVATAR):
                st.markdown(f"*{message['time']}*\t{seen_status}\n\n**{message['content'].strip()}**")
        elif message["role"] == 'alice':
            if st.session_state.role == "bob":
                message["seen"] = True
            with st.chat_message("human", avatar=ALICE_AVATAR):
                st.markdown(f"*{message['time']}*\t{seen_status}\n\n**{message['content'].strip()}**")
    with open(DB_FILE, "w") as file:
        json.dump(st.session_state['messages'][-MESSAGE_HISTORY_LIMIT:], file)

    if prompt := st.chat_input(""):
        st.session_state['messages'].append({"role": st.session_state.role, "content": prompt, "time": time_now().isoformat(sep="|", timespec="minutes")[:16], "seen": False})
        with open(DB_FILE, "w") as file:
            json.dump(st.session_state['messages'][-MESSAGE_HISTORY_LIMIT:], file)
        st.rerun()

    while True:
        time.sleep(REFRESH_INTERVAL)
        with open(DB_FILE, "r") as file:
            a = json.load(file)
        if len(a) != len(st.session_state['messages']) or (a and st.session_state['messages'] and a[-1].get("seen") != st.session_state['messages'][-1].get("seen")):
            st.session_state['messages'] = a
            st.rerun()
