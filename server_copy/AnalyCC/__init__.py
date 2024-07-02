import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import json
# second file:

import re  # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory


class AnalyCC:
    def __init__(self, videoId):
        self.videoId = videoId
        self.GOOGLE_API_KEY = "AIzaSyDxp5B2tqKHGOWjI0rp8pL1eyzJMiIdVac"
        genai.configure(api_key="AIzaSyA52Gz9Ni5Jw9dWFY6wGjj0lmWnJQQXBxM")
        self.generation_config = {
            "temperature": 0.2,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 5000,
        }
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ]
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config =self.generation_config,
            safety_settings = self.safety_settings,
            system_instruction=" You are a youtube video transcript organiser bot. You are provided with these objectives and examples.\n        Your job is to first analyse all objectives and then generate the solution step-by-step. You can use the examples as a reference for the output format. The objectives and output format are to be followed strictly.\n        OBJECTIVES:\n        1. Given the input, the initial part consists of subtitles of a youtube video extracted from Youtube Transcript Api. The second part consists of the timestamps at which subtitles above appear in the video. The time timestamps are in the format of \"seconds.milliseconds\". Analyse it.\n        2. Generate the summary of all the given subtitles whitin 6 lines. You can go beyond the number of lines in the example.\n        3. Provide the summary from only the given input. No creativity is encouraged. Summary of all the input to be provided within 6 concise points.\n        4. In the summary, no usage of proper nouns like individual names are allowed, instead mention them with the word 'Speaker'.\n        5. Remember the initial timestamp of the subtitle from where a particular summary was started.\n        6. Now give the output in JSON format where the keys are the remembered timestamps from above and the values are the summary lines corresponding to it.\n\n        Example Input 1:\n        '''\n        Transcript:\n        and superhero get superhero outfits and\n        you liked yours\n        oh man yes yes I did oh thank you for it\n        more than you were meant to didn't you\n        did they offer you other clothes mm-hmm\n        yeah well let me ask you something if\n        they offered you that would you ever\n        take no I would never take it off yes I\n        but I fly generally anyway yeah yeah\n        monk if someone else is got a new suit\n        spider-man it's got a new suit oh yes\n        but you really like the suit right\n        I do yes because I can go to the\n        bathroom in it mainly you watch I Man 1\n        Robert wore the full suit and then if\n        you watch Iron Man 2 he wore like\n\n        Timestamps:\n        0.0 - 2.25 - 3.419 - 6.33 - 12.86 - 15.63 - 20.13 - 21.24 - 25.71 - 30.81 - 32.489 - 35.219 - 37.53 - 40.71 - 44.719 - 47.399 -\n        '''\n\n        Example Output 1:\n        '''{\"0.0\": \"Superhero outfits are discussed.\",\"32.489\": \"The speaker expresses his liking for his superhero outfit.\",\"40.71\": \"Iron Man's suits are being discussed\"}'''\n\n        Explaination for the timestamps in Example output 1: Compare the original input for finding appropriate timestamps for summary lines. They accurately match the context of the transcript.\n\n        ---------------\n        Example Input 2:\n        '''\n        Transcript:\n        your question uh do we have multiple\n        options answer is\n        yes uh is that a problem why should it\n        be a problem if I'm smart enough to have\n        multiple options you should be admiring\n        me you know you shouldn't be\n        criticizing now is is that a problem for\n        other\n        [Music]\n        people\n        [Music]\n        multiple choice mindset is would that be\n        would that be right um from\n        non-alignment to I think you may have\n        called it or somebody else called it all\n        alignment so you can pick and choose\n        alliances but you can also pick and\n        choose topics on Russia for example you\n        still buy Uh Russian oil uh is that is\n        that okay with your uh counterpart from\n        the US everything is your your\n\n        Timestamps:\n        0.24 - 2.72 - 4.16 - 7.279 - 9.28 - 11.599 - 13.759 - 17.68 - 18.91 - 28.96 - 37.26 - 42.44 - 46.039 - 48.96 - 51.48 - 53.719 - 56.6 - 58.519 - 61.8 - 66.56 - 70.439 -\n        '''\n\n        Example Output 1:\n        '''{\"0.0\": \"The speaker defends having multiple options as a sign of intelligence, suggesting admiration instead of criticism.\",\"42.44\": \"Mention of shifting from non-alignment to 'all alignment', where countries can pick and choose alliances and topics.\",\"58.519\": \"Reference to buying Russian oil and questioning if it's acceptable to counterparts from the US.\",\"66.56\": \"The speaker's statement ends with a question about everything belonging to \"your counterpart from the US.\"}'''\n\n        Explaination for the timestamps in Example output 2: Compare the original input for finding appropriate timestamps for summary lines. They accurately match the context of the transcript.\n",
            )

    def generate_prompt(self, transcript):
        # prompt = """
        # You are a youtube video transcript organiser bot. You are provided with these objectives and examples.
        # Your job is to first analyse all objectives and then generate the solution step-by-step. You can use the examples as a reference for the output format. The objectives and output format are to be followed strictly.
        # OBJECTIVES:
        # 1. Given the input, the initial part consists of subtitles of a youtube video extracted from Youtube Transcript Api. The second part consists of the timestamps at which subtitles above appear in the video. The time timestamps are in the format of "seconds.milliseconds". Analyse it.
        # 2. Generate the summary of all the given subtitles whitin 6 lines. You can go beyond the number of lines in the example.
        # 3. Provide the summary from only the given input. No creativity is encouraged. Summary of all the input to be provided within 6 concise points.
        # 4. In the summary, no usage of proper nouns like individual names are allowed, instead mention them with the word 'Speaker'.
        # 5. Remember the initial timestamp of the subtitle from where a particular summary was started.
        # 6. Now give the output in JSON format where the keys are the remembered timestamps from above and the values are the summary lines corresponding to it.

        # Example Input 1:
        # '''
        # Transcript:
        # and superhero get superhero outfits and
        # you liked yours
        # oh man yes yes I did oh thank you for it
        # more than you were meant to didn't you
        # did they offer you other clothes mm-hmm
        # yeah well let me ask you something if
        # they offered you that would you ever
        # take no I would never take it off yes I
        # but I fly generally anyway yeah yeah
        # monk if someone else is got a new suit
        # spider-man it's got a new suit oh yes
        # but you really like the suit right
        # I do yes because I can go to the
        # bathroom in it mainly you watch I Man 1
        # Robert wore the full suit and then if
        # you watch Iron Man 2 he wore like

        # Timestamps:
        # 0.0 - 2.25 - 3.419 - 6.33 - 12.86 - 15.63 - 20.13 - 21.24 - 25.71 - 30.81 - 32.489 - 35.219 - 37.53 - 40.71 - 44.719 - 47.399 -
        # '''

        # Example Output 1:
        # '''{"0.0": "Superhero outfits are discussed.","32.489": "The speaker expresses his liking for his superhero outfit.","40.71": "Iron Man's suits are being discussed"}'''

        # Explaination for the timestamps in Example output 1: Compare the original input for finding appropriate timestamps for summary lines. They accurately match the context of the transcript.

        # ---------------
        # Example Input 2:
        # '''
        # Transcript:
        # your question uh do we have multiple
        # options answer is
        # yes uh is that a problem why should it
        # be a problem if I'm smart enough to have
        # multiple options you should be admiring
        # me you know you shouldn't be
        # criticizing now is is that a problem for
        # other
        # [Music]
        # people
        # [Music]
        # multiple choice mindset is would that be
        # would that be right um from
        # non-alignment to I think you may have
        # called it or somebody else called it all
        # alignment so you can pick and choose
        # alliances but you can also pick and
        # choose topics on Russia for example you
        # still buy Uh Russian oil uh is that is
        # that okay with your uh counterpart from
        # the US everything is your your

        # Timestamps:
        # 0.24 - 2.72 - 4.16 - 7.279 - 9.28 - 11.599 - 13.759 - 17.68 - 18.91 - 28.96 - 37.26 - 42.44 - 46.039 - 48.96 - 51.48 - 53.719 - 56.6 - 58.519 - 61.8 - 66.56 - 70.439 -
        # '''

        # Example Output 1:
        # '''{"0.0": "The speaker defends having multiple options as a sign of intelligence, suggesting admiration instead of criticism.","42.44": "Mention of shifting from non-alignment to 'all alignment', where countries can pick and choose alliances and topics.","58.519": "Reference to buying Russian oil and questioning if it's acceptable to counterparts from the US.","66.56": "The speaker's statement ends with a question about everything belonging to "your counterpart from the US."}'''

        # Explaination for the timestamps in Example output 2: Compare the original input for finding appropriate timestamps for summary lines. They accurately match the context of the transcript.

        # Now Your Input to process is:

        # """
        # in JSON FORMAT, each keyed with timestamps for appropriate watching. Important: Do not deviate from the input. No creative context addition will be tolerated\n\n"

        # print(transcript)
        prompt = "\nTranscript:\n"  # Add transcript header
        for i, line in enumerate(transcript):
            prompt += f"{line['text']}\n"

        prompt += "\nTimestamps:\n"
        for i, line in enumerate(transcript):
            prompt += f"{line['start']} - "

        prompt += "\nYour Output as answer:\n"  # Add empty line

        return prompt

    def generate_summary_with_ai(self, transcript):
        try:
            prompt = self.generate_prompt(transcript)
            summaryGenerator = self
            summaryGenerator.GenerateSummary(prompt)
            summaries = summaryGenerator.generated_summary

            data_obj = json.loads(summaries)

            # Create new dictionary with timestamp and summary
            new_dict = [{"timestamp": timestamp.strip(), "summary": summary}
                        for timestamp, summary in data_obj.items()]

            return new_dict

        except Exception as e:
            return [{'error': str(e)}]

    def GenerateSummary(self, prompt):
        prompt_parts = [
            prompt
        ]
        
        chat_session = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": prompt_parts,
                }
            ],
        )
        responses = chat_session.send_message("Give output", stream=True)
        responses.resolve()
        
        all_responses = [
                part.text for response in responses for part in response.parts if hasattr(part, 'text')]
        answer = " ".join(all_responses).replace("```json", "", 1).replace("\n```", "", 1)
        answer = " ".join(all_responses).replace("``` json", "", 1).replace("\n```", "", 1)
        
        print("ANS: ", answer)
        self.generated_summary = answer

    def generate_summary(self):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(self.videoId, languages=['en', 'en-US', 'hi'])
            # Process transcript and extract timestamps
            # Format: [{'text': 'Subtitle text', 'start': 10.0, 'duration': 3.0}, ...]

            # Generate summary using AI model
            summary = self.generate_summary_with_ai(transcript)

            return summary
        except Exception as e:
            return str(e)

    def run(self):
        summary = self.generate_summary()
        return summary
