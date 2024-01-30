from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
import os

def fetch_youtube_transcript(url):
    """
    This tool can be used to retrieve a transcript from a YouTube video url. It will then write a creative blog post summarizing
    the video.

    This can ONLY interact with youtube URLs. Other URLs cannot use this tool.

    Args:
    url (str): A user provided YouTube url in quotes. ex: 'https://www.youtube.com/randomchannelname'

    Returns:
    string: The answer to the user's query in markdown format.
    """
    # Extracting video ID from URL
    video_id = url.split("watch?v=")[1].split("&")[0]

    try:
        # Fetching the transcript
        print(f'Grabbing transcript from {url}')
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        print('Handing transcript to writer agent')
        llm = Ollama(
        model="mistral_long",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        base_url="http://192.168.1.234:11434"
    )
        post = llm.invoke(
            f'''
            You are a creative, intelligent content writer. You specialize in taking transcripts and using them
            to write creative, detailed, engaging blog posts about the videos they are from.

            You do not simply repeat the points in the transcript. You expand on the concepts and write the blog
            post IN YOUR OWN WORDS.

            Please write a user facing blog post using the transcript below: 
            
            {formatted_transcript}
            '''
        )
        file_path = os.path.expanduser('~/Downloads/post.md')
        with open(file_path, 'w') as file:
            file.write(f'# Post' + post + f'\n\n# Transcript:\n{formatted_transcript}')
        print('Write post.txt to your Downloads folder')
        return
    except NoTranscriptFound:
        return "No transcript found for this video."