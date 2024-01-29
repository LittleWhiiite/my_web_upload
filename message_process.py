import streamlit as st
import time,os

def process_message():
    message_list=[]
    
    #读取文件
    try:#判断是否有留言文本文件
        with open("messages.txt",'r',encoding="utf-8")as mes:
            message_list=mes.read().split("\n")#读取留言文本字典
            if message_list[-1]=="":
                message_list.pop()#删除最后的空项
            for i in range(len(message_list)):
                message_list[i]=message_list[i].split("#")#以:具体分割每个留言的详细信息
                
    except FileNotFoundError:#如果没有留言文件
        with open("messages.txt",'w',encoding="utf-8")as mes:#创建文件
            mes.write("")

    #显示文本([1]:名字,[2]:头像,[3]:信息内容,[4]:时间)
    mes_con=st.container(border=True)#创建容器框
    no_message=False#是否无留言
    with mes_con:
        for message in message_list:#遍历消息列表
            # st.write(f"**{message[1]}**&nbsp;&nbsp;(:gray[{message[4]}]):")#书写用户名
            with st.chat_message(name=message[1],avatar=message[2]):#创建消息框
                st.write(f"""######  **{message[1]}**&nbsp;&nbsp;(:gray[{message[4]}]):  
                         {message[3]}""")#书写留言信息
        #清空留言区按钮     
        if message_list:
            message_space,message_col=st.columns([0.75,0.25])#并列容器
            with message_col:
                if st.button("清空留言区",type="primary",use_container_width=True):
                    os.remove("messages.txt")    
                    st.rerun()
        else:
            no_message=True
        if no_message:        
            st.caption("暂无人发布消息哦~快去抢沙发吧!")

    #留言交互
    mes_input_con=st.container(border=True)#创建容器框
    with mes_input_con:
        # with st.empty():
        st.write("**留言区:**")
        user_name_text,user_name_col,user_avatar_text,user_avatar_col=st.columns([0.1,0.5,0.09,0.31])#并列容器
        with user_name_text:
            st.write("用户名:")
        with user_name_col:
            user_name=st.text_input(" ",placeholder="输入你的用户名...",label_visibility="collapsed")
        with user_avatar_text:
            st.write("头像:")
        with user_avatar_col:
            user_avatar=st.selectbox(" ",["🧑","🧒","🧓","🧔","🧐","🌖","🌞","🌛","🌤️","🌺","🍋","🍄","🎃","🎅","🎸","☃️","🧛‍♀️"],index=None,placeholder="选择一个头像吧...",label_visibility="collapsed")
        input_message_col,enter_message_col=st.columns([0.9,0.1])#并列容器
        with input_message_col:
            input_message=st.text_input(" ",placeholder="输入你想说的话吧...",label_visibility="collapsed")#留言输入框

        #输入保存
        with enter_message_col:
            enter_message=st.button("留言",type="primary",use_container_width=True)
        if enter_message:
            if user_name and user_avatar and input_message:
                now_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())#获取当前时间
                if message_list:#判断消息列表是否有消息
                    message_list.append([str(int(message_list[-1][0])+1),user_name,user_avatar,input_message,now_time])#将用户名,头像,输入的文本添加到消息列表的最后
                else:
                    message_list.append([str(1),user_name,user_avatar,input_message,now_time])#将用户名,头像,输入的文本添加到消息列表的最后,序号因为没有消息所以直接为1
                with open("messages.txt",'w',encoding="utf-8")as mes:#打开文件准备写入
                    writein_str=""#预写入的字符串
                    for message in message_list:#遍历消息列表
                        writein_str+=("#").join(message)+"\n"#组合文本格式添加到预写入的字符串
                    writein_str=writein_str[:-1]#清除结尾换行
                    mes.write(writein_str)#写入文本
                with open("messages.txt",'r',encoding="utf-8")as mes:
                    st.rerun()
            else:
                st.warning('👆👆&nbsp;&nbsp;&nbsp;&nbsp;好像有信息没有填充完整哦😕')