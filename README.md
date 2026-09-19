# Final project

Emotion Detector web application using the Watson NLP endpoint supplied by Skills Network.

## Run in the Skills Network lab

1. Install dependencies: `python3 -m pip install --user -r requirements.txt`.
2. Run the required live tests: `python3 -m unittest test_emotion_detection -v`.
3. Run error-handling tests: `python3 -m unittest test_error_handling -v`.
4. Run static analysis: `python3 -m pylint server.py`.
5. Start the app: `python3 server.py` and open port 5000 through the lab launcher.

`python3 verify_project.py` repeats service checks and saves their real output under `evidence/`.
The Watson endpoint is supplied by the course and may require the Skills Network environment.

## Structure

- `EmotionDetection/emotion_detection.py`: service request, JSON parsing, scores and HTTP 400 handling.
- `EmotionDetection/__init__.py`: package export.
- `server.py`: Flask interface.
- `test_emotion_detection.py`: five live-service tests required by the lab.
- `test_error_handling.py`: additional isolated error-handling tests.
- `templates/` and `static/`: original IBM starter interface.
- `evidence/`: actual development outputs and code snapshots.

## Review before submission

This development draft was prepared with AI assistance. Review and understand the code and validate it in your own environment before deciding what to submit under your course rules.
A public repository in your own GitHub account and final assessment submission are separate steps.
The existing IBM starter LICENSE applies to the supplied starter files.
