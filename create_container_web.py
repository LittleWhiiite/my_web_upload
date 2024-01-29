import streamlit as st
from PIL import Image
def main(txt,scale):
    ####读取网页文本文件
    #获取文本
    with open(txt,"r",encoding="utf-8")as f:
        string=f.read()
    
    #将文本按容器分割
    contains=string.split("--------\n")
    length=len(contains)#存储容器数量
    
    #将文本进一步按单项文本分割
    for contain in range(len(contains)):
        contains[contain]=contains[contain].split("-\n")
    #删除多余项
    for text in contains:
        if text[0]=="":
            text.pop(0)
        if text[-1]=="":
            text.pop() 
    
    ####创建容器对象
    #分门别类创建容器框架函数
    def create_container_web_vedio(text1,url,text3,col):#多个文本替代项,并列容器对象
        with col:#在每个并列容器中
            with st.container(border=True):#创建容器(共row个)
                text1=Image.open(text1).resize((450,400))#读取图片并修改尺寸
                st.image(text1,use_column_width="always")#图片
                st.link_button("点此观看",url,use_container_width=True,help="跳转到**Bilibili**并观看视频",type="primary")#链接按钮
                with st.expander("详细信息..."):#创建下拉框
                    st.write(text3)#详细描述
                    
    def create_container_web_music(text1,text2,url1,url2,url3,col):#多个文本替代项,并列容器对象
        with col:#在每个并列容器中
            with st.container(border=True):#创建容器(共row个)
                st.write(text1)#标题
                st.write(text2,unsafe_allow_html=True)#音频插件
                st.link_button("在**网易云音乐**听",url1,use_container_width=True,help="跳转到**网易云音乐**并聆听音频",type="primary")#链接按钮
                bt_col1,bt_col2=st.columns([1,1])#创建并列
                with bt_col1:
                    st.link_button("在**酷狗音乐**听",url2,use_container_width=True,help="跳转到**酷狗音乐**并聆听音频",type="primary")#链接按钮
                with bt_col2:
                    st.link_button("在**QQ音乐**听",url3,use_container_width=True,help="跳转到**QQ云音乐**并聆听音频",type="primary")#链接按钮
                    
    def create_container_web_tool(text1,text2,text3,text4,url,col):#多个文本替代项,并列容器对象
        with col:#在每个并列容器中
            with st.container(border=True):#创建容器(共row个)
                st.subheader(text1,anchor=False)#标题
                st.write(text2)#概述
                st.image(text3,use_column_width=True)#图片
                st.link_button(text4,url,use_container_width=True,help="https://wupanhao.github.io/tuner/",type="primary")#链接按钮         
    
    def create_container_web_game(text1,text2,text3,text4,text5,text6,col):#多个文本替代项,并列容器对象
        with col:#在每个并列容器中
            with st.container(border=True):#创建容器(共row个)
                st.subheader(text1,anchor=False)#标题
                st.write(text2)#概述
                st.image(text3,caption=text4,use_column_width=True)#图片
                with st.expander("了解更多..."):#创建下拉框
                    st.write(text5)#详细描述
                    st.write(text6)#链接
    

                
    #循环创建并列容器并创建普通容器
    i=0#容器循环数变量(并列容器个数)
    ct_index=0#容器遍历到第几个
    row=len(scale)#记录列数
    for i in range((length-length%row)//row):#执行行数-1次,因为一个并列容器有row个容器,所以循环创建并列容器的次数是容器数1/row,如果容器数有余数也先执行前面整行的,留剩下的在后面执行 
        cols=st.columns(scale)#创建并列容器(因为宽度项数下方设置为row,所以一次会生成row个col)
        for col in cols:#(因为上方创建了row个col所以会执行row次)
            #分别创建容器
            if txt=="games.txt":
                text1,text2,text3,text4,text5,text6=contains[ct_index]#分别将文本内容赋值
                create_container_web_game(text1,text2,text3,text4,text5,text6,col)#执行函数
            elif txt=="vedios.txt":
                text1,text2,text3=contains[ct_index]#分别将文本内容赋值
                create_container_web_vedio(text1,text2,text3,col)#执行函数
            elif txt=="musics.txt":
                text1,text2,url1,url2,url3=contains[ct_index]#分别将文本内容赋值
                create_container_web_music(text1,text2,url1,url2,url3,col)#执行函数
            elif txt=="tools.txt":
                text1,text2,text3,text4,url=contains[ct_index]#分别将文本内容赋值
                create_container_web_tool(text1,text2,text3,text4,url,col)#执行函数
            ct_index+=1
        scale=scale[::-1]#比例颠倒,并列容器比例交替出现
        i+=1
          
    if length%row!=0:#判断容器数量是否多出一个
        ##再多执行一遍创建容器代码
        cols=st.columns(scale)#创建并列容器(因为宽度项数下方设置是row所以一次会生成row个col)
        #在执行一次创建框架
        for x in range(length%row):#创建余下不够一整行的容器
            if txt=="games.txt":
                text1,text2,text3,text4,text5,text6=contains[ct_index]#分别将文本内容赋值
                create_container_web_game(text1,text2,text3,text4,text5,text6,cols[x])#执行函数
            elif txt=="vedios.txt":
                text1,text2,text3=contains[ct_index]#分别将文本内容赋值
                create_container_web_vedio(text1,text2,text3,cols[x])#执行函数
            elif txt=="musics.txt":
                text1,text2,url1,url2,url3=contains[ct_index]#分别将文本内容赋值
                create_container_web_music(text1,text2,url1,url2,url3,cols[x])#执行函数
            elif txt=="tools.txt":
                text1,text2,text3,text4,url=contains[ct_index]#分别将文本内容赋值
                create_container_web_tool(text1,text2,text3,text4,url,cols[x])#执行函数

#main("tools.txt",[0.5,0.5])#执行创建容器代码