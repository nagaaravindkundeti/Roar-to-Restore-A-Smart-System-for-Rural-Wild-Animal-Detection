$(document).ready(function() {
			// Define a function to retrieve the counts for each detected class
			function updateHandCount() {
            fetch('/hand_count')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('hand-count').textContent = data.hand_count;
                })
                .catch(error => console.error(error));
        }

        setInterval(updateHandCount, 1000);

		});

