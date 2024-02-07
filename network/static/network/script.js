    // Edit post function
    function editPost(postId) {
        fetch(`/edit/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                body: $(`#post-body-${postId}`).val
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

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.edit-view').forEach(editView => {
        editView.style.display = 'none';
    });
    document.querySelectorAll('.post-view').forEach(postView => {
        postView.style.display = 'block';
    });

    document.querySelectorAll('button').forEach(button => {
        button.onclick = function(event) {
            event.preventDefault();
            var postId = button.getAttribute('data-id');
            var currentLikes = parseInt(document.querySelector('.current-likes').innerHTML);

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
                console.log(response);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    var postId;
    // Function to show form and prepopulate field with old post
    $("button").on("click", function () {
        postId = $(this).attr("data-id");
        document.querySelector(`#edit-view-${postId}`).style.display = 'block';
        document.querySelector(`#post-view-${postId}`).style.display = 'none';
        fetch(`/edit/${postId}`)
            .then(response => response.json())
            .then(post => {
                $(`#post-body-${postId}`).text(post.body);
            });
    });



    // Event binding for edit form
    $(`#edit-form${postId}`).on("submit", function (event) {
        event.preventDefault();
        editPost(postId);
    });
});
