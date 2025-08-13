# 241-353 AI ECOSYSTEM MODULE

##  Color Detection System with Hue Histogram (Realtime Frame)

### Project Overview

This is a simple web application built with **Streamlit** that performs real-time color detection on a video stream. It allows users to select a video source (uploaded file, webcam, or stream URL), adjust the color range using HSV parameters, and visualize both the detected color area and its hue distribution in a live histogram.

---

### Features

- **Flexible Video Sources:** Supports video from a local file, a live webcam feed, or a network stream URL (e.g., `rtsp://`).
- **Customizable Color Detection:** Use interactive sliders in the sidebar to define the target color range by adjusting Hue, Saturation, and Value (HSV) minimum and maximum thresholds.
- **Real-time Visualization:** Displays the original video frame side-by-side with the processed frame, where the detected color is highlighted with contours.
- **Live Hue Histogram:** Generates and updates a histogram in real time, showing the hue distribution of the entire frame and specifically for the detected color area.
- **User-friendly Interface:** A clean, responsive GUI with custom CSS styles makes the application easy to use.

---


### Setup & Installation

Ensure that you have Python installed on your system before proceeding.

1. Clone the repository:
   ```bash
   git clone <repo-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-folder>
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
      ```bash
      venv\Scripts\activate
      ```
   - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
---

### Running and Viewing the Application

Ensure you're inside the project directory and the virtual environment is activated.
1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```
2.  A new browser tab will automatically open, or you can manually navigate to:
    ```
    http://localhost:8501
    ```