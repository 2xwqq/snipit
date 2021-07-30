

function snipit(callback) {
    chrome.extension.sendMessage({name: 'screenshot'}, function(response) {
        var data = response.screenshotUrl;
        var canvas = document.createElement('canvas');
        var img = new Image();
        img.onload = function() {
            canvas.width = 1920;
            canvas.height = 1080;
            canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);

            canvas.toBlob((blob) => {           
                var fd = new FormData();
                fd.append('file', blob, Date.now() + '.png');

                var xhr = new XMLHttpRequest();  // Ajax
                xhr.open('POST', 'http://127.0.0.1:5000/v1/upload');
                xhr.send(fd);
            })
        }
        img.src = data;
    });
}


document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("snap").onclick = snipit;
})
