from googletrans import Translator

def detect_and_translate(text):
    translator = Translator()
    detected_lang = translator.detect(text).lang
    translated_text = translator.translate(text, dest='en').text
    return detected_lang, translated_text


detect_and_translate("Hola, ¿cómo estás?")