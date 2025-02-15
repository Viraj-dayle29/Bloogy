from transformers import T5Tokenizer ,T5ForConditionalGeneration
import pyttsx3
import os
from dotenv import load_dotenv

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name,legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_name)



def summarizer(input_text):
    huggingface_token = os.getenv("HUGGING_FACE_ENDPOINTS")
    # Tokenize and summarize the input text using T5
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)

    # Decode and output the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary





def text_to_speech(text, output_file):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Save speech to file
    engine.save_to_file(text, output_file)

    # Close the engine
    engine.runAndWait()

# Example usage
