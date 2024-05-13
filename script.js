function performSearch() {
    var query = document.getElementById('searchQuery').value;
    var url = `http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}`;
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();  
        })
        .then(data => {
            const resultsContainer = document.getElementById('results');
            resultsContainer.innerHTML = ''; 
            if (data.length > 0) {
                const list = document.createElement('ul');
                data.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = `${item.file_name} (Score: ${item.score}) - ${item.summary}`;
                    list.appendChild(li);
                });
                resultsContainer.appendChild(list);
            } else {

                resultsContainer.textContent = 'No results found.';
            }
        })
        .catch(error => {
            // If an error occurs during the fetch operation, log it to the console and display an error message.
            console.error('Error fetching data:', error);
            document.getElementById('results').textContent = 'Failed to load results.';
        });
}

// Optional: Add an event listener for the Enter key to trigger the search when pressed
document.getElementById('searchQuery').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        performSearch();
    }
});
