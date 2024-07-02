document.addEventListener("DOMContentLoaded", function () {
  let generateButton = document.getElementById("generateButton");
  let videoName = document.getElementById("videoName");
  let loader = document.getElementById("generateLoader");

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    let tab = tabs[0];
    if (tab && tab.url.includes("youtube.com")) {
      let url = new URL(tab.url);
      let videoId = url.searchParams.get("v");
      if (videoId) {
        getVideoTitle(tab.title);
      }
    } else {
      videoName.innerHTML =
        "<h3 style='text-align: center;'>Not a Youtube video! Please open one to use the extension!</h3>";

      generateButton.style.display = "none";
    }
  });

  function getVideoTitle(tabTitle) {
    // Regex to remove any notifications or counts
    let regex = /(?:\([0-9]+\)\s)?(.+?)\s-\sYouTube/;
    let match = regex.exec(tabTitle);
    if (match && match[1]) {
      let videoTitle = match[1];
      videoName.innerHTML = `<div style='margin-bottom: 10px; font-size: 16px; display: flex; flex-direction: column; gap='2px'><span><b>Currently Watching: </b></span><br/>${videoTitle}</div>`;
    } else {
      videoName.innerHTML = "Video title not found";
    }
  }

  generateButton.addEventListener("click", function () {
    loader.style.display = "block"; // Show loader when generating summary
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      let tab = tabs[0];
      if (tab && tab.url.includes("youtube.com")) {
        let url = new URL(tab.url);
        let videoId = url.searchParams.get("v");
        if (videoId) {
          getSummaryFromServer(videoId);
        }
      }
    });
  });
});

function getSummaryFromServer(videoId) {
  fetch("http://localhost:5000/api/v1/youtubeSubtitleAnalysis", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ videoId: videoId }),
  })
    .then((response) => response.json())
    .then((data) => {
      try {
        displaySummary(data.summary);
        hideLoader(); // Hide loader after displaying summary
      } catch (error) {
        alert("Error parsing JSON:", error);
        hideLoader(); // Hide loader on error
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      hideLoader(); // Hide loader on error
    });
}

function displaySummary(summaryData) {
  let summaryDiv = document.getElementById("summary");
  summaryDiv.innerHTML = ""; // Clear previous summary

  summaryData.forEach((item) => {
    // Create a container div for each summary row
    let row = document.createElement("div");
    row.className = "summary-row";

    // Create a rounded button for timestamp
    let button = document.createElement("button");
    button.className = "timestamp-button";
    button.innerText = `Jump to ${formatTime(Number(item.timestamp))}`;

    button.addEventListener("click", function () {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        let tab = tabs[0];
        if (tab && tab.url.includes("youtube.com")) {
          let url = new URL(tab.url);
          let videoId = url.searchParams.get("v");
          if (videoId) {
            let seekUrl = `https://www.youtube.com/watch?v=${videoId}&t=${Math.floor(
              Number(item.timestamp)
            )}s`;
            chrome.tabs.update(tab.id, { url: seekUrl });
          }
        }
      });
    });

    let divider = document.createElement("div");
    divider.className = "divider";
    divider.innerText = "|"; // Fixed divider text

    // Create a label for the summary
    let label = document.createElement("div");
    label.className = "summary-label";
    label.innerText = item.summary;

    // Append button and label to the row
    row.appendChild(button);
    row.appendChild(divider); // Add divider between button and label
    row.appendChild(label);

    // Append the row to the summary div
    summaryDiv.appendChild(row);
  });
}

// Helper function to format timestamp into minutes and seconds
function formatTime(timestamp) {
  let minutes = Math.floor(timestamp / 60);
  let seconds = Math.floor(timestamp % 60);
  return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
}

function hideLoader() {
  let loader = document.getElementById("generateLoader");
  loader.style.display = "none"; // Hide the loader
}
