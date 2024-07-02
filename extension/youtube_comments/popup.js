document.addEventListener("DOMContentLoaded", function () {
  let generateButton = document.getElementById("generateButton");
  let loader = document.getElementById("generateLoader");
  let pageName = document.getElementById("pageName");
  let errorElement = document.getElementById("error-element");

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    let tab = tabs[0];
    if (tab && tab.url.includes("youtube.com")) {
      let url = new URL(tab.url);
      let videoId = url.searchParams.get("v");
      if (videoId) {
        getVideoTitle(tab.title);
      }
    } else {
      pageName.innerHTML =
        "<h3 style='text-align: center;'>Not a Youtube video! Please open one to use the extension!</h3>";

      generateButton.style.display = "none";
    }
  });

  generateButton.addEventListener("click", function () {
    loader.style.display = "block"; // Show loader when generating summary
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      let tab = tabs[0];
      if (tab && tab.url.includes("youtube.com")) {
        let url = new URL(tab.url);
        let videoId = url.searchParams.get("v");
        if (videoId) {
          let seekUrl = `https://www.youtube.com/watch?v=${videoId}`;
          getArticleSummaryFromServer(seekUrl);
        }
      }
    });
  });
});

function getArticleSummaryFromServer(youtubeUrl) {
  fetch("http://localhost:5000/api/v1/youtubeCommentAnalysis", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ youtubeUrl }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      try {
        if (data.error) {
          throw new Error(data.error);
        }
        displaySummary(data.summary);
        hideLoader(); // Hide loader after displaying summary
      } catch (error) {
        errorElement.innerText = `Error: ${error}`;
        errorElement.style.display = "block";
        setTimeout(function () {
          errorElement.style.display = "none";
        }, 5000);
        hideLoader(); // Hide loader on error
      }
    })
    .catch((error) => {
      errorElement.innerText = `Fetch Error: ${error.message}`;
      errorElement.style.display = "block";
      setTimeout(function () {
        errorElement.style.display = "none";
      }, 5000);
      hideLoader(); // Hide loader on error
    });
}

function displaySummary(summaryData) {
  let summaryElement = document.getElementById("summary");
  // Set the HTML content to the summary element
  summaryElement.innerHTML = summaryData;
}

function hideLoader() {
  let loader = document.getElementById("generateLoader");
  loader.style.display = "none"; // Hide the loader
}
