import os
import boto3
# from utilities import get_value

ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


def get_speech(output_speech_file, text):
    # Initialize Polly client with credentials
    polly = boto3.client(
        'polly',
        region_name='us-east-1',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_ACCESS_KEY
    )

    # Convert text to speech
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna',
        Engine='generative'
        # Engine options: standard | neural | long-form | generative
    )

    # Save the audio to a file
    with open(output_speech_file, 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Speech synthesized and saved as ' + output_speech_file)

