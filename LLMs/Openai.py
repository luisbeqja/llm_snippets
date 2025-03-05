import os
from openai import OpenAI

# Initialize the OpenAI client
# Make sure to set your API key as an environment variable
client = OpenAI(
    # This is the recommended way to store API keys
    api_key=os.environ.get("OPENAI_API_KEY")
)

def generate_text_completion():
    """
    Generate a text completion using the GPT model.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to gpt-4 or other models
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a short poem about technology."}
            ],
            max_tokens=150,
            temperature=0.7
        )
        print("Text Completion Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"An error occurred in text completion: {e}")

def generate_image():
    """
    Generate an image using DALL-E.
    """
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt="A futuristic cityscape with flying cars",
            n=1,  # Number of images to generate
            size="1024x1024"
        )
        
        # Print the URL of the generated image
        print("Generated Image URL:")
        print(response.data[0].url)
    except Exception as e:
        print(f"An error occurred in image generation: {e}")

def transcribe_audio():
    """
    Transcribe an audio file using Whisper.
    Note: Replace 'path/to/your/audio/file.mp3' with an actual audio file path.
    """
    try:
        with open("path/to/your/audio/file.mp3", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        
        print("Audio Transcription:")
        print(transcription.text)
    except Exception as e:
        print(f"An error occurred in audio transcription: {e}")


def text_to_speech(text, file_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Add .mp3 extension if not present
    if not file_path.endswith('.mp3'):
        file_path = f"{file_path}.mp3"

    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",  # Alloy has a more professional, podcast-like voice
        input=text,
        speed=1.12,  # Slightly slower for better clarity
        response_format="mp3",  # Ensure high quality audio
    )
    
    
    # Create a temporary path for the main audio
    temp_main_audio_path = f"{file_path}.mp3"
    
    # Save the main audio to the temporary path
    response.stream_to_file(temp_main_audio_path)
    return file_path


def main():
    """
    Main function to demonstrate different OpenAI API capabilities.
    """
    # Uncomment the functions you want to test
    
    # generate_text_completion()
    # generate_image()  # Requires DALL-E access
    # transcribe_audio()  # Requires an audio file
    # text_to_speech("Hello, how are you?", "test.mp3")

if __name__ == "__main__":    
    main()