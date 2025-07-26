import streamlit as st
import cv2
import numpy as np
import tempfile
import matplotlib.pyplot as plt
import time

# Hide footer & hamburger (optional)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .css-18e3th9 {padding: 2rem 1rem 1rem 1rem;}
        .color-box {
            width: 100%;
            height: 40px;
            border-radius: 5px;
            margin-top: 8px;
            margin-bottom: 16px;
            border: 2px solid #B388FF;
        }
        .video-source-btn {
            background-color: #B388FF;
            color: white;
            padding: 0.5rem 1.2rem;
            border-radius: 0.5rem;
            font-weight: bold;
            margin: 0.2rem;
            border: none;
            cursor: pointer;
        }
        .video-source-btn:hover {
            background-color: #7A4FFF;
        }
        .selected-btn {
            background-color: #7A4FFF !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#B388FF; text-align:center;'>Color Detection System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:gray; text-align:center;'>With Hue Histogram (Realtime Frame)</h4>", unsafe_allow_html=True)

# Sidebar - HSV control
with st.sidebar:
    st.markdown("## Adjust Color Detection Parameters (HSV)")

    h_min = st.number_input("Hue Min", 0, 179, 150)
    h_max = st.number_input("Hue Max", 0, 179, 170)
    s_min = st.number_input("Saturation Min", 0, 255, 100)
    s_max = st.number_input("Saturation Max", 0, 255, 255)
    v_min = st.number_input("Value Min", 0, 255, 150)
    v_max = st.number_input("Value Max", 0, 255, 255)

    avg_h = int((h_min + h_max) / 2)
    avg_s = int((s_min + s_max) / 2)
    avg_v = int((v_min + v_max) / 2)
    hsv_color = np.uint8([[[avg_h, avg_s, avg_v]]])
    rgb_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2RGB)[0][0]
    hex_color = '#%02x%02x%02x' % tuple(rgb_color)
    st.markdown(f'<div class="color-box" style="background-color:{hex_color};"></div>', unsafe_allow_html=True)
    st.markdown(f"<center><code>{hex_color.upper()}</code> (Approximate detected color)</center>", unsafe_allow_html=True)

# --- Video Source Selection Buttons ---
st.markdown("#### Select Video Source")

col1, col2, col3 = st.columns(3)
video_source = st.session_state.get("video_source", None)

if col1.button("Upload Video", key="btn_upload"):
    st.session_state.video_source = "upload"
if col2.button("Webcam", key="btn_cam"):
    st.session_state.video_source = "webcam"
if col3.button("Stream URL", key="btn_url"):
    st.session_state.video_source = "url"

video_source = st.session_state.get("video_source", None)

uploaded_file = None
stream_url = None

if video_source == "upload":
    uploaded_file = st.file_uploader("Upload your video file", type=["mp4", "avi", "mov"])
elif video_source == "url":
    stream_url = st.text_input("Enter the stream URL, e.g., rtsp:// or http://")

def open_video_capture():
    if video_source == "upload":
        if uploaded_file is None:
            return None
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        return cv2.VideoCapture(tfile.name)
    elif video_source == "webcam":
        return cv2.VideoCapture(0)
    elif video_source == "url":
        if not stream_url:
            return None
        return cv2.VideoCapture(stream_url)
    return None

cap = open_video_capture()

if cap is not None and cap.isOpened():
    placeholder_cols = st.columns(2)
    placeholder_orig = placeholder_cols[0].empty()
    placeholder_detect = placeholder_cols[1].empty()
    placeholder_hist = st.empty()

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps if fps > 0 else 0.03

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("Cannot read the video or video has ended.")
            break

        frame = cv2.resize(frame, (640, 360))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        placeholder_orig.image(frame_rgb, caption="Original Frame", use_container_width=True)
        placeholder_detect.image(result_rgb, caption="Detected Color", use_container_width=True)

        hue_channel = hsv[:, :, 0]
        hist = cv2.calcHist([hue_channel], [0], mask, [180], [0, 180])

        fig, ax = plt.subplots(figsize=(6,3), facecolor='#1E1E2F')
        ax.plot(hist, color='#B388FF')
        ax.set_facecolor('#1E1E2F')
        ax.tick_params(colors='white')
        ax.set_title('Hue Distribution', color='#B388FF')
        ax.set_xlabel('Hue', color='white')
        ax.set_ylabel('Frequency', color='white')

        placeholder_hist.pyplot(fig)
        plt.close(fig)

        time.sleep(delay)

    cap.release()
else:
    if video_source == "upload" and uploaded_file is None:
        st.info("Please upload a video file to start.")
    elif video_source == "url" and (not stream_url or stream_url.strip() == ""):
        st.info("Please enter a stream URL.")
    elif video_source == "webcam":
        st.info("Waiting for webcam connection...")
    elif video_source is None:
        st.info("Please select a video source above.")
