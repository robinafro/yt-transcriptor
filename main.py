import os, sys, json, subprocess

from . import download
from . import transcribe

config = json.load(open('config.json'))

USER = os.path.expanduser("~")
ARG = sys.argv[1] if len(sys.argv) > 1 else None

DEFAULT_NAMES = {
    "main_dir": ".kafka-transcriptor",
    "output_dir": "output",
    "temp_dir": "temp",
}

def get_folder(name):
    return os.path.join(USER, config.get(name, DEFAULT_NAMES[name]))

def initialize_folders():
    if not os.path.exists(get_folder('main_dir')):
        os.mkdir(get_folder('main_dir'))

    if not os.path.exists(get_folder('output_dir')):
        os.mkdir(get_folder('output_dir'))

    if not os.path.exists(get_folder('temp_dir')):
        os.mkdir(get_folder('temp_dir'))

def clear_dir(dir):
    for file in os.listdir(get_folder(dir)):
        os.remove(os.path.join(get_folder(dir), file))

def get_transcript(url):
    name = url.split('=')[1]

    clear_dir('temp_dir')
    
    download.download_and_convert_audio(url, get_folder('temp_dir'))

    transcript = transcribe.transcribe_large_audio(os.path.join(get_folder('temp_dir'), f'{name}.wav'))

    clear_dir('temp_dir')

    return name, transcript

def save_transcript(name, transcript):
    with open(os.path.join(get_folder('output_dir'), f'{name}.txt'), 'w') as f:
        f.write(transcript)

def open_transcript(name):
    if os.name == 'posix':
        editor_cmd = 'xdg-open'
    elif os.name == 'nt':
        editor_cmd = 'start'
    else:
        raise Exception("Unsupported operating system")
    
    file_path = os.path.join(get_folder('output_dir'), f'{name}.txt')

    full_cmd = [editor_cmd, file_path]

    # Use subprocess to open the file
    subprocess.run(full_cmd, check=True)

if __name__ == "__main__":
    initialize_folders()

    if ARG is not None:
        if ARG.startswith('http'):
            name, transcript = get_transcript(ARG)

            save_transcript(name, transcript)

            if len(sys.argv) > 2 and sys.argv[2] == 'open':
                open_transcript(name)
        elif ARG == 'open':
            if len(sys.argv) < 3:
                raise Exception("Missing argument: transcript name")
            
            open_transcript(sys.argv[2])
        elif ARG == 'clear':
            clear_dir('output_dir')