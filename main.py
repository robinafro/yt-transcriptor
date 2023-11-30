import os, sys, json

try:
    import download
    import transcribe
    import textwrap

    from colorama import Fore
except ImportError:
    print("Missing dependencies. Please run `pip install -r requirements.txt` to install them.")
    exit(1)

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

if not os.path.exists(config_path):
    raise Exception("Config file not found.")

config = json.load(open(config_path))

USER = os.path.expanduser("~")
ARG = sys.argv[1] if len(sys.argv) > 1 else None

DEFAULT_NAMES = {
    "main_dir": ".kafka-transcriptor",
    "output_dir": "output",
    "temp_dir": "temp",
}

def is_valid_path(path):
    try:
        # Check if the path is valid for both Unix and Windows
        os.path.normpath(path)
        return True
    except (ValueError, TypeError):
        return False
    
def get_folder(name):
    return os.path.join(USER, config.get(name, DEFAULT_NAMES[name]))

def initialize_folders():
    if not os.path.exists(get_folder('main_dir')):
        print(f"{Fore.BLUE}Initializing folders...{Fore.RESET}")

        os.mkdir(get_folder('main_dir'))

    if not os.path.exists(get_folder('output_dir')):
        print(f"{Fore.BLUE}Restoring folder {get_folder('output_dir')}...{Fore.RESET}")

        os.mkdir(get_folder('output_dir'))

    if not os.path.exists(get_folder('temp_dir')):
        print(f"{Fore.BLUE}Restoring folder {get_folder('temp_dir')}...{Fore.RESET}")

        os.mkdir(get_folder('temp_dir'))

def clear_dir(dir):
    for file in os.listdir(get_folder(dir)):
        os.remove(os.path.join(get_folder(dir), file))

def get_transcript(url_or_path, language):
    is_url = False

    if url_or_path.startswith('http'):
        url = url_or_path
        is_url = True
    elif is_valid_path(url_or_path):
        if not os.path.exists(url_or_path):
            raise Exception("Invalid path. File does not exist.")
        
        if not url_or_path.endswith('.wav'):
            raise Exception("Invalid path. File must be a .wav file.")

        url = os.path.join(os.path.dirname(os.path.abspath(__file__)), url_or_path)
    else:
        raise Exception("Invalid URL or path. If this is a path, make sure it is absolute.")
    
    if url.startswith('http'):
        name = url.split('=')[1]

        if '&' in name:
            name = name.split('&')[0]
            url = url.split('&')[0]
    else:
        name = os.path.basename(url).split('.')[0]

    clear_dir('temp_dir')
    
    if is_url:
        audio = download.download_and_convert_audio(url, get_folder('temp_dir'), name)
    else:
        audio = url

    transcript = transcribe.transcribe_large_audio(audio, temp_path=get_folder('temp_dir'), language=language)

    clear_dir('temp_dir')

    return name, transcript

def format_transcript(transcript):
    return textwrap.fill(transcript, width=140)

def save_transcript(name, transcript, format=False):
    if format:
        transcript = format_transcript(transcript)

    file_path = os.path.join(get_folder('output_dir'), f'{name}.txt')

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
    except UnicodeEncodeError as e:
        # Handle the exception by replacing problematic characters
        cleaned_transcript = ''.join(c if ord(c) < 128 else '?' for c in transcript)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_transcript)
        print(f"{Fore.YELLOW}Warning: UnicodeEncodeError occurred. Problematic characters replaced in {file_path}. Error: {e}{Fore.RESET}")

    print(f"{Fore.GREEN}Successfully saved transcript to {file_path}{Fore.RESET}")

def open_transcript(name):
    file_path = os.path.join(get_folder('output_dir'), f'{name}.txt')

    if not os.path.exists(file_path):
        raise Exception(f"Transcript {name} does not exist.")
    
    if not os.path.isfile(file_path):
        raise Exception(f"Transcript {name} is not a file.")

    os.startfile(file_path)

if __name__ == "__main__":
    initialize_folders()

    if ARG is not None:
        if ARG.startswith('http') or ARG.startswith('/') or ARG.startswith('\\') or ARG.startswith('C:'):
            language = config["default_lang"]

            for arg in sys.argv:
                if arg.startswith('lang='):
                    language = arg.split('=')[1]

            name, transcript = get_transcript(ARG, language)

            save_transcript(name, transcript)

            if "open" in sys.argv:
                open_transcript(name)
        elif ARG == 'open':
            if len(sys.argv) < 3:
                raise Exception("Missing argument: transcript name")
            
            open_transcript(sys.argv[2])
        elif ARG == 'list':
            print(f"{Fore.BLUE}Listing transcripts...{Fore.RESET}")

            for file in os.listdir(get_folder('output_dir')):
                print(f"{Fore.GREEN}{file.split('.')[0]}{Fore.RESET}")
        elif ARG == 'clear':
            clear_dir('output_dir')