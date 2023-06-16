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

    var resultElement = document.createElement('div');
    resultElement.textContent = 'Site: ' + item;
    //, Matches: ' + value;

    resultsContainer.appendChild(resultElement);
  }
}
