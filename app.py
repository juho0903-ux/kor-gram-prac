import streamlit as st

st.set_page_config(
    page_title="중1 국어 문법 미션",
    page_icon="📝",
    layout="centered"
)

SENTENCE = "먹구름이 가득 낀 하늘은 늘 철수가 공포에 잡아먹히게 하였다."

# -----------------------------
# 정답 데이터
# -----------------------------
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

SELF_MORPHEMES = {"구름", "가득", "하늘", "늘", "철수", "공포"}
DEPENDENT_MORPHEMES = {
    "먹-(먹구름)", "이", "끼-", "-ㄴ", "은", "가", "에",
    "잡-", "-아", "먹-(잡아먹히다)", "-히-", "-게", "하-", "-였-", "-다"
}
LEXICAL_MORPHEMES = {
    "구름", "가득", "끼-", "하늘", "늘", "철수", "공포",
    "잡-", "먹-(잡아먹히다)", "하-"
}
GRAMMATICAL_MORPHEMES = {
    "먹-(먹구름)", "이", "-ㄴ", "은", "가", "에",
    "-아", "-히-", "-게", "-였-", "-다"
}

ALL_MORPHEMES = [
    "먹-(먹구름)", "구름", "이", "가득", "끼-", "-ㄴ", "하늘", "은",
    "늘", "철수", "가", "공포", "에", "잡-", "-아",
    "먹-(잡아먹히다)", "-히-", "-게", "하-", "-였-", "-다"
]

POS_OPTIONS = ["선택", "명사", "대명사", "수사", "동사", "형용사", "관형사", "부사", "조사", "감탄사"]

# -----------------------------
# 유틸
# -----------------------------
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

def same_morphemes(user_text, answer_list):
    return normalize_morpheme_text(user_text) == answer_list

