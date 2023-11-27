# yt-transcriptor

a tool that allows you to easily generate transcriptions for any youtube video.

# installation

- run `git clone https://github.com/Actulurus/yt-transcriptor.git/`
- cd into the repository
- run `pip install -r requirements.txt`

# usage

`python main.py "https://youtube.com/watch?v=video_id"` - generate transcriptions - add `open` after the url to open the text file when done - add `lang=en-US` with a valid language of this format to change the language
`python main.py "C:\Users\username\Documents\...."`- same as above, just a local file instead of a youtube video. File must be in .wav format!
`python main.py open "video_id"` - open an already existing transcriptions file

# configuration

in the config.json file, you can change the directories that the files save to. you can also use it to change the default language.
