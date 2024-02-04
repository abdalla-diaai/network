
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function(event) {
            event.preventDefault()
            var postId =  button.getAttribute('data-id');
            console.log(postId)
            var currentLikes = parseInt(document.querySelector('#current-likes').innerHTML);
    
            fetch(`/like/${postId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    likes: currentLikes + 1
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                // Handle the response as needed
                console.log(response);
            })
            .catch(error => {
                // Handle errors
                console.error('Error:', error);
            });
        }
    })
});

