from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from tqdm import tqdm
# tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en", cache_dir="./models/")

# model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-zh-en", cache_dir="./models/")

translator_pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-zh-en", model_kwargs={'cache_dir':"./models/", 'max_length': 2048})

def translate(src_text):
	translated_text = []
	for text in tqdm(src_text):
		if len(text) > 512:
			temp_translation = ""
			for i in range(0, len(text), 512):
				temp_translation += translator_pipe(text[i: min(i + 512, len(text))])[0]['translation_text']
			translated_text.append(temp_translation)
		else:
			translated_text.append(translator_pipe(text)[0]['translation_text'])
	return translated_text

# test_string = "本影片為虛擬貨幣詐騙系列「下集」"

# print(translate([test_string]))


