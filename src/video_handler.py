from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


class YouTubeVideoHandler:
    def get_video_id(self, url):
        query = urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            return parse_qs(query.query).get('v', [None])[0]
        return None

    def fetch_transcript(self, video_id):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=['fr']
            )
            full_text = " ".join([entry['text'] for entry in transcript])
            return full_text
        except Exception as e:
            raise Exception(f"Transcript fetch failed: {e}")