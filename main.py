from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googletrans import Translator
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd
import numpy as np
import requests
import os

from config import channel_list
from channel_functions import get_channel_ids, get_channel_stats, get_all_videos, get_video_details
from translator import translate

_ = load_dotenv()

from together_llm import ask_llm_to_extract_keywords



def flatten(lol):
	l = []
	for ll in lol:
		l += ll
	return l

def main():

	# print("Getting Channel IDs")

	# youtube = build('youtube', 'v3', developerKey=os.environ['api_key'])
	# channel_id_dict = get_channel_ids(youtube, channel_list)

	# print("Channel stats to Dataframe")

	# channel_stats_df = pd.DataFrame(get_channel_stats(youtube, list(channel_id_dict.values())))

	# print("Getting all videos in channels")

	# all_video_list = get_all_videos(youtube, list(channel_stats_df['Channel_playlist']))

	# # Eliminate the videos already processed in a previous timestamp

	# print("Getting video details")

	# main_database = get_video_details(youtube, flatten(all_video_list)[:10])

	# all_descriptions = main_database['descriptions']

	# print("Translating")
	# all_translated_descriptions = translate(all_descriptions, 10)

	# # for i in range(10):
	# # 	print(all_descriptions[i])
	# # 	print(all_translated_descriptions[i])

	# # 	print('=' * 25)
	# main_database['translated'] = all_translated_descriptions

	# pd.DataFrame.from_dict(main_database).to_csv("main_database_11th_Dec.csv")


	## PHASE 2
	main_database = pd.read_csv("main_database_11th_Dec.csv", index_col=[0])
	for row_id, values in main_database.iterrows():
		document = values['translated']
		keywords_in_video = ask_llm_to_extract_keywords(document)
		# row_id == video_id
		# values['publish_date']
		# 	-> push to SQL
		print(keywords_in_video)
		print("=" * 25)

if __name__ == '__main__':
	main()
