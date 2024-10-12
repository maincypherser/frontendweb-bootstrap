document.getElementById('proceed').addEventListener('click', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.tabs.update(tabs[0].id, { url: tabs[0].url });
  });
});
