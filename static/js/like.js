document.querySelectorAll('.likes').forEach(function(likeButton) {
    likeButton.addEventListener('click', function() {
        var imageId = this.dataset.id;
        fetch('/artecho/like_image/' + imageId + '/', {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                this.querySelector('span').textContent = data.likes;
            });
    });
});