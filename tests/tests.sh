curl --header "Content-Type: application/json"   --request POST   --data '{"text":"Hello World","site":"https://www.google.com"}' http://localhost:5000/update
curl --header "Content-Type: application/json"   --request POST   --data '{"question":"Hello World","number_of_results":2}' http://localhost:5000/search

