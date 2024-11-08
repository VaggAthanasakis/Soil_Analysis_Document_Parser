from deep_translator import GoogleTranslator
from langdetect import detect


class Translator:
    def __init__(self) -> None:
        pass

    # function to split text into segments of max_length length
    def split_text(self,text, max_length=2000):
        segments = []
        while len(text) > max_length:
            # Find the last space within the 5000 character limit to avoid splitting words
            split_index = text[:max_length].rfind(' ')
            segments.append(text[:split_index])
            text = text[split_index + 1:]
        segments.append(text)  # Add any remaining text as the last segment
        return segments

    # Function that translates each chunk from greek to english
    def translate_text_in_chunks(self,text,source_lang='auto', target_lang='en'):
        segments = self.split_text(text)
        translated_segments = []

        for segment in segments:
            translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(segment)
            translated_segments.append(translated_text)

        # Join all translated segments into a single text
        return ' '.join(translated_segments)


    # function to translate the input of the LLM in English In order to achieve betterc accuracy
    def text_translator(self,input_text):

        # Check if the text is not in english
        if (detect(input_text) != 'en'):
            translated_text = self.translate_text_in_chunks(input_text)
            return translated_text
        
        return input_text


        