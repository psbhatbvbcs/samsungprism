# Content Summarization

![Screenshot from 2024-03-02 01-08-22](https://media.github.ecodesamsung.com/user/26811/files/00daee46-6ed5-4c9d-8716-d78182efb909)

## About
An extension with a interactive user-interface which aims to help users in getting a concise and factually accurate summary of content from various usecases. The extension at completion will include features like: YouTube Comments Tone Analysis, YouTube Subtitles/Transcript Analysis, News Article Summary, and a E-Commerce product summarizer.
Currently the extension at this version has the YouTube Subtitles/Transcript Analysis integrated into it.


## 🖥 - High Level Design

### [_I_] Extension - Frontend
* The extension was built after going through the official documentation from the Chrome resources.
   Link: https://developer.chrome.com/docs/extensions
   
* The extension has a default popup page which gives an overview of the extension. This page is visible in non-compatible websites outside of the usecase.
* It automatically redirects to a different interface as soon as it detects a compatible website (Youtube video as of this version) through the url of the active tab.
* Here, the user is provided with the details of the current video along with a "Generate Summary".
* The extension is made responsive along with appropriate styling.
* It is built with HTML, CSS and Vanilla Javascript.

### [_II_] Extension - Script
* As soon as the user clicks on the "Generate Summary" button, the Javascript code makes an API call with the ID of the video as a payload to the python backend which processes the summary of the transcript of the video.
* On receivingg a successfull response back from the Python backend, the script displays the lines of summary on the extension along with buttons, which help in jumping to that part of the video most suitable for the summary line.

### [_III_] Python Backend - Server
* The python backend's job is to scrape, process the transcripts and then generate a summary out of it.
* The python sends back the generated summary as the API calls response.

## 🛠️ - Low Level Design

### [_I_] Python Backend - Server
* The library used to scrape the subtitles/transcripts of a YouTube video is the `youtube_transcript_api`
* The extracted transcripts are obtained as an Array of Objects/Dictionary which has 3 parameters: `text`, `start`, `duration`.
* Then they are processed and fit into a prompt.
* The current prompt provides a satisfactory output. The type of prompting technique used now is called as the `Few-Shot-Prompting Technique`.
* The combined prompt is sent to the `LLM (Gemini Pro)` which processes the summary and provides an output.
* The prompt is designed in such a way that the output format is in JSON format for easier applications accross languages (Python and Javascript)

## 🤔 - Challenges
* The current prompt and technique provides a satisfactory result, but the number of summary lines generated are many.
* Long content from articles as well as youtube transcripts should be handled successfully.
* The timestamp provided back by the LLM to jump in video according to summary, is not 100% accurate.
* `Methods tried`: Already tried calculating ROUGE score of summary line in reference to the transcript to find the most suitable timestamp for the summary line. Results not satisfactory.

## 🔭 - Further Tasks
* Implement one new feature - "Chat with any Web Page"
* Integrate all the mentioned usecases into the extensions
* Reduce the amount of summary
* Get back appropriate timestamp for the summary.

## 🕹️ - Installation Instructions
### [_I_] Python Backend - Server
>Prerequisites: Python, pip
1. Navigate to the "server" directory
2. Install the required libraries
```bash
pip install -r requirements.txt
```
3. Obtain an API key for the Gemini model from here: https://aistudio.google.com/app/u/1/apikey. Save the key as the "GOOGLE_API_KEY" in the .env file. Eg. GOOGLE_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
4. Start the Flask server
```bash
python3 server.py
```

### [_II_] Loading the extension
1. Go to the broswers extension manager page and enable developer mode
2. Click on the "Load Unpacked" button. In the folder upload window, navigate to the "extension" directory and select it.
3. Pin the extension for easier access.

_Once completing the installation and ensuring that the python backend is up and running, go to any YouTube video to test the extension!_
