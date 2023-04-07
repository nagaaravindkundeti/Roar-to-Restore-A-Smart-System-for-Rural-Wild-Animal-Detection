var video = document.getElementById('video');

navigator.mediaDevices.getUserMedia({ video: true, audio: false })
	.then(function(stream) {
		video.srcObject = stream;
    // Add the "autoplay" attribute to the video element
		video.setAttribute('autoplay', true);
	})
	.catch(function(err) {
		console.log('Error: ' + err);
	});





function loadPage(page) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("box").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", page, true);
    xhttp.send();
}

