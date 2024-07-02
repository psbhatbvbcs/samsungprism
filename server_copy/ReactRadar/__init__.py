import streamlit as st
from urllib.parse import parse_qs, urlparse  # type: ignore
import google.generativeai as palm
from googleapiclient.discovery import build
import pandas as pd
import re  # type: ignore
import random  # type: ignore
from rouge_score import rouge_scorer
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Set your YouTube API key and Google API key
YOUTUBE_API_KEY = "AIzaSyDVKROa2PHT7JrXg_bMqZ1-7HNCnxpqsZ8"

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


class ReactRadar():
    def __init__(self, video_url):
        self.video_url = video_url
        self.text_content = ""
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1, safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        })

    def get_text_chunks(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=15000, chunk_overlap=500)
        chunks = text_splitter.create_documents([text])
        return chunks

    def get_prompt_template(self):
        chunks_prompt = """
            Below is the comments from a youtube video. Perform sentiment analysis and find out what the users think about the video. Give your output strictly within 200 words in the form of summary.
            Input: `{text}`
            Summary:
        """

        map_prompt_template = PromptTemplate(
            input_variables=["text"], template=chunks_prompt)

        final_combine_prompt = """
            Below is the comments from a youtube video. Perform sentiment analysis and find out what the users think about the video. Give your output strictly within 200 words in the form of summary.
            Input: `{text}`
            Output:The summary should always be stylized and formatted with HTML tags. <ul><b>Overall User Reaction:</b><li>(sentence)</li> and so on.
        """

        final_prompt_template = PromptTemplate(
            input_variables=["text"], template=final_combine_prompt)

        return map_prompt_template, final_prompt_template

    def get_summary(self):
        try:
            # web_content = self.get_webpage_content()
            web_content = self.text_content
            web_content = re.sub(r'[\n\t\r]', '', web_content)
            print("Web Content: ", web_content)
            text_chunks = self.get_text_chunks(web_content)
            map_prompt_template, final_prompt_template = self.get_prompt_template()

            chain = load_summarize_chain(
                llm=self.llm,
                chain_type="map_reduce",
                map_prompt=map_prompt_template,
                combine_prompt=final_prompt_template,
                verbose=False,
            )

            summary = chain.invoke(text_chunks)
            # print("Summary: ", summary["output_text"])

            return summary["output_text"]

        except Exception as e:
            return str(e)

    def get_video_description(self, video_id):
        video_data = youtube.videos().list(part="snippet", id=video_id).execute()
        print("Video Data:", video_data)
        if "items" in video_data and video_data["items"]:
            return video_data["items"][0]["snippet"]["description"]
        else:
            return ""

    def get_video_id_from_url(self):
        print("Video URL:", self.video_url)

        parsed_url = urlparse(self.video_url)
        print("Parsed URL:", parsed_url)
        video_id = parse_qs(parsed_url.query).get("v")
        print("Video ID:", video_id)
        return video_id[0] if video_id else None

    def scrape_all_with_replies(self):
        try:
            video_id = self.get_video_id_from_url()
            print("Video ID:", video_id)
            if not video_id:
                return "Invalid YouTube Video URL. Please provide a valid URL."

            data = (
                youtube.commentThreads()
                .list(
                    part="snippet", videoId=video_id, maxResults=100, textFormat="plainText"
                )
                .execute()
            )
            # print("Data:", data)

            comments_to_concatenate = []

            for i in data["items"]:
                comment = i["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

                comments_to_concatenate.append(comment)

                TotalReplyCount = i["snippet"]["totalReplyCount"]

                if TotalReplyCount > 0:
                    parent = i["snippet"]["topLevelComment"]["id"]

                    data2 = (
                        youtube.comments()
                        .list(
                            part="snippet",
                            maxResults=100,
                            parentId=parent,
                            textFormat="plainText",
                        )
                        .execute()
                    )

                    for i in data2["items"]:
                        comment = i["snippet"]["textDisplay"]
                        comments_to_concatenate.append(comment)

            # print("Comments to concatenate:", comments_to_concatenate)
            selected_comments = random.sample(
                comments_to_concatenate, min(20, len(comments_to_concatenate))
            )

            # print("Selected Comments:", selected_comments)

            concatenated_comments = " ".join(selected_comments)

            self.text_content = concatenated_comments

            generated_summary = self.get_summary()
            return generated_summary

        except Exception as e:
            return str(e)

    def get_final_summary(self):
        print(f"URL: {self.video_url}")
        generated_summary = self.scrape_all_with_replies()
        return generated_summary
