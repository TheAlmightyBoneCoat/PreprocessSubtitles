# PreprocessSubtitles
Automatic punctuation, capitalization and grouping for YouTube subtitles.

Dependencies:
spaCy:
pip install -U pip setuptools wheel
pip install -U spacy
python3 -m spacy download en_core_web_sm

NeMo:
apt-get update && apt-get install -y libsndfile1 ffmpeg
pip install Cython
pip install nemo_toolkit[all]
