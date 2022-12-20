from rest_framework.response import Response
from rest_framework.views import APIView
from ttsApp.serializers import TTSSerializer
from django.http import HttpResponse, FileResponse
from gtts import gTTS
import pyttsx3
import os

# Create your views here.
class TTSView(APIView):
    serializerClass = TTSSerializer

    def post(self, request):
        # Get the text to synthesize from the request
        serializer = self.serializerClass(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['text']

        engine = pyttsx3.init()

        # Set the voice to a female Hindi voice
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        # Set the language to Hindi
        engine.setProperty('language', 'hi')

        # engine.setProperty('volume', 1.0)  # setting up volume level  between 0 and 1
        #
        engine.setProperty('rate', 125)  # setting up new voice rate

        engine.say(text)

        temp_file = "tts-temp.mp3"
        engine.save_to_file(text, temp_file)
        engine.runAndWait()

        try:
            with open(temp_file, 'rb') as f:
                audio_data = f.read()
        except FileNotFoundError:
            return Response({"error": "Unable to read audio file"}, status=500)

        try:
            os.remove(temp_file)
        except OSError:
            pass  # the file does not exist, so we can ignore the error

        response = HttpResponse(audio_data, content_type='audio/mpeg')
        return response


class GTTSView(APIView):
    def post(self, request):
        text = request.data.get('text')
        language = request.data.get('language', 'hi')

        # Create the audio file
        audio = gTTS(text=text, lang=language)
        audio.save('audio.mp3')

        # Return the audio file in the response
        file = open('audio.mp3', 'rb')
        return FileResponse(file, content_type='audio/mpeg')
