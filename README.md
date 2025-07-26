# 241-353 AI ECOSYSTEM MODULE

##  Color Detection System with Hue Histogram (Realtime Frame)

### Project Overview

This is a simple web application built with Streamlit that detects a specified color range in video frames (from a video file, webcam, or stream URL) and shows the hue distribution histogram in real time.

---

### Features

- Upload a video file or use your webcam or stream URL as video source
- Adjust HSV (Hue, Saturation, Value) parameters to specify the color range for detection
- Real-time color detection with mask visualization
- Display the hue histogram of the detected color area
- Clean and user-friendly interface with custom styles

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
1. Run the application:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and go to:
   ```
   http://localhost:8501
   ```