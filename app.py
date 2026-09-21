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
