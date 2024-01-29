from streamlit_tags import st_tags
import streamlit as st
import webbrowser,requests,uuid,hashlib
from bs4 import BeautifulSoup
import time,os

url = 'https://openapi.youdao.com/api'
data = {
        'q': None,
        'from': 'auto',
        'to': 'zh-CHS',
        'ext': 'mp3',
        'appKey': '74d2408d4034972b',
        'salt': str(uuid.uuid1()), 
        'signType': 'v3',
        'curtime': str(int(time.time()))
    }  

#删除历史记录按钮提醒
def remove_history_button_clicked():
    st.session_state.hist_remove=True
#抓取音频文件
def download_music_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')# 在这里使用BeautifulSoup解析页面，找到包含音乐文件URL的元素,进行相应的操作，提取音乐文件URL
        music_url = ''  # 这里存储你获取到的音乐文件URL
        
        if response.status_code == 200:
            with open("cache/sound.mp3", 'wb') as file:
                file.write(response.content)
            with open("cache/sound.mp3", 'rb') as sound:
                return_sound=sound.read()
            os.remove("cache/sound.mp3")
            return return_sound
        else:
            st.error('❗&nbsp;&nbsp;下载单词音频失败，请稍后点击刷新按钮重试...')
            if st.button("刷新",type="primary"):
                st.rerun()

    else:
        st.error('❗&nbsp;&nbsp;网络不可用，请检查你的网络状况或代理服务器')
        if st.button("刷新",type="primary"):
            st.rerun()
#网页抓取
def getsign(data):
    sha = hashlib.sha256()
    q = data['q'] if len(data['q']) <= 20 else data['q'][:10] + len(data['q']) + data['q'][-10:]
    sha.update((data['appKey'] + q + data['salt'] + data['curtime'] + 'mbccomD3aoyJm20n0aWTU3ZrtvrKl8xC').encode('utf-8'))
    return sha.hexdigest()

#读取单词文件
def load_words_dictionary():
    with open("words_space.txt","r",encoding="utf=8")as f:
        words=f.read().split("\n")#以换行大体分割每个单词
        for i in range(len(words)):
            words[i]=words[i].split("#")#以#具体分割每个单词的详细信息
            
        words_dict={}#创建单词字典
        words_history={}
        try:#判断是否有单词历史文件
            with open("words_history.txt",'r')as his:
                words_history_list=his.read().split("\n")#读取单词历史字典
                if words_history_list[-1]=="":
                    words_history_list.pop()#删除最后的空项
                for i in range(len(words_history_list)):
                    words_history_list[i]=words_history_list[i].split(":")#以:具体分割每个历史的详细信息
                for history in words_history_list:
                    words_history[history[0]]=int(history[1])
        except FileNotFoundError:#如果没有历史文件
            with open("words_history.txt",'w')as his:#创建文件
                write_text=""#写入文件的字符串
                for word in words:#将所有单词存储进历史字典,值都为0
                    words_history[word[1]]=0
                for history in words_history:#将字典内容写入字符串
                    write_text+=(str(history)+":"+str(words_history[history])+"\n")
                his.write(write_text)#写入文件
        for word in words:
            words_dict[word[1]]=[int(word[0]),word[2]]#{"单词":[编号,"词性"]}

        return words_dict,words_history
#单词查询主程序
def process_dict(words_dict,words_history):       
    #单词输入
    word_con1=st.container(border=True)#创建容器
    with word_con1:
        input_words=st_tags(
            label="""在下方输入单词并按下**回车&nbsp;Enter**以查询...""",
            text="输入需要查询的单词...",
            suggestions=list(words_dict.keys()))#标签输入框
        
        #删除记录按钮
        remove_history_space,remove_history_col=st.columns([0.75,0.25])
        with remove_history_col:
            if st.button("删除查询次数记录",use_container_width=True,type="primary",on_click=remove_history_button_clicked):
                os.remove("words_history.txt")
                st.rerun()
    
    #删除提醒
    if "hist_remove" not in st.session_state:
        st.session_state.hist_remove=False
    if st.session_state.hist_remove:
        st.toast(f'''已删除查询次数记录 ''', icon="✅")#删除成功提醒
        st.session_state.hist_remove=False
        
    #单词查询
    word_con2=st.container(border=True)#创建容器
    with word_con2:
        for input_word in input_words:#遍历输入的单词
            if input_word in list(words_dict.keys()):#判断单词是否在词典中
                words_history[input_word]+=1#查询历史次数加一
                st.write(f"**{input_word}：{words_dict[input_word][1]}**（在词典列表的第{words_dict[input_word][0]}项，共查询了{words_history[input_word]}次）")#查询结果
                #语音播放
                if input_word:
                    data['q'] = input_word
                    data['sign'] = getsign(data)#编辑请求
                    sent_content = requests.post(url, data=data)#发送请求获取单词音频
                    res_content = sent_content.json()
                    audio_1, audio_2 = st.columns(2)
                    if res_content["errorCode"]=="0":
                        with audio_1:
                            st.write("英文发音👇:")
                            res_audio=res_content['basic']["uk-speech"]#获取单词音频
                            st.audio(download_music_url(res_audio))
                        with audio_2:
                            st.write("中文发音👇:")
                            res_audio=res_content['tSpeakUrl']
                            st.audio(download_music_url(res_audio))
                    else:
                        st.error("""❗&nbsp;&nbsp;错误  
                                 单词发音获取失败，请稍后点击刷新按钮重试，或尝试单独查询此单词。""")
                        if st.button("刷新",type="primary",key=input_word+"refresh"):
                            st.rerun()
                    # st.write(res_content)
                #彩蛋
                if input_word=="balloon":
                    st.balloons()
                if input_word=="snow":
                    st.snow()
            else:
                st.write(f"""词典中找不到单词“**{input_word}**”&nbsp;&nbsp;o(╥﹏╥)o  
                         [去百度翻译查查~😎](https://fanyi.baidu.com/?aldtype=16047#en/zh/{input_word})""")
        

    #将历史写入文本文件
    with open("words_history.txt",'w')as his:#创建文件
        write_text=""#写入文件的字符串
        for history in words_history:#将字典内容写入字符串
            write_text+=(str(history)+":"+str(words_history[history])+"\n")
        his.write(write_text)#写入文件
