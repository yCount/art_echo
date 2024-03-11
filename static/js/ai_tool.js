var buttons = document.querySelectorAll('.button-section button');

buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        buttons.forEach(function(btn) {
            btn.classList.remove('selected');
        });

        this.classList.add('selected');
    });
});

document.getElementById('uploadImage').addEventListener('click', function() {
    
    document.getElementById('upload-section').style.display = 'block';

    document.getElementById('AI-section').style.display = 'none';
});

document.getElementById('aiTool').addEventListener('click', function() {
    document.getElementById('upload-section').style.display = 'none';
    document.getElementById('displayImage').style.display = 'none';
    document.getElementById('details-section').style.display = 'none';
    document.getElementById('AI-section').style.display = 'block';
});