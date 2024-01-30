import streamlit as st
import re,base64,time,os,uuid
from io import BytesIO
from pathlib import Path
from streamlit_drawable_canvas import st_canvas
from PIL import Image

def process_canvas():
    option_col,canvas_col=st.columns([0.4,0.6])
    #工具栏
    with option_col:
        with st.container(border=True):
            st.write("##### 工具栏")
   
            with st.container(border=True):
                modes={"点形":"point",  "直线":"line", "矩形":"rect", "圆形":"circle", "多边形":"polygon","对象选择":"transform","线条":"freedraw"}#模式汇总
                drawing_mode = st.selectbox(
                    "绘画模式:", ("线条","点形",  "直线", "矩形", "圆形", "多边形","对象选择")
                )#模式选择器
                drawing_mode=modes[drawing_mode]
                
                if drawing_mode == 'point':
                    point_display_radius = st.slider("点形半径: ", 1, 25, 3)
                if drawing_mode == 'polygon':
                    st.caption("*使用左键单击添加多边形顶点，加粗点为起始点，右键以结束定点添加并创建多边形")
            
            with st.container(border=True):
                stroke_color_col,fill_color_col,stroke_width_col=st.columns([0.2,0.2,0.6])
                with stroke_color_col:
                    stroke_color = st.color_picker("画笔颜色: ")
                with fill_color_col:
                    fill_color = st.color_picker("填充颜色: ",help="点形和矩形的内部颜色",value="#FFA500")
                with stroke_width_col:
                        stroke_width = st.slider("画笔粗细: ", 1, 25, 3)
            
            with st.container(border=True):
                bg_color_col,bg_img_col=st.columns([0.2,0.8])
                with bg_color_col:
                    bg_color = st.color_picker("背景颜色: ", "#eee")
                with bg_img_col:
                    bg_image = st.file_uploader("背景图片:", type=["png", "jpg"])
            
            realtime_update = st.checkbox("启用实时更新", True,help="当每次对象/选择更新或鼠标抬起时将画布数据发送到Streamlit，这可能会:red[**导致画笔中断**]，但有利于:green[**获取画布数据**]")

    #画布
    with canvas_col:
        st.write("##### 画布")
        canvas_result = st_canvas(
            fill_color=fill_color,  # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            background_image=Image.open(bg_image) if bg_image else None,
            update_streamlit=realtime_update,
            height=445,width=850,
            drawing_mode=drawing_mode,
            point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
            key="canvas",
        )
        if canvas_result is not None and canvas_result.image_data is not None:
            img_data = canvas_result.image_data
            im = Image.fromarray(img_data.astype("uint8"), mode="RGBA")
            byte_arr = io.BytesIO()  
            im.save(byte_arr, format='PNG')  
            byte_arr = byte_arr.getvalue()
            st.download_button("下载图片", data=byte_arr, file_name='画板图片.png', mime="application/octet-stream")
