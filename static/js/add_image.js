document.getElementById('imageInput').addEventListener('change', function() {
    const reader = new FileReader();
    reader.onload = function(e) {
        const displayImage = document.getElementById('displayImage');
        displayImage.src = e.target.result;
        displayImage.style.display = 'block';
        document.getElementById('details-section').style.display = 'flex';
    };
    reader.readAsDataURL(this.files[0]);
});
