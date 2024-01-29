from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import time,random
from PIL import Image
import streamlit_option_menu as st_menu
# print(st_menu.__version__)

from create_container_web import main
from draw_process import *
from dictionary_process import *
from message_process import process_message
from canvas_process import process_canvas
from word_game_process import process_word_game

#st.balloons()#气球
#小提示
def toast():
    time.sleep(15)
    st.toast("你好~😃")
    time.sleep(2)
    st.toast("找到感兴趣的内容了嘛——",icon="😍")
    time.sleep(5)
    st.toast("没有?",icon="😔")
    time.sleep(1)
    st.toast("先别走！再看看",icon="😜")
    
#我的兴趣推荐
def page_1():
    st.header("我的兴趣推荐",anchor=False,divider="rainbow",sd=1)#大标题

    tab1, tab2, tab3 ,tab4= st.tabs([ "视频📺","音乐🎵", "小工具🛠️","游戏🎮"])#标签切换栏
    with tab1:
        main("vedios.txt",[1,1,1])#执行创建容器代码
    with tab2:
        st.info("""&nbsp;&nbsp;提示  
                初次加载时，音乐播放器可能加载缓慢出现空白，请耐心等待...""", icon="ℹ️")#提升框
        main("musics.txt",[0.55,0.45])#执行创建容器代码
    with tab3:
        main("tools.txt",[0.55,0.45])#执行创建容器代码
    with tab4:
        main("games.txt",[0.55,0.45])#执行创建容器代码
    st.caption(">该栏目持续更新中😉~")
    
    
#我的图片处理工具    
def page_2():
    st.header("图片处理小工具",anchor=False,divider="rainbow")#大标题
    #上传文件
    upload_flag=False#上传成功标记
    img_con1=st.container(border=True)#容器
    with img_con1:
        uploaded_file=st.file_uploader("上传图片以进行图片处理...",type=["png","jpg","jpeg"],on_change=st.cache_resource.clear)#文件上传器
        if uploaded_file:#判断是否上传了图片
            img=Image.open(uploaded_file)#加载图片
            file_name=uploaded_file.name#获取图片名称
            file_type=uploaded_file.type#获取图片类型
            width,height=img.size#获取图片大小
            st.success(f'''图片上传成功!  
                       {file_name}&nbsp;&nbsp;&nbsp;&nbsp;{file_type}文件&nbsp;&nbsp;&nbsp;&nbsp;{width}px*{height}px''', icon="✅")#上传成功提醒
            
            upload_flag=True#上传成功标记
            
    #图片处理
    if upload_flag:#判断是否加载图片
        process_draw(img,file_name)#图片处理



#我的智慧词典    
def page_3():
    st.header("单词查询",anchor=False,divider="rainbow")#大标题
    st.markdown("###### 遇到了不会的英语单词？😨都扔给我吧！👌")
    words_dict,words_history=load_words_dictionary()#读取单词和单词历史文件
    process_dict(words_dict,words_history)#执行单词查询主程序

    st.header("&nbsp;&nbsp;",anchor=False)#占位
    st.header("&nbsp;&nbsp;",anchor=False)#占位
    st.header("🕹️单词记忆挑战",anchor=False,divider="rainbow")#大标题
    st.markdown("🚩**单词记忆大挑战！来试试看~**")
    st.write("游戏规则：:orange[系统将随机在词库中显示一个单词，你需要在特定的时间内记忆]:red[**单词**]:orange[和]:red[**单词的词性及含义**]:orange[，并完成出现的选择题，正常模式下共**10**题。]")
    process_word_game(words_dict,words_history)


                            
#我的留言区 
def page_4():
    st.header("留言区",anchor=False,divider="rainbow")#大标题
    process_message()

def page_5():
    st.header("🖌️魔法画板",anchor=False,divider="rainbow")#大标题
    st.markdown("**这是一个万能的魔法画板，你可以在这里随心所欲的涂鸦并保存你的作品。**:red[（❗在右上角**三点-Settings**中打开**Wide mode**体验更佳哦~）]")

    process_canvas()#画布主函数

                
#添加选项切换卡(https://github.com/victoryhb/streamlit-option-menu)
page_names=["兴趣推荐","图片处理","智慧词典","留言区","魔法画板"]#页面列表
if st.session_state.get('down_switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % len(page_names)#切换下一项
    manual_select = st.session_state['menu_option']#获取当前选项字符
elif st.session_state.get('up_switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) - 1) % len(page_names)#切换下一项
    manual_select = st.session_state['menu_option']#获取当前选项字符
else:
    manual_select = None

with st.sidebar:
    page= st_menu.option_menu("Little_white's 小屋",page_names, icons=['stars', 'images',"journal-bookmark-fill","chat-left-dots-fill","easel2-fill"],
                           menu_icon="globe", default_index=0,manual_select=manual_select,
                            styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin":"10px", "--hover-color": "#eee"}})#菜单界面
st.markdown(
        "##### 你好，陌生人😀，欢迎来到我的个人小站，不论你是:red[**游戏大神**]、:orange[**编程大神**]，还是:blue[**网页搭建大佬**]，又或是:green[**计算机学家**]，还是什么都不知道的:gray[*小白*]，都欢迎浏览和访问:rainbow[Litte_white]'s个人网站~😻"
    )#标题语    

if page=="兴趣推荐":
    st.session_state['menu_option']=0
    page_1()
elif page=="图片处理":
    st.session_state['menu_option']=1
    page_2()
elif page=="智慧词典":
    st.session_state['menu_option']=2
    page_3()
elif page=="留言区":
    st.session_state['menu_option']=3
    page_4()
elif page=="魔法画板":
    st.session_state['menu_option']=4
    page_5()


    
st.header("&nbsp;&nbsp;",anchor=False)#占位
st.write("----")
switch_bt_col1,switch_bt_space,switch_bt_col2=st.columns([0.35,0.79,0.35])#两个切换页面按钮,中间有间隔
with switch_bt_col1:
    st.button(f"上一项：{page_names[(st.session_state.get('menu_option', 0) - 1) % len(page_names)]}", key='up_switch_button')#按钮
with switch_bt_col2:
    st.button(f"下一项：{page_names[(st.session_state.get('menu_option', 0) + 1) % len(page_names)]}", key='down_switch_button')#按钮

# toast()
#待添加:图片处理reset按钮,图片处理剪切旋转(https://github.com/andfanilo/streamlit-drawable-canvas),单词游戏根据难度筛选单词长度,