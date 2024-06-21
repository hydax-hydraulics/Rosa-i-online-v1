const video = document.getElementById('webcam');
const captureBtn = document.getElementById('captureBtn');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error('Error accessing webcam:', error);
    });

captureBtn.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL('image/png');

    fetch('/capturre', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error capturing image:', error);
    });
});
