import os

import boto3
from dotenv import load_dotenv

load_dotenv()

# Create a client for Amazon Polly
polly_client = boto3.Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                             aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                             region_name=os.getenv("REGION_NAME")).client('polly')


class Speaker:

    @staticmethod
    def synthesize_speech(text, voice_id, engine="standard", output_format="mp3", text_type="text"):
        """
        Synthesize speech using Amazon Polly and return the audio stream.

        Parameters:
        - text: The text to convert to speech
        - voice_id: The voice to use (e.g., 'Joanna', 'Matthew')
        - engine: The engine to use ('standard', 'neural', or 'long-form')
        - output_format: The output format ('mp3', 'ogg_vorbis', or 'pcm')
        - text_type: The type of input text ('text' or 'ssml')

        Returns:
        - Audio stream
        """
        try:
            response = polly_client.synthesize_speech(Text=text, VoiceId=voice_id, Engine=engine,
                                                      OutputFormat=output_format, TextType=text_type)
            return response['AudioStream'].read()
        except Exception as e:
            print(f"Error synthesizing speech: {str(e)}")
            return None

    @staticmethod
    def save_audio_file(audio_data, file_path):
        """
        Save audio data to a file.

        Parameters:
        - audio_data: The audio data to save
        - filename: The name of the file to save to
        """
        if audio_data:
            try:
                with open(file_path, 'wb') as file:
                    file.write(audio_data)
                print(f"Audio saved to {file_path}")
            except Exception as e:
                print(f"Error saving audio file: {str(e)}")
