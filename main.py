import os
import json
import re
from datetime import datetime
from image_fetcher import get_image
import script_fetcher
from speech_fetcher import get_speech
import editor

# -- Utility Functions --
# Function to get the value from any json file
def get_value(file, key):
    f = open(file)
    data = json.load(f)
    value = data[key]
    f.close()
    return value


# Declare the constants
IMAGE_PATH = ''
SPEECH_PATH = ''
VIDEO_DIRECTORY = ''
VIDEO_COUNTER_FILE = 'acc_data.json'
VIDEO_COUNT = get_value(VIDEO_COUNTER_FILE, 'video_counter')
LOG_FILE = ''
OUTPUT_FILE = ''
TEMP_PROMPT_NAME = 'prompt.txt'
TEMP_SCRIPT_NAME = 'script.txt'
TEMP_OUTPUT_NAME = 'final_video.mp4'


def make_directories(video_title):
    global IMAGE_PATH, SPEECH_PATH, VIDEO_DIRECTORY, VIDEO_COUNT, LOG_FILE, OUTPUT_FILE
    VIDEO_DIRECTORY = 'res/' + str(VIDEO_COUNT) + '_' + re.sub("[^A-Z]", "", video_title,0,re.IGNORECASE)
    IMAGE_PATH = VIDEO_DIRECTORY + '/images'
    SPEECH_PATH = VIDEO_DIRECTORY + '/speech'
    if(not os.path.exists(VIDEO_DIRECTORY)):
        os.mkdir(VIDEO_DIRECTORY)
    if(not os.path.exists(IMAGE_PATH)):
        os.mkdir(IMAGE_PATH)
    if(not os.path.exists(SPEECH_PATH)):
        os.mkdir(SPEECH_PATH)
    
    dt_string = datetime.now().strftime("%Y%m%d%H%M%S")
    # set the output file path
    OUTPUT_FILE = VIDEO_DIRECTORY + '/' + 'output_' + dt_string + '.mp4'
    # set the logfile
    LOG_FILE = VIDEO_DIRECTORY + '/' + 'log_'+ dt_string + '.txt'


def get_script_dictionary():
    script_dictionary = {}
    f = open('script.txt', 'r')
    # read and ignore the first line
    f.readline()
    for line in f.readlines():
        if line.strip():
            script_dictionary[line.split('|')[0]] = line.split('|')[1].strip()
    return script_dictionary
  

# Fetch the script and save it
script_fetcher.get_script('script.txt')

# Extract the video title from the script
VIDEO_TITLE = open('script.txt', 'r').readline()

# Create the required directories in res/
make_directories(VIDEO_TITLE)

# start writing to the log file
if(os.path.exists(LOG_FILE)):
    os.remove(LOG_FILE)
log = open(LOG_FILE, 'a')

VIDEO_NAME = str(VIDEO_COUNT) + '_' + VIDEO_TITLE + '.mp4'

script_dictionary = get_script_dictionary()

print("script_dictionary: " )
print(script_dictionary)
log.write('script_dictionary \n')
log.write(str(script_dictionary))
log.write('\n\n')
print('\n\n')

# Initialize the media sets to be populated and send to the editor
media_sets = []

# Fetch and save the image and speech resources
for i in range (0,len(script_dictionary)):
    # key is the image prompt
    image_complete_path = IMAGE_PATH + '/' + str(i) + '.jpg'
    speech_complete_path = SPEECH_PATH + '/' + str(i) + '.mp3'
    image_prompt, speech_text = list(script_dictionary.items())[i]
    get_image(image_complete_path, image_prompt+". Do not include any text in the image.")
    get_speech(speech_complete_path, speech_text)

    # add the image and speech names to the media_sets
    media_sets.append({"image" : image_complete_path, "audio" : speech_complete_path})

print("media_sets: " )
print(media_sets)
log.write('media_sets\n')
log.write(str(media_sets))
# print("---Checking resources---")
# print("---Checking images---")
# for file in os.listdir(IMAGE_PATH):
#     print(file)
# print("---Checking audio---")
# for file in os.listdir(SPEECH_PATH):
#     print(file)


# Execute the editor
try:
    editor.run_editor(media_sets, TEMP_OUTPUT_NAME)
except Exception as e:
    print(f"An error occurred while creating the video: {e}")


# Rename and move the script, prompt adn the output to the VIDEO_DIRECTORY; update the video counter in acc_data.json
def perform_cleanup():
    print('Performing Cleanup...')
    print('Rename and move the script, prompt and output to the VIDEO_DIRECTORY')
    if(os.path.exists(TEMP_PROMPT_NAME)):
        os.rename(TEMP_PROMPT_NAME, VIDEO_DIRECTORY + '/' +str(VIDEO_COUNT) + '_' + TEMP_PROMPT_NAME)
    if(os.path.exists(TEMP_SCRIPT_NAME)):
        os.rename(TEMP_SCRIPT_NAME, VIDEO_DIRECTORY + '/' +str(VIDEO_COUNT) + '_' + TEMP_SCRIPT_NAME)
    if(os.path.exists(TEMP_OUTPUT_NAME)):
        os.rename(TEMP_OUTPUT_NAME, VIDEO_DIRECTORY + '/' +str(VIDEO_COUNT) + '_' + TEMP_OUTPUT_NAME)
    
    print('Updating the video counter in acc_data.json')
    # udpate the video counter in acc_data.json
    """
    Reads a JSON file, increments the 'video_counter' value by 1, 
    and updates the file.

    :param json_file: Path to the JSON file.
    """
    try:
        # Read the JSON file
        with open(VIDEO_COUNTER_FILE, 'r') as file:
            data = json.load(file)
        
        # Increment the 'video_counter' value
        if "video_counter" in data:
            data["video_counter"] += 1
        else:
            raise KeyError("'video_counter' key not found in the JSON file.")
        
        # Write the updated JSON back to the file
        with open(VIDEO_COUNTER_FILE, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"Updated 'video_counter' to {data['video_counter']}.")
    except FileNotFoundError:
        print(f"Error: File '{VIDEO_COUNTER_FILE}' not found.")
    except json.JSONDecodeError:
        print(f"Error: File '{VIDEO_COUNTER_FILE}' is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")

perform_cleanup()

print('Script Executed Successfully!!')