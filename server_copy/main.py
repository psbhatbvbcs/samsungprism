from NewsCrunch import NewsCrunch
from ReactRadar import ReactRadar
from AnalyCC import AnalyCC
from ReviewAReview import ReviewAReview
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/healthCheck", methods=["GET"])
def healthCheck():
    return jsonify({"message": "Server is running"})


@app.route("/api/v1/articleSummary", methods=["POST"])
def articleSummary():
    try:
        data = request.get_json()
        if 'articleContent' not in data:
            return jsonify({"error": "articleContent is required"}), 400

        articleContent = data['articleContent']
        newsCrunch = NewsCrunch(articleContent)
        summary = newsCrunch.get_article_summary()

        print("Summary: ", summary)
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/ecommerceSummary", methods=["POST"])
def ecommerceSummary():
    try:
        data = request.get_json()
        if 'articleContent' not in data:
            return jsonify({"error": "articleContent is required"}), 400

        articleContent = data['articleContent']
        reviewAReview = ReviewAReview(articleContent)
        summary = reviewAReview.get_article_summary()

        print("Summary: ", summary)
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/youtubeCommentAnalysis", methods=["POST"])
def youtubeCommentAnalysis():
    try:
        data = request.get_json()
        print(data)
        if 'youtubeUrl' not in data:
            return jsonify({"error": "youtubeUrl is required"}), 400

        youtubeUrl = data['youtubeUrl']
        reactRadar = ReactRadar(youtubeUrl)
        summary = reactRadar.get_final_summary()

        print("Summary: ", summary)
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/youtubeSubtitleAnalysis", methods=["POST"])
def youtubeSubtitleAnalysis():
    try:
        data = request.get_json()
        print(data)
        if 'videoId' not in data:
            return jsonify({"error": "videoId is required"}), 400

        videoId = data['videoId']
        analyCC = AnalyCC(videoId)
        summary = analyCC.run()

        print("Summary: ", summary)
        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
