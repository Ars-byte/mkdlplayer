python -m venv --without-pip venv
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
./venv/bin/python get-pip.py
./venv/bin/pip install pygame PyQt6 pypresence mutagen soundfile numpy
