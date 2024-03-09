var buttons = document.querySelectorAll('.button-section button');

buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        // Remove the 'selected' class from all buttons
        buttons.forEach(function(btn) {
            btn.classList.remove('selected');
        });

        // Add the 'selected' class to the clicked button
        this.classList.add('selected');
    });
});

document.getElementById('uploadImage').addEventListener('click', function() {
    // Show the upload section
    document.getElementById('upload-section').style.display = 'block';

    // Hide the AI section
    document.getElementById('AI-section').style.display = 'none';
});

document.getElementById('aiTool').addEventListener('click', function() {
    // Hide the upload section
    document.getElementById('upload-section').style.display = 'none';
    document.getElementById('displayImage').style.display = 'none';
    document.getElementById('details-section').style.display = 'none';

    // Show the AI section
    document.getElementById('AI-section').style.display = 'block';
});