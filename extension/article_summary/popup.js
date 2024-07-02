document.addEventListener("DOMContentLoaded", function () {
  let generateButton = document.getElementById("generateButton");
  let loader = document.getElementById("generateLoader");
  let pageName = document.getElementById("pageName");
  let errorElement = document.getElementById("error-element");

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    let tab = tabs[0];
    if (tab && tab.url.includes("https://")) {
      pageName.innerHTML = `<div style='margin-bottom: 30px; font-size: 16px; display: flex; flex-direction: column; gap='2px'><span><b>Currently reading: </b></span><div>${tab.title}</div></div>`;
      generateButton.style.display = "block";
    }
  });

  generateButton.addEventListener("click", function () {
    loader.style.display = "block"; // Show loader when generating summary
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      let tab = tabs[0];
      if (tab && tab.url.includes("https://")) {
        chrome.scripting.executeScript(
          {
            target: { tabId: tabs[0].id },
            function: scraper,
          },
          (results) => {
            const scrapedData = results[0].result;
            getArticleSummaryFromServer(scrapedData.bodyContent);
          }
        );
      }
    });
  });
});

function scraper() {
  let body = String(document.querySelector("body")?.innerText) || "";

  return {
    bodyContent: body,
  };
}

function getArticleSummaryFromServer(articleContent) {
  fetch("http://localhost:5000/api/v1/articleSummary", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ articleContent }),
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
