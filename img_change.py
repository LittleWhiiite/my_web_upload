from PIL import Image,ImageOps,ImageEnhance,ImageFilter,ImageDraw
import collections as coll
import streamlit as st
import matplotlib.pyplot as plt

#图片像素化
def masaik(img,block):
    pic = img.convert("RGB")  # 打开图片并转换格式

    width, height = pic.size  # 获取图片尺寸
    block = block  # 存储像素画分辨率
    board=Image.new("RGB",pic.size)#新建空图片
    # 裁剪图片
    for y in range(0, height, block):  # 循环切割图片
        for x in range(0, width, block):
            temp = pic.crop((x, y, x+block, y+block))#保存裁剪下的图片
            temp_list=list(temp.getdata())#获取小图像素
            max_color = coll.Counter(temp_list).most_common()[0][0]  # 获取图片中最多的像素
            new_pic=Image.new("RGB",(block,block),max_color)#新建一张为最多出现次数颜色的空图
            board.paste(new_pic,(x,y))#把裁剪的图片拼接到board上
    return board

#滤镜
def filt(img,filter_flags,gs_radio):
    filters=[ImageFilter.BLUR,ImageFilter.CONTOUR,ImageFilter.DETAIL,ImageFilter.EDGE_ENHANCE,ImageFilter.EDGE_ENHANCE_MORE,
             ImageFilter.EMBOSS,ImageFilter.FIND_EDGES,ImageFilter.SMOOTH,ImageFilter.SMOOTH_MORE,ImageFilter.SHARPEN,ImageFilter.GaussianBlur]#滤镜对象列表
    for i in range(len(filters)-1):
        if filter_flags[i]:
            img=img.filter(filters[i])#逐一判断并添加滤镜
    if filter_flags[-1]:
        img=img.filter(ImageFilter.GaussianBlur(gs_radio))#高斯模糊
    return img

#字符画
def draw_code(img_):
    #灰度图
    img=img_.convert("L")
    
    #图片等比例缩小
    width,height=img.size
    max_px=500
    if max(width,height)>max_px:
        if width>height:
            height=round(max_px*(height/width))
            width=max_px
        elif height>width:
            width=round(max_px*(width/height))
            height=max_px
        elif height==width:
            height,width=max_px,max_px
    
    img=img.resize((width,height))#重设图片比例
    plt.rcParams["image.cmap"] = "gray"
    
    
    ASCII_HIGH ='''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. '''
    #字符串
    txt=""
    for y in range(height):
        for x in range(width):
            pos=(x,y)
            gray=img.getpixel(pos)
            index=int(gray/256*70)
            txt += ASCII_HIGH[index]+" "
        txt+="\n"
    # print(txt)
    
    #with open("bcm.txt","w")as f:
        #f.write(txt)
    #文本转图片
    img_new=Image.new("RGB",(width*12,height*12),"white")
    draw=ImageDraw.Draw(img_new)
    draw.text((0,0),txt,fill="black",spacing=1)

    return txt,img_new

    
#更改图片
@st.cache_resource(show_spinner="图片渲染中...")
def change_img(_img,order,reverse,alpha,block,filter_flags,gs_radio,buffers,code_draw):
    

    #对比度
    con=buffers[3]/100#获取对比度数值
    enhancer=ImageEnhance.Contrast(_img)#实例化对比度对象
    _img=enhancer.enhance(con)#设置对比度

    #明亮度
    bri = buffers[4]/100#获取亮度数值
    enhancer = ImageEnhance.Brightness(_img)  # 实例化明亮度对象
    _img = enhancer.enhance(bri)  # 设置明亮度
    _img.convert("RGBA")
    
    #反转图片
    if reverse:
        _img=ImageOps.invert(_img.convert("RGB"))#设置图片为反色
    _img.convert("RGBA")
    
    #像素化
    if block:
        _img=masaik(_img,block).convert("RGBA")

    #滤镜
    if True in filter_flags:
        _img=filt(_img,filter_flags,gs_radio)
    
    txt=''
    #字符画
    if code_draw:
        txt,_img=draw_code(_img)
        
    
    #获取RGB顺序
    if order=="(R,B,G)":
        rc,gc,bc=(0,2,1)
    elif order=="(R,G,B)":
        rc,gc,bc=(0,1,2)
    elif order=="(B,R,G)":
        rc,gc,bc=(1,2,0)
    elif order=="(B,G,R)":
        rc,gc,bc=(2,1,0)
    elif order=="(G,R,B)":
        rc,gc,bc=(1,0,2)
    elif order=="(G,B,R)":
        rc,gc,bc=(2,0,1)
    #修改RGB通道顺序
    _img.convert("RGBA")
    width,height=_img.size#获取图片宽高
    img_array=_img.load()#获取图片像素值
    for x in range(width):#双重循环遍历每一个像素
        for y in range(height):
            #获取rgb值
            r=img_array[x,y][rc]+buffers[0]#将顺序和增强作为参数
            g=img_array[x,y][gc]+buffers[1]
            b=img_array[x,y][bc]+buffers[2]
            a=alpha#设置透明度
            img_array[x,y]=(r,g,b,a)#调换顺序重新把rgb赋值回去
    return _img,txt

