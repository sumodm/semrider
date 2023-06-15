// const article = document.querySelector("article");

/*
// `document.querySelector` may return null if the selector doesn't match anything.
if (article) {
  const text = article.textContent;
  const wordMatchRegExp = /[^\s]+/g; // Regular expression
  const words = text.matchAll(wordMatchRegExp);
  // matchAll returns an iterator, convert to array to get word count
  const wordCount = [...words].length;
  const readingTime = Math.round(wordCount / 200);
  const badge = document.createElement("p");
  // Use the same styling as the publish information in an article's header
  badge.classList.add("color-secondary-text", "type--caption");
  badge.textContent = `⏱️ ${readingTime} min read`;

  // Support for API reference docs
  const heading = article.querySelector("h1");
  // Support for article docs with date
  const date = article.querySelector("time")?.parentNode;

  (date ?? heading).insertAdjacentElement("afterend", badge);

  console.log(text);
}
*/

/* Code to Walk Through DOM and get text
var queue = [document.body], curr, text_content="";
while (curr = queue.pop()) {
  //if (!curr.textContent) continue;
  for (var i = 0; i < curr.childNodes.length; ++i) {
    switch (curr.childNodes[i].nodeType) {
      case Node.ELEMENT_NODE: //1
        queue.push(curr.childNodes[i]);
        break;
      case Node.TEXT_NODE: // 3
        text_content = text_content + "  " + curr;
        break;
    }
  }
}

console.log(text_content);
*/

var docs = document.body;
var text = docs.innerText || docs.textContent;

console.log(text);
