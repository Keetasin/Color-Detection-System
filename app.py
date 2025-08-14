import streamlit as st
import cv2
import numpy as np
import tempfile
import matplotlib.pyplot as plt
import time
import os

# --- Constants ---
FRAME_WIDTH = 640
FRAME_HEIGHT = 360
URL_READ_TIMEOUT = 5  # seconds

# --- Function Definitions ---

def process_frame(frame, hsv_params):
    """
    Processes a single video frame to detect color and draw contours.
    
    Args:
        frame: The input video frame (BGR).
        hsv_params: A dictionary containing h_min, h_max, s_min, etc.

    Returns:
        A tuple containing:
        - original_frame: The resized original frame (RGB).
        - processed_frame: The frame with detected color and contours (RGB).
        - hsv_image: The HSV version of the frame.
        - mask: The binary mask used for color detection.
    """
    resized_frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    hsv_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)
    
    lower = np.array([hsv_params['h_min'], hsv_params['s_min'], hsv_params['v_min']])
    upper = np.array([hsv_params['h_max'], hsv_params['s_max'], hsv_params['v_max']])
    mask = cv2.inRange(hsv_image, lower, upper)
    
    result = cv2.bitwise_and(resized_frame, resized_frame, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(result, contours, -1, (0, 0, 255), 2)
    
    original_frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    processed_frame_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    return original_frame_rgb, processed_frame_rgb, hsv_image, mask

def open_video_capture(source, file=None, url=None):
    """Opens a video capture object based on the selected source."""
    if source == "upload":
        if file is None:
            return None
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.read())
        return cv2.VideoCapture(tfile.name)
    elif source == "webcam":
        return cv2.VideoCapture(0, cv2.CAP_DSHOW)
    elif source == "url":
        if not url:
            return None
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        return cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    return None

# --- Main App ---

# --- UI Styling ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .st-emotion-cache-18e3th9 {padding: 2rem 1rem 1rem 1rem;}
        .color-box {
            width: 100%; height: 40px; border-radius: 5px;
            margin-top: 8px; margin-bottom: 16px; border: 2px solid #B388FF;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.markdown("<h1 style='color:#B388FF; text-align:center;'>Color Detection System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:gray; text-align:center;'>With Hue Histogram (Realtime Frame)</h4>", unsafe_allow_html=True)

# --- Sidebar Controls ---
with st.sidebar:
    st.markdown("## Adjust Color Detection (HSV)")

    hsv_params = {
        'h_min': st.number_input("Hue Min", 0, 179, 40),
        'h_max': st.number_input("Hue Max", 0, 179, 80),
        's_min': st.number_input("Saturation Min", 0, 255, 50),
        's_max': st.number_input("Saturation Max", 0, 255, 255),
        'v_min': st.number_input("Value Min", 0, 255, 50),
        'v_max': st.number_input("Value Max", 0, 255, 255)
    }

    # --- NEW: Input Validation ---
    if hsv_params['h_min'] >= hsv_params['h_max']:
        st.warning("Hue Min must be less than Hue Max.")
    if hsv_params['s_min'] >= hsv_params['s_max']:
        st.warning("Saturation Min must be less than Saturation Max.")
    if hsv_params['v_min'] >= hsv_params['v_max']:
        st.warning("Value Min must be less than Value Max.")
    
    # --- Color Preview Box ---
    avg_h = int((hsv_params['h_min'] + hsv_params['h_max']) / 2)
    avg_s = int((hsv_params['s_min'] + hsv_params['s_max']) / 2)
    avg_v = int((hsv_params['v_min'] + hsv_params['v_max']) / 2)
    hsv_color = np.uint8([[[avg_h, avg_s, avg_v]]])
    rgb_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2RGB)[0][0]
    hex_color = '#%02x%02x%02x' % tuple(rgb_color)
    st.markdown(f'<div class="color-box" style="background-color:{hex_color};"></div>', unsafe_allow_html=True)
    st.markdown(f"<center><code>{hex_color.upper()}</code> (Approximate Color)</center>", unsafe_allow_html=True)

# --- Video Source Selection ---
st.markdown("#### Select Video Source")
cols = st.columns(3)
if cols[0].button("Upload Video", key="btn_upload"): st.session_state.video_source = "upload"
if cols[1].button("Webcam", key="btn_cam"): st.session_state.video_source = "webcam"
if cols[2].button("Stream URL", key="btn_url"): st.session_state.video_source = "url"

video_source = st.session_state.get("video_source", None)
uploaded_file, stream_url = None, None

if video_source == "upload":
    uploaded_file = st.file_uploader("Upload your video file", type=["mp4", "avi", "mov"])
elif video_source == "url":
    stream_url = st.text_input("Enter the stream URL", placeholder="https://... or rtsp://...")

# --- Video Processing and Display ---
cap = open_video_capture(video_source, file=uploaded_file, url=stream_url)

if cap and cap.isOpened():
    placeholder_cols = st.columns(2)
    placeholder_orig = placeholder_cols[0].empty()
    placeholder_detect = placeholder_cols[1].empty()
    placeholder_hist = st.empty()

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps if fps > 0 else 0.03

    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        
        if time.time() - start_time > URL_READ_TIMEOUT and video_source == 'url':
            st.error("Stream connection timed out. 🌐")
            break
        if not ret:
            st.warning("Video has ended or cannot be read.")
            break

        original, processed, hsv, mask = process_frame(frame, hsv_params)

        placeholder_orig.image(original, caption="Original Frame", use_container_width=True)
        placeholder_detect.image(processed, caption="Detected Color", use_container_width=True)

        hue_channel = hsv[:, :, 0]
        hist_all = cv2.calcHist([hue_channel], [0], None, [180], [0, 180])
        hist_mask = cv2.calcHist([hue_channel], [0], mask, [180], [0, 180])
        
        fig, ax = plt.subplots(figsize=(6,3), facecolor='#0E1117')
        ax.plot(hist_all, color='gray', label='All Hue')
        ax.plot(hist_mask, color='#B388FF', label='Selected Hue', linewidth=2)
        ax.set_facecolor('#0E1117')
        ax.tick_params(colors='white')
        ax.set_title('Hue Distribution', color='#B388FF')
        ax.set_xlabel('Hue', color='white')
        ax.set_ylabel('Frequency', color='white')
        ax.legend(facecolor='#0E1117', labelcolor='white')
        placeholder_hist.pyplot(fig)
        plt.close(fig)

        time.sleep(delay)
    cap.release()
else:
    if video_source == "upload" and uploaded_file is None:
        st.info("Please upload a video file to start. 📁")
    elif video_source == "url" and (not stream_url or stream_url.strip() == ""):
        st.info("Please enter a stream URL. 🌐")
    elif video_source == "webcam" and not (cap and cap.isOpened()):
        st.error("Cannot access webcam. 📸 Please check if it's connected and not used by another app.")
    elif video_source and not (cap and cap.isOpened()):
         st.error(f"Error opening source: {video_source}. Please check the file or URL.")
    else:
        st.info("Please select a video source above. 👆")