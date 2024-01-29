import streamlit as st
import os
from img_change import *



#回调函数,将生成字符画的按钮状态设为相反
def code_button_clicked():
    st.session_state.code=not st.session_state.code

# #调取获取保存路径器
# def get_save_dialog():
#      # 创建Tkinter根窗口对象
#     root = Tk()
#     root.withdraw()
    
#     # 调用文件选择对话框并获取所选文件的路径
#     path = tkinter.filedialog.askdirectory(title="选择保存路径")
    
#     # 关闭Tkinter根窗口
#     root.destroy()

#     return path

#保存图片按钮提醒
def save_image_button_clicked():
    st.session_state.save_image=True
#保存字符画文本按钮提醒
def save_txt_button_clicked():
    st.session_state.save_txt=True
    
#图片处理主函数 
def process_draw(img,file_name):
    img_con2=st.container(border=True)#容器
    with img_con2:
        st.write("原图:")
        st.image(img,caption=f"{file_name}",use_column_width=True)#显示图片
        
        st.write("图片处理：")
        img_tab1,img_tab2,img_tab3,img_tab4=st.tabs(["通道","滤镜","增强","效果"])
        #通道选项
        with img_tab1:
            img_con3=st.container(border=True)#容器
            with img_con3:
                option = st.selectbox("图片RGB色值换序",["(R,B,G)","(B,R,G)","(B,G,R)","(G,R,B)","(G,B,R)","(R,G,B)"],index=5,placeholder="选择一种RGB通道的顺序...",help="通过将图片的RGB通道顺序进行改变达到出现不同色调的效果")# 选择器,默认RGB,
                alpha=st.slider("透明度(Alpha)",0,255,255,help="0表示图片完全透明，255表示图片完全不透明")#透明度滑块
                
                    
            #滤镜选项
            filter_names=["模糊","轮廓","细节","边界增强","深度边缘增强","浮雕","寻找边界","平滑","深度平滑","锐化","高斯模糊"]#滤镜列表
            with img_tab2:
                img_con3=st.container(border=True)#容器
                with img_con3:
                    #生成滤镜勾选框
                    filter_flags=[]#滤镜勾选框列表
                    for i in range(5):
                        filt_col1,filt_col2=st.columns([1,1])#并列容器
                        with filt_col1:
                            filter_flags.append(st.checkbox(filter_names[i*2]))#添加滤镜勾选框
                        with filt_col2:
                            filter_flags.append(st.checkbox(filter_names[i*2+1]))#添加滤镜勾选框
                    filter_flags.append(st.checkbox(filter_names[-1],help="可调节模糊度的模糊方式"))#添加滤镜勾选框
                    gs_radio=5#高斯模糊系数
                    if filter_flags[-1]:
                        gs_radio=st.slider("高斯模糊系数",1,20,10,help="数值越大，图片越模糊")#高斯模糊系数滑块
                    else:
                        st.slider("高斯模糊系数",1,20,gs_radio,help="*需先勾选“高斯模糊”。 数值越大，图片越模糊",disabled=True)#被禁用的高斯模糊系数滑块
                        gs_radio=5        

            #增强选项
            with img_tab3:
                img_con3=st.container(border=True)#容器
                with img_con3:
                    r_buffer=st.slider("红色通道增强系数",-255,255,0,help="数值越大，红色越明显（对应通道范围在0~255，超出部分计0或255）")#红色通道增强系数滑块
                    g_buffer=st.slider("绿色通道增强系数",-255,255,0,help="数值越大，绿色越明显（对应通道范围在0~255，超出部分计0或255）")#绿色通道增强系数滑块
                    b_buffer=st.slider("蓝色通道增强系数",-255,255,0,help="数值越大，蓝色越明显（对应通道范围在0~255，超出部分计0或255）")#蓝色通道增强系数滑块
                    contrast_buffer=st.slider("对比度增强系数",0,300,100,help="数值越大，对比度越高",format="%d%%")#对比度增强系数滑块
                    bright_buffer=st.slider("亮度增强系数",0,300,100,help="数值越大，亮度越高",format="%d%%")#亮度度增强系数滑块
                    buffers=[r_buffer,g_buffer,b_buffer,contrast_buffer,bright_buffer]#增强变量列表

            #效果选项
            with img_tab4:
                img_con3=st.container(border=True)#容器
                with img_con3:
                    #反色
                    reverse = st.checkbox('反转颜色',help="反转图片颜色（与修改透明度不兼容，透明度将设为255）")#反转勾选框
                    #像素化
                    pixelation=st.checkbox('像素化',help="对图片进行像素化处理")#像素化勾选框
                    block=10
                    if pixelation:
                        block=st.slider("像素化系数",1,20,10,help="数值越大，图片越模糊，像素化程度越深")#像素化滑块
                    else:
                        st.slider("像素化系数",1,20,block,help="*需先勾选“像素化”。 数值越大，图片越模糊，像素化程度越深",disabled=True)#被禁用的像素化滑块
                        block=1
                        
                    #字符画
                    codebt_presed=False#判断按钮是否按下
                    if not "code" in st.session_state:
                        st.session_state.code=False
                    
                    if st.session_state.code:
                        codebt_presed=True
                        st.button("撤销字符画",use_container_width=True,help="撤销字符画还原原图",type="secondary",on_click=code_button_clicked)
                    else:
                        st.button("生成字符画",use_container_width=True,help="生成一个由不同明暗字符组成的图画，缩小图片效果更明显哦~😎",type="secondary",on_click=code_button_clicked)
            

        #显示预览图片
        st.write("编辑预览：")
        img,txt=change_img(img,option,reverse,alpha,block,filter_flags,gs_radio,buffers,codebt_presed)
        st.image(img,use_column_width=True)#处理并展示

        #保存文件
        save_name=file_name.split(".")[0]+"_remixed.png"#保存文件名
        cache_name=file_name.split(".")[0]+"_cache.png"#缓存文件名

        if "save_image" not in st.session_state:
            st.session_state.save_image=False
        if st.session_state.save_image:
            st.toast(f'''图片下载成功!  
                   已保存到浏览器下载目录，请打开浏览器下载目录查看。 ''', icon="✅")#保存图片成功提醒
            st.session_state.save_image=False
            
        if "save_txt" not in st.session_state:
            st.session_state.save_txt=False
        if st.session_state.save_txt:
            st.toast(f'''文件下载成功!  
                       已保存到浏览器下载目录，请打开浏览器下载目录查看。''', icon="✅")#保存字符画文件成功提醒
            st.session_state.save_txt=False
    
        
            
        os.makedirs("cache",exist_ok=True)#创建缓存文件夹
        img.save("""cache/"""+cache_name)#先将图片保存到缓存中
        with open ("""./cache/"""+cache_name,"rb")as f:#打开缓存的图片
            st.download_button(label="保存图片文件",data=f,file_name=save_name,mime="image/png",use_container_width=True,type="primary",on_click=save_image_button_clicked)#下载到浏览器中

        os.remove("""cache/"""+cache_name)#删除缓存图片
        
        #保存字符画文本
        if txt:
            save_name=file_name.split(".")[0]+"_codedrawing.txt"#保存文件名
            st.download_button(label="保存字符画txt文本",data=txt,file_name=save_name,mime="text/txt",use_container_width=True,type="primary",on_click=save_txt_button_clicked)#下载到浏览器中          
