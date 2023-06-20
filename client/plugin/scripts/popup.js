document.addEventListener('DOMContentLoaded', function() {
  var form = document.getElementById('search-form');

  form.addEventListener('submit', function(event) {
    event.preventDefault();
    var keywords = document.getElementById('keywords').value;
    var resultsCount = document.getElementById('results').value;

    searchAPI(keywords, resultsCount);
  });
});

function searchAPI(keywords, resultsCount) {
  var url = 'http://localhost:5000/search';

  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 'question':keywords, 'number_of_results':resultsCount })
  })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      displayResults(data.top_sites, data.top_context);
    })
    .catch(function(error) {
      console.error('Error:', error);
    });
}

function displayResults(top_sites, top_context) {
  var resultsContainer = document.getElementById('results-container');
  resultsContainer.innerHTML = '';

  for (var i = 0; i < top_sites.length; i++) {
    var item = top_sites[i];
    var value = top_context[i];

    var resultNumb = document.createElement('div');
    resultNumb.textContent = (i+1) + '. ';
    //, Matches: ' + value;

    var resultText = document.createElement('a');
    var createAText = document.createTextNode(item);
    resultText.setAttribute('href', item);
    resultText.appendChild(createAText);

    resultsContainer.appendChild(resultNumb).appendChild(resultText);
    //resultsContainer.appendChild(resultText);
  }
}
