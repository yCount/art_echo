var buttons = document.querySelectorAll('.button-section button');

buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        buttons.forEach(function(btn) {
            btn.classList.remove('selected');
        });

        this.classList.add('selected');
    });
});

document.getElementById('user-btn').addEventListener('click', function() {
    document.getElementById('user-results').style.display = 'block';
    document.getElementById('category-results').style.display = 'none';
    document.getElementById('title-results').style.display = 'none';
});

document.getElementById('cat-btn').addEventListener('click', function() {
    document.getElementById('user-results').style.display = 'none';
    document.getElementById('category-results').style.display = 'block';
    document.getElementById('title-results').style.display = 'none';
});

document.getElementById('title-btn').addEventListener('click', function() {
    document.getElementById('user-results').style.display = 'none';
    document.getElementById('title-results').style.display = 'block';
    document.getElementById('category-results').style.display = 'none';
});