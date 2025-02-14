# second file:

import re  # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory


class ReviewAReview():
    def __init__(self, articleContent):
        self.articleContent = articleContent
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1, safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        })

    def get_text_chunks(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=15000, chunk_overlap=500)
        chunks = text_splitter.create_documents([text])
        print("Chunks: ", chunks)
        return chunks

    def get_prompt_template(self):
        chunks_prompt = """
            You are provided the entire page of an Ecommerce product. Get the single main product details like Name, price, description (within 3 lines) and the summary of the reviews within 200 words.
            Input: `{text}`
            Summary:
        """

        map_prompt_template = PromptTemplate(
            input_variables=["text"], template=chunks_prompt)

        final_combine_prompt = """
            You are provided the entire page of an Ecommerce product. Get the single main product details like Name, price, description (within 3 lines) and the summary of the reviews within 5-6 bulleted points.
            Input: `{text}`
            Output:The summary should always be stylized and formatted with HTML tags. <ul><b>(topic name 1)</b><li>(points)</li><br/><b>(topic name 2)</b><li>(points)</li><br/> and so on.
        """

        final_prompt_template = PromptTemplate(
            input_variables=["text"], template=final_combine_prompt)

        return map_prompt_template, final_prompt_template

    def get_summary(self):
        try:
            # web_content = self.get_webpage_content()
            web_content = self.articleContent
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

    def get_article_summary(self):
        summary = self.get_summary()
        return summary
