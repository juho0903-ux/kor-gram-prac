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

st.markdown("""
<style>
.block-container {max-width: 900px; padding-top: 2rem;}
.sentence-box {
    background: #eef6ff;
    border: 1px solid #b8d8ff;
    border-radius: 12px;
    padding: 16px 18px;
    font-size: 1.08rem;
    margin: 8px 0 18px 0;
}
.condition-box {
    background: #f6f6f6;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("📝 퇴계원중 1학년 중간고사 대비 문항 연습")
st.caption("중간고사에 필요한 국어 문법 개념을 문항별로 연습합니다.")

st.markdown(
    '<div class="sentence-box"><b>문장</b><br>' + SENTENCE + '</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["1️⃣ 문항 1", "2️⃣ 문항 2", "3️⃣ 문항 3"])

with tab1:
    st.subheader("1. 파생어를 찾아 분석해 보세요.")
    st.markdown("""
    <div class="condition-box">
    ✅ 문장에서 파생어를 모두 찾기<br>
    ✅ 각 파생어를 형태소 단위로 분석하기<br>
    ✅ 형태소 분석 시 접사·어간·어미의 붙임표를 정확하게 표시하기<br>
    ✅ 각 파생어의 품사 쓰기
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        word1 = st.text_input("파생어 1", key="q1_word1")
        morph1 = st.text_input("형태소 분석 1", key="q1_morph1")
        pos1 = st.text_input("품사 1", placeholder="예: 명사", key="q1_pos1")
    with c2:
        word2 = st.text_input("파생어 2", key="q1_word2")
        morph2 = st.text_input("형태소 분석 2", key="q1_morph2")
        pos2 = st.text_input("품사 2", placeholder="예: 동사", key="q1_pos2")

    if st.button("1번 제출", type="primary", key="q1_submit"):
        st.session_state.q1_submitted = True

    if st.session_state.q1_submitted:
        user_entries = [
            (word1.strip(), morph1, pos1.strip()),
            (word2.strip(), morph2, pos2.strip()),
        ]
        correct_count = 0
        seen = set()

        for idx, (word, morph, pos) in enumerate(user_entries, start=1):
            if word in Q1_ANSWERS and word not in seen:
                ans = Q1_ANSWERS[word]
                morph_ok = same_morphemes_in_order(morph, ans["morphemes"])
                pos_ok = pos == ans["pos"]
                seen.add(word)

                if morph_ok and pos_ok:
                    st.success(f"{idx}번째 답: 정확합니다.")
                    correct_count += 1
                else:
                    if not morph_ok:
                        st.warning(f"{idx}번째 답: 형태소 분석을 다시 확인해 보세요. 붙임표까지 정확히 써야 합니다.")
                    if not pos_ok:
                        st.warning(f"{idx}번째 답: 품사를 다시 확인해 보세요.")
            else:
                st.error(f"{idx}번째 답: 파생어 선택을 다시 확인해 보세요.")

        if correct_count == 2:
            st.success("두 파생어를 모두 정확하게 분석했습니다!")
        else:
            with st.expander("힌트 보기"):
                st.write("접사가 붙어 만들어진 단어를 찾아보세요.")

with tab2:
    st.subheader("2. 문장에 쓰인 모든 단어의 품사를 써 보세요.")
    st.caption(f"가능한 품사: {POS_OPTIONS_TEXT}")
    st.info("각 칸에 품사 이름만 직접 입력하세요. 예: 명사, 조사, 동사")

    q2_user = {}
    words = list(Q2_ANSWERS.keys())
    cols = st.columns(2)

    for i, word in enumerate(words):
        with cols[i % 2]:
            q2_user[word] = st.text_input(
                word,
                placeholder="품사 입력",
                key=f"q2_{i}"
            ).strip()

    if st.button("2번 제출", type="primary", key="q2_submit"):
        st.session_state.q2_submitted = True

    if st.session_state.q2_submitted:
        wrong = []
        blank = []

        for word, answer in Q2_ANSWERS.items():
            user_answer = q2_user[word]
            if not user_answer:
                blank.append(word)
            elif user_answer != answer:
                wrong.append(word)

        if not wrong and not blank:
            st.success("모든 단어의 품사를 정확하게 썼습니다!")
        else:
            if blank:
                st.warning(f"아직 쓰지 않은 단어: {', '.join(blank)}")
            if wrong:
                st.warning(f"다시 확인할 단어: {', '.join(wrong)}")
            st.info("정답은 바로 보여주지 않습니다. 해당 단어만 고쳐서 다시 제출해 보세요.")

with tab3:
    st.subheader("3. 형태소를 종류별로 분류해 보세요.")
    st.markdown("""
    <div class="condition-box">
    ✅ 네 칸에 해당 형태소를 직접 쓰세요.<br>
    ✅ 형태소 사이는 <b>쉼표(,)</b>로 구분하세요.<br>
    ✅ 접사·어간·어미의 <b>붙임표 위치까지 정확하게</b> 써야 정답으로 인정합니다.<br>
    ✅ 형태소의 순서는 달라도 됩니다.
    </div>
    """, unsafe_allow_html=True)

    self_text = st.text_area(
        "자립 형태소",
        placeholder="예: 구름, 가득, ...",
        height=90,
        key="q3_self"
    )
    dependent_text = st.text_area(
        "의존 형태소",
        placeholder="예: 먹-, 이, ...",
        height=110,
        key="q3_dependent"
    )
    lexical_text = st.text_area(
        "실질 형태소",
        placeholder="예: 구름, 가득, ...",
        height=100,
        key="q3_lexical"
    )
    grammatical_text = st.text_area(
        "형식 형태소",
        placeholder="예: 먹-, 이, ...",
        height=100,
        key="q3_grammatical"
    )

    if st.button("3번 제출", type="primary", key="q3_submit"):
        st.session_state.q3_submitted = True

    if st.session_state.q3_submitted:
        user_map = {
            "자립 형태소": self_text,
            "의존 형태소": dependent_text,
            "실질 형태소": lexical_text,
            "형식 형태소": grammatical_text,
        }

        wrong_categories = []
        for category, user_text in user_map.items():
            if same_items_ignore_order(user_text, Q3_ANSWERS[category]):
                st.success(f"{category}: 정확합니다.")
            else:
                wrong_categories.append(category)
                st.warning(
                    f"{category}: 다시 확인해 보세요. 형태소의 누락·중복 또는 붙임표 위치가 틀릴 수 있습니다."
                )

        if not wrong_categories:
            st.success("네 종류의 형태소를 모두 정확하게 분류했습니다!")
        else:
            st.info("틀린 칸만 수정해서 다시 제출할 수 있습니다.")

st.divider()
left, right = st.columns([4, 1])
with left:
    st.caption("틀린 항목을 수정한 뒤 다시 제출할 수 있습니다.")
with right:
    if st.button("처음부터 다시 풀기"):
        reset_all()
