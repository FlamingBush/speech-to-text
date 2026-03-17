# speech-to-text-vosk

Offline speech-to-text in Python using Vosk.

## Features

- Offline speech recognition
- WAV file transcription
- Live microphone transcription


## Setup

pip install -r requirements.txt

## Model

wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 model

## Run

python main.py --mic --model models/en-us

python main.py --file samples/test.wav --model models/en-us