def init_state():
    defaults = {
        "q1_submitted": False,
        "q2_submitted": False,
        "q3a_submitted": False,
        "q3b_submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

init_state()

# -----------------------------
# 스타일
# -----------------------------
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
.small-note {font-size: 0.92rem; color: #666;}
</style>
""", unsafe_allow_html=True)

st.title("📝 중1 국어 문법 미션")
st.caption("한 문장을 단계별로 분석하며 파생어·품사·형태소를 연습합니다.")

st.markdown('<div class="sentence-box"><b>문장</b><br>' + SENTENCE + '</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["1️⃣ 파생어 분석", "2️⃣ 모든 단어의 품사", "3️⃣ 형태소 분류"])

# -----------------------------
# 1번
# -----------------------------
with tab1:
    st.subheader("1. 파생어를 찾아 분석해 보세요.")
    st.markdown("""
    <div class="condition-box">
    ✅ 문장에서 파생어를 모두 찾기<br>
    ✅ 각 파생어를 형태소 단위로 분석하기<br>
    ✅ 각 파생어의 품사 쓰기
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        word1 = st.text_input("파생어 1", key="q1_word1")
        morph1 = st.text_input("형태소 분석 1", placeholder="예: 먹- / 구름", key="q1_morph1")
        pos1 = st.selectbox("품사 1", POS_OPTIONS, key="q1_pos1")
    with c2:
        word2 = st.text_input("파생어 2", key="q1_word2")
        morph2 = st.text_input("형태소 분석 2", placeholder="예: 잡- / -아 / 먹- / -히- / -게", key="q1_morph2")
        pos2 = st.selectbox("품사 2", POS_OPTIONS, key="q1_pos2")

    if st.button("1번 제출", type="primary", key="q1_submit"):
        st.session_state.q1_submitted = True

    if st.session_state.q1_submitted:
        user_entries = [
            (word1.strip(), morph1, pos1),
            (word2.strip(), morph2, pos2),
        ]
        correct_count = 0
        seen = set()

        for idx, (word, morph, pos) in enumerate(user_entries, start=1):
            if word in Q1_ANSWERS and word not in seen:
                ans = Q1_ANSWERS[word]
                word_ok = True
                morph_ok = same_morphemes(morph, ans["morphemes"])
                pos_ok = pos == ans["pos"]
                seen.add(word)

                if word_ok and morph_ok and pos_ok:
                    st.success(f"{idx}번째 답: 정확합니다.")
                    correct_count += 1
                else:
                    if not morph_ok:
                        st.warning(f"{idx}번째 답: 파생어는 맞지만 형태소 분석을 다시 확인해 보세요.")
                    if not pos_ok:
                        st.warning(f"{idx}번째 답: 파생어는 맞지만 품사를 다시 확인해 보세요.")
            else:
                st.error(f"{idx}번째 답: 파생어 선택을 다시 확인해 보세요.")

        if correct_count == 2:
            st.balloons()
            st.success("두 파생어를 모두 정확하게 분석했습니다!")
        else:
            with st.expander("힌트 보기"):
                st.write("접사가 붙어 만들어진 단어를 찾아보세요. 한 단어는 접두사가, 다른 한 단어는 접미사가 관여합니다.")

# -----------------------------
# 2번
# -----------------------------
with tab2:
    st.subheader("2. 문장에 쓰인 모든 단어의 품사를 써 보세요.")
    st.caption("조사는 세부 종류가 아니라 '조사'라고 쓰도록 했습니다.")

    cols = st.columns(2)
    q2_user = {}
    words = list(Q2_ANSWERS.keys())
    for i, word in enumerate(words):
        with cols[i % 2]:
            q2_user[word] = st.selectbox(
                f"{word}",
                POS_OPTIONS,
                key=f"q2_{i}"
            )

    if st.button("2번 제출", type="primary", key="q2_submit"):
        st.session_state.q2_submitted = True

    if st.session_state.q2_submitted:
        wrong = []
        for word, answer in Q2_ANSWERS.items():
            if q2_user[word] != answer:
                wrong.append(word)

        if not wrong:
            st.success("모든 단어의 품사를 정확하게 분류했습니다!")
        else:
            st.warning(f"다시 확인할 단어: {', '.join(wrong)}")
            st.info("틀린 단어만 다시 고쳐서 제출해 보세요.")

# -----------------------------
# 3번
# -----------------------------
with tab3:
    st.subheader("3. 형태소를 종류별로 분류해 보세요.")
    st.caption("같은 '먹-'이라도 쓰인 위치와 기능이 달라서 구별해 표시했습니다.")

    st.markdown("#### 3-1. 자립 형태소 / 의존 형태소")
    st.write("각 형태소가 어느 쪽에 해당하는지 선택하세요.")

    q3a_user = {}
    for i, m in enumerate(ALL_MORPHEMES):
        q3a_user[m] = st.radio(
            m,
            ["선택", "자립 형태소", "의존 형태소"],
            horizontal=True,
            key=f"q3a_{i}"
        )

    if st.button("3-1 제출", type="primary", key="q3a_submit"):
        st.session_state.q3a_submitted = True

    if st.session_state.q3a_submitted:
        wrong = []
        for m, choice in q3a_user.items():
            answer = "자립 형태소" if m in SELF_MORPHEMES else "의존 형태소"
            if choice != answer:
                wrong.append(m)

        if not wrong:
            st.success("자립 형태소와 의존 형태소를 모두 정확하게 분류했습니다!")
        else:
            st.warning(f"다시 확인할 형태소: {', '.join(wrong)}")

    st.divider()
    st.markdown("#### 3-2. 실질 형태소 / 형식 형태소")
    st.write("이번에는 같은 형태소들을 의미와 문법적 기능을 기준으로 분류하세요.")

    q3b_user = {}
    for i, m in enumerate(ALL_MORPHEMES):
        q3b_user[m] = st.radio(
            m,
            ["선택", "실질 형태소", "형식 형태소"],
            horizontal=True,
            key=f"q3b_{i}"
        )

    if st.button("3-2 제출", type="primary", key="q3b_submit"):
        st.session_state.q3b_submitted = True

    if st.session_state.q3b_submitted:
        wrong = []
        for m, choice in q3b_user.items():
            answer = "실질 형태소" if m in LEXICAL_MORPHEMES else "형식 형태소"
            if choice != answer:
                wrong.append(m)

        if not wrong:
            st.success("실질 형태소와 형식 형태소를 모두 정확하게 분류했습니다!")
        else:
            st.warning(f"다시 확인할 형태소: {', '.join(wrong)}")

st.divider()
left, right = st.columns([4, 1])
with left:
    st.caption("틀린 항목을 다시 수정한 뒤 재제출할 수 있습니다.")
with right:
    if st.button("처음부터 다시 풀기"):
        reset_all()
