from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from tqdm import tqdm
# tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en", cache_dir="./models/")

# model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-zh-en", cache_dir="./models/")

translator_pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-zh-en", model_kwargs={'cache_dir':"./models/", 'max_length': 2048})

def translate(src_text, batch_size=1):
	translated_text = []
	num_lines_per_text = []
	int_translations = []
	final_translations = []
	for text in src_text:
		if len(text) > 512:
			# temp_translation = ""
			num_lines = 0
			for i in range(0, len(text), 512):
				# temp_translation += translator_pipe(text[i: min(i + 512, len(text))])[0]['translation_text']
				translated_text.append(text[i: min(i + 512, len(text))])
				num_lines += 1
			# translated_text.append(temp_translation)
			num_lines_per_text.append(num_lines)
		else:
			# translated_text.append(translator_pipe(text)[0]['translation_text'])
			translated_text.append(text)
			num_lines_per_text.append(1)
	for i in tqdm(range(0, len(translated_text), batch_size)):
		trns = translator_pipe(translated_text[i: min(i + batch_size, len(translated_text))])
		# int_translations += trns[:]['translation_text']
		for ttxt in trns:
			int_translations.append(ttxt['translation_text'])
	idx = 0
	for num_lines in num_lines_per_text:
		final_translations.append(" ".join(int_translations[idx: idx + num_lines]))
		idx += num_lines
	return final_translations

# test_string = "本影片為虛擬貨幣詐騙系列「下集」"

# print(translate([test_string]))


