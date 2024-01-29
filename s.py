if not st.session_state.game_start:
    难度选择
    is_start=st.button("开始游戏",type="primary")
else:
    判断正误
    if st.button("继续游戏",type="primary"):
        is_start=True
    if st.button("退出游戏",type="primary"):
        is_exit=True
if is_start:
    if not st.session_state.game_start:
        st.session_state.game_start=True
    if stop_flag:
        计时\答题
    else:
        is_exit=True
elif is_exit:
    结算
    st.session_state.game_start=False