chrome.runtime.onInstalled.addListener(() => {
  chrome.action.onClicked.addListener(async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (tab && tab.url && tab.url.startsWith('http')) {
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['scripts/content.js']
      });
    }
  });
});
