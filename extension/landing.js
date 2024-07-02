// landing.js

// Get the current URL
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  let youtubeCommentButton = document.getElementById("youtube-comment-button");
  let youtubeSubtitleButton = document.getElementById(
    "youtube-subtitle-button"
  );
  let articleSummaryButton = document.getElementById("article-summary-button");
  let ecommerceSummaryButton = document.getElementById(
    "ecommerce-summary-button"
  );

  let errorElement = document.getElementById("error-element");

  var url = tabs[0].url;

  youtubeCommentButton.addEventListener("click", function () {
    if (url.includes("youtube.com")) {
      window.location.href = "./youtube_comments/popup.html";
    } else {
      errorElement.innerText =
        "Please open a YouTube video to use this feature.";
      errorElement.style.display = "block";
      setTimeout(function () {
        errorElement.style.display = "none";
      }, 5000);
    }
  });

  youtubeSubtitleButton.addEventListener("click", function () {
    if (url.includes("youtube.com")) {
      window.location.href = "./youtube_subtitles/popup.html";
    } else {
      errorElement.innerText =
        "Please open a YouTube video to use this feature.";
      errorElement.style.display = "block";
      setTimeout(function () {
        errorElement.style.display = "none";
      }, 5000);
    }
  });

  articleSummaryButton.addEventListener("click", function () {
    if (url.includes("https://")) {
      window.location.href = "./article_summary/popup.html";
    } else {
      errorElement.innerText = "Please open an article to use this feature.";
      errorElement.style.display = "block";
      setTimeout(function () {
        errorElement.style.display = "none";
      }, 5000);
    }
  });

  ecommerceSummaryButton.addEventListener("click", function () {
    if (url.includes("https://")) {
      window.location.href = "./ecommerce_summary/popup.html";
    } else {
      errorElement.innerText =
        "Please open an e-commerce site to use this feature.";
      errorElement.style.display = "block";
      setTimeout(function () {
        errorElement.style.display = "none";
      }, 5000);
    }
  });
});
