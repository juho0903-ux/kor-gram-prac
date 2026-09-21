import streamlit as st
import re
from collections import Counter

st.set_page_config(
    page_title="퇴계원중 1학년 중간고사 대비 문항 연습",
    page_icon="📝",
    layout="centered"
)

SENTENCE = "먹구름이 가득 낀 하늘은 늘 철수가 공포에 잡아먹히게 하였다."

Q1_ANSWERS = {
    "먹구름": {
        "morphemes": ["먹-", "구름"],
        "pos": "명사",
    },
    "잡아먹히게": {
        "morphemes": ["잡-", "-아", "먹-", "-히-", "-게"],
        "pos": "동사",
    },
}

Q2_ANSWERS = {
    "먹구름": "명사",
    "이": "조사",
    "가득": "부사",
    "낀": "동사",
    "하늘": "명사",
    "은": "조사",
    "늘": "부사",
    "철수": "명사",
    "가": "조사",
    "공포": "명사",
    "에": "조사",
    "잡아먹히게": "동사",
    "하였다": "동사",
}

Q3_ANSWERS = {
    "자립 형태소": ["구름", "가득", "하늘", "늘", "철수", "공포"],
    "의존 형태소": [
        "먹-", "이", "끼-", "-ㄴ", "은", "가", "에",
        "잡-", "-아", "먹-", "-히-", "-게", "하-", "-였-", "-다"
    ],
    "실질 형태소": [
        "구름", "가득", "끼-", "하늘", "늘", "철수", "공포",
        "잡-", "먹-", "하-"
    ],
    "형식 형태소": [
        "먹-", "이", "-ㄴ", "은", "가", "에",
        "-아", "-히-", "-게", "-였-", "-다"
    ],
}

POS_OPTIONS_TEXT = "명사, 대명사, 수사, 동사, 형용사, 관형사, 부사, 조사, 감탄사"

def normalize_morpheme_text(text: str):
    if not text:
        return []
    cleaned = (
        text.replace("/", " ")
        .replace(",", " ")
        .replace("·", " ")
        .replace("|", " ")
    )
    return [x.strip() for x in cleaned.split() if x.strip()]

def split_short_answers(text: str):
    if not text:
        return []
    parts = re.split(r"[,/·|\n]+", text)
    return [p.strip() for p in parts if p.strip()]

def same_morphemes_in_order(user_text, answer_list):
    return normalize_morpheme_text(user_text) == answer_list

def same_items_ignore_order(user_text, answer_list):
    return Counter(split_short_answers(user_text)) == Counter(answer_list)

def init_state():
    defaults = {
        "q1_submitted": False,
        "q2_submitted": False,
        "q3_submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

init_state()
