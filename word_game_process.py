import streamlit as st
import time,random


def process_word_game(words_dict,words_history):
    #变量初始化
    is_start=False
    is_exit=False
    show_answer_empty=None
    if "game_start" not in st.session_state:
        st.session_state.game_start=False
    if "user_answered_word" not in st.session_state:
        st.session_state.user_answered_word="1"
    if "user_answered_meaning" not in st.session_state:
        st.session_state.user_answered_meaning="1"
    if "infinity_checkbox" not in st.session_state:
        st.session_state["infinity_checkbox"]=False
    if "rem_time" not in st.session_state:
        st.session_state["rem_time"]=0
    
    if not st.session_state.game_start:#判断游戏是否开始
        option_empty=st.empty()
        with option_empty:
            #游戏参数选择
            choose_dif_con=st.container(border=True)
            with choose_dif_con:
                st.write("**难度选择：**")
                difficult=st.radio(
                    ' ',
                    [':green[简单]', ':blue[普通]', ':red[困难]',":gray[自定义]"],
                    captions=['记忆时间7s', '记忆时间3s', '记忆时间1.5s'],index=1
                    ,horizontal=True,label_visibility="collapsed"
                )#选择难度框
                #获取记忆时间
                if difficult==":gray[自定义]":
                    custom_time_col,custom_round_col,infinity_col=st.columns([0.4,0.4,0.2])
                    with custom_time_col:
                        st.session_state.rem_time=st.number_input("自定义记忆时间:",placeholder="输入自定义的记忆时间..",min_value=1.0,max_value=20.0,step=0.5,value=None,)#自定义记忆时间,数字输入框
                    with custom_round_col:
                        if not st.session_state["infinity_checkbox"]:
                            st.session_state.rem_round=st.number_input("自定义题数:",placeholder="输入自定义的题数..",min_value=1,max_value=100,step=1,value=None,help="自定义题数，题目轮次结束后将进入结算")#自定义轮次,数字输入框
                        else:
                            st.session_state.rem_round=st.number_input("自定义题数:",placeholder="无尽模式下无法设置题数...",min_value=1,max_value=100,step=1,value=None,disabled=True,help="自定义题数，题目轮次结束后将进入结算")#自定义轮次,数字输入框
                    with infinity_col:
                        st.session_state.infinity_mod=st.checkbox("无尽模式",help="题数无限，可随时结束游戏",key="infinity_checkbox")
                else:
                    if difficult==":green[简单]":
                        st.session_state.rem_time=7
                    elif difficult=="blue[普通]":
                        st.session_state.rem_time=3
                    elif difficult==":red[困难]":
                        st.session_state.rem_time=1.5
                    st.session_state.rem_round=10
                    st.session_state.infinity_mod=False
                rem_time=st.session_state.rem_time
                
                begin_space,begin_col=st.columns([0.85,0.15])
                with begin_col:
                    begin_btn_push=st.button("开始游戏",type="primary")
                if begin_btn_push:
                    if (st.session_state.rem_time and st.session_state.rem_round and not st.session_state.infinity_mod) or (st.session_state.rem_time and st.session_state.infinity_mod):#判断自定义模式非无尽模式是否填写了时间和题数,或是无尽模式是否填写了时间
                        is_start=True
                        is_exit=False
                        st.session_state.correct=0#正确数
                        st.session_state.wrong=0#错误数
                        st.session_state.now_question=0#当前题
                    else:
                        st.warning("""⚠️**注意**  
                                   好像没有填写完整记忆时间和题数哦~""")
    else:
        is_start=False
        show_answer_empty=st.empty()
        with show_answer_empty:
            with st.container(border=True):
                st.write(f"**第{str(st.session_state.now_question)}题：**")
                if st.session_state.user_answered_word==None:
                    st.session_state.user_answered_word="_*未填写答案_"
                if st.session_state.user_answered_meaning==None:
                    st.session_state.user_answered_meaning="_*未填写答案_"
                if st.session_state.user_answered_word==st.session_state.answer_word and st.session_state.user_answered_meaning==words_dict[st.session_state.answer_word][1]:#判断是否回答正确
                    st.write("✔️:green[回答正确!]")
                    st.write(f"##### **{st.session_state.answer_word}&nbsp;&nbsp;{words_dict[st.session_state.answer_word][1]}**")
                    st.session_state.correct+=1
                    if st.session_state.correct+st.session_state.wrong>st.session_state.now_question:#如果对题和错题加起来超过了总题数
                        st.session_state.correct=st.session_state.now_question-st.session_state.wrong#将对题设置为总题数-错题
                else:
                    st.write("❌:red[回答错误!]")
                    st.session_state.wrong+=1
                    st.write(f"刚刚的单词是：**{st.session_state.answer_word}&nbsp;&nbsp;{words_dict[st.session_state.answer_word][1]}**")
                    st.write(f"你回答的是：:red[{st.session_state.user_answered_word}&nbsp;&nbsp;{st.session_state.user_answered_meaning}]")
                    if st.session_state.correct+st.session_state.wrong>st.session_state.now_question:#如果对题和错题加起来超过了总题数
                        st.session_state.wrong=st.session_state.now_question-st.session_state.correct#将错题设置为总题数-对题
                if st.session_state.question_count!="infinity" and st.session_state.now_question==st.session_state.question_count:#在不是无尽模式的情况下如果是最后一题
                    end_space,end_col=st.columns([0.85,0.15])
                    with end_col:
                            if st.button("结束游戏",type="primary"):
                                is_exit=True
                                is_start=False
                                show_answer_empty.empty()
                else:
                    continue_space,continue_col,exit_col=st.columns([0.7,0.15,0.15])
                    with continue_col:#继续按钮
                        if st.button("继续游戏"):
                            is_start=True
                    with exit_col:
                        if st.button("退出游戏",type="primary"):
                            is_exit=True
                            is_start=False         
                
    #游戏开始
    if is_start:
        if show_answer_empty!=None:#如果显示答案部件不为空
            show_answer_empty.empty()#清空显示答案
        rem_time=st.session_state.rem_time#设置记忆时间
        if not st.session_state.game_start:#如果开始标记为false
            st.session_state.game_start=True#设置开始标记为true
            option_empty.empty()#清除选项显示部件
        st.session_state.now_question+=1#题数+1
        game_con=st.container(border=True)
        with game_con:
            #出题
            if st.session_state.infinity_mod:#判断是否是无尽模式
                st.session_state.question_count="infinity"#设置题数为无限
                stop_flag=(True)#下方循环的执行条件
            else:
                st.session_state.question_count=st.session_state.rem_round#设置题数
                stop_flag=(st.session_state.now_question<=st.session_state.question_count)#循环执行条件为当前题数小于等于总题数
            if stop_flag:
                question_show_empty=st.empty()
                with question_show_empty:
                    question_show_con=st.container()
                    with question_show_con:
                        st.write(f"**第{str(st.session_state.now_question)}题：**")
        
                        st.session_state.answer_word=random.choice(list(words_dict.keys()))
                        st.write(f"#### {st.session_state.answer_word}&nbsp;&nbsp;{words_dict[st.session_state.answer_word][1]}")#显示题目文本
                        time_bar=st.progress(100,text=f"剩余时间：**{rem_time}s**")#创建计时进度条
                        for i in range(100,-1,-1):
                            time_bar.progress(i,text=f"剩余时间：**{round(rem_time*(i/100),2)}s**")#进度条值-1%
                            time.sleep(rem_time/100)#等待记忆秒数的1%
                        time.sleep(0.28)
                question_show_empty.empty()#清空题目和进度条

                # question_empty=st.empty()
                # with question_empty:
                qestion_con=st.container()
                with qestion_con:
                    letters="qwertyuiopasdfghjklzxcvbnm"
                    wrong1=st.session_state.answer_word.replace(st.session_state.answer_word[random.randint(0,len(st.session_state.answer_word)-1)],"",1)#错误选项1,随机删除一个字母
                    wrong2=st.session_state.answer_word
                    while wrong2==st.session_state.answer_word:
                        wrong2=st.session_state.answer_word.replace(st.session_state.answer_word[random.randint(0,len(st.session_state.answer_word)-1)],random.choice(st.session_state.answer_word),1)#错误选项2,随机替换1个字母为本单词中的某个字母,保证不与原单词相同
                    wrong3=st.session_state.answer_word
                    while wrong3==st.session_state.answer_word:
                        wrong3=st.session_state.answer_word.replace(st.session_state.answer_word[random.randint(0,len(st.session_state.answer_word)-1)],random.choice(letters),1)#错误选项3,随机替换1个字母为任意字母,保证不与原单词相同
                    word_answers=[st.session_state.answer_word,wrong1,wrong2,wrong3]#单词的错误选项
                    random.shuffle(word_answers)#打乱答案
                    
                    wrong4,wrong5,wrong6=random.choice(list(words_dict.values())),random.choice(list(words_dict.values())),random.choice(list(words_dict.values()))  #单词意思的错误选项,在单词列表的其他单词的意思中随机挑选三个
                    meaning_answers=[words_dict[st.session_state.answer_word][1],wrong4[1],wrong5[1],wrong6[1]]#意思的错误选项
                    random.shuffle(meaning_answers)#打乱答案
                    
                    with st.form("question",border=False):
                        st.write(f"**第{str(st.session_state.now_question)}题：**")
                        st.write("刚刚出现的单词是...")
                        st.session_state.user_answered_word=st.radio(' ',[f'{word_answers[0]}', f'{word_answers[1]}', f'{word_answers[2]}',f"{word_answers[3]}"],index=None,key="word_radio",horizontal=True,label_visibility="collapsed")    #单词选择框
                        st.write("下列哪一项是该单词正确的意思?")
                        st.session_state.user_answered_meaning=st.radio(' ',[meaning_answers[0],meaning_answers[1],meaning_answers[2],meaning_answers[3]],index=None,key="mean_radio",horizontal=True,label_visibility="collapsed") #意思选择框   
                        # if st.session_state.user_answered_meaning and st.session_state.user_answered_word:
                        submit_space,submit_col=st.columns([0.9,0.1])
                        with submit_col:
                            st.form_submit_button("提交",on_click=submit_btn_clicked)#,on_click=submit_btn_clicked,args=(user_answered_word,user_answered_meaning)
                        
                            # else:
                        #     submitted = st.form_submit_button("提交",disabled=True)
                        #     st.caption("*好像还没有选完答案哦~*")    
            else:
                is_exit=True
    elif is_exit:
        show_answer_empty.empty()#清空显示答案
        with st.container(border=True):
            st.write(":red[**游戏结束!**]")
            acc=round(st.session_state.correct/st.session_state.now_question*100,1)
            st.write(f"本轮游戏记忆了**{str(st.session_state.now_question)}**个单词，回答正确:green[**{str(st.session_state.correct)}**]道，错误:red[**{str(st.session_state.wrong)}**]道，正确率:blue[{str(acc)}%]，再接再厉！🎉")
            continue_space,sure_col=st.columns([0.9,0.1])
            with sure_col:
                st.button("确定",type="primary",on_click=reset_game)

#重置游戏重要变量
def reset_game():
    st.session_state.game_start=False
    is_exit=False
    st.session_state.correct=0#正确数
    st.session_state.wrong=0#错误数
    st.session_state.now_question=0#当前题数
#     st.session_state.user_answered_word , st.session_state.user_answered_meaning = user_answered_word , user_answered_meaning
#     st.write(st.session_state.user_answered_word,st.session_state.user_answered_meaning)

#提交按钮点击
def submit_btn_clicked():
    st.session_state.user_answered_word=st.session_state["word_radio"]
    st.session_state.user_answered_meaning=st.session_state["mean_radio"]