
# Chanchu's Drowsiness Detector

Chanchu's Drowsiness Detector is a web application that uses OpenCV and MediaPipe to detect drowsiness in real-time via a webcam feed. The app triggers an alert when it detects signs of drowsiness, such as prolonged eye closure.

## Features

- **Real-Time Drowsiness Detection**: Uses Eye Aspect Ratio (EAR) to monitor eye closure and trigger an alert if drowsiness is detected.
- **Web-Based Interface**: The application runs as a Flask web app, accessible through a browser.
- **Alert Sound**: Plays a buzzer sound when drowsiness is detected.
- **Neon-Themed UI**: The web interface features a purple neon background with a modern design.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/chanchu-drowsiness-detector.git
   cd chanchu-drowsiness-detector
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Download the `buzzer.mp3` file and place it in the project directory.**

## Running the Application

1. **Start the Flask web server:**

   ```bash
   python app.py
   ```

2. **Open your web browser and go to:**

   ```
   http://127.0.0.1:5000/
   ```

3. **Allow the website to access your webcam.**

4. **The application will start displaying the webcam feed.**

   - If drowsiness is detected, a message "You Are Sleeping!" will appear on the right side of the screen, and an alert sound will play.

## File Structure

```
/chanchu_drowsiness_detector
|-- app.py               
|-- requirements.txt     
|-- templates/
|   |-- index.html       
|-- static/
|   |-- style.css       
|-- buzzer.mp3          
```

## Dependencies

- Flask
- OpenCV
- MediaPipe
- NumPy
- SciPy
- Pygame

These are listed in the `requirements.txt` file. Install them using:

```bash
pip install -r requirements.txt
```

## Usage

This application is designed for monitoring drowsiness in real-time. It can be particularly useful for drivers, machine operators, or anyone needing to stay alert. The app will alert you visually and audibly if it detects that you're drowsy.


## Acknowledgements

- [MediaPipe](https://github.com/google/mediapipe) - For face detection and landmarks.
- [OpenCV](https://opencv.org/) - For handling webcam feed and image processing.
- [Pygame](https://www.pygame.org/) - For playing the alert sound.
```
