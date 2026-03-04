import os
import google.generativeai as genai
# from utilities import get_value
import random

KEYS_FILE = 'keys.json'
# PATHS_FILE = 'paths.json'
TOPICS_FILE = 'topics.txt'
COVERED_TOPICS_FILE = 'topics-covered.txt'
MODEL = "gemini-1.5-flash"
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
BASE_PROMPT_FILE = 'prompt-base.txt'
PROMPT_FILE = 'prompt.txt'
# OUTPUT_SCRIPT_PATH = get_value(PATHS_FILE, "script_path")


def get_script_topic(file1, file2):
    """
    Reads a random line from file1, checks if the word exists in file2.
    Keeps picking random words until a unique word is found.
    Writes the unique word to file2 and returns it.

    :param file1: Path to the first file containing a list of words (one per line).
    :param file2: Path to the second file where unique words will be checked and written.
    :return: The unique word that was written to file2.
    """
    # Read all words from file2 into a set for faster lookup
    with open(file2, 'r') as f2:
        file2_words = set(f2.read().splitlines())
    
    # Read all lines from file1
    with open(file1, 'r') as f1:
        file1_words = f1.read().splitlines()
    
    while True:
        # Pick a random word from file1
        random_word = random.choice(file1_words)
        # Check if it is in file2
        if random_word not in file2_words:
            # If not, write it to file2 and return it
            with open(file2, 'a') as f2:
                f2.write(random_word + '\n')
            return random_word
        

def get_prompt_first_line(topic):
    return "I am making a YouTube shorts video on \"" + topic + "\"."


def update_prompt(first_line):
    """
    Prepends a given line to the beginning of a file.

    :param file_path: Path to the file.
    :param line: The string to prepend to the file.
    """
    # Read the original contents of the base prompt file
    with open(BASE_PROMPT_FILE, 'r') as file:
        original_contents = file.readlines()
    
    # Write the new line followed by the original contents to the prompt file
    with open(PROMPT_FILE, 'w') as file:
        file.write(first_line + ' ')
        file.writelines(original_contents)


def get_prompt(file):
    f = open(file, "r")
    content = f.read()
    f.close()
    return content


def write_to_file(output_file, content):
    f = open(output_file, "w")
    f.write(content)
    f.close()


def get_script(output_file_name):
    # get the topic and prepare the prompt
    update_prompt(get_prompt_first_line(get_script_topic(TOPICS_FILE,COVERED_TOPICS_FILE)))

    # consume gemini api to get the script
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(get_prompt(PROMPT_FILE))    
    write_to_file(output_file_name, response.text)
