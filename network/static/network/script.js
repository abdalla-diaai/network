// Edit post function
$('.post-edit').on("click", function () {

    var editId = $(this).attr("data-edit");
    fetch(`/edit/${editId}`, {
        method: 'PUT',
        body:
            JSON.stringify({
                body: $(`#post-body-${editId}`).val(),
            }),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        // Check if the response status is ok (2xx)
        if (response.ok) {
            // Parse the JSON response
            return response.json();
        } else {
            // Handle error responses
            console.error('Error:', response.statusText);
            throw new Error('Failed to edit post');
        }
    })
    .then(responseData => {
        // Redirect to the desired URL
        console.log(responseData);
        window.location.href = '/allposts';
    })
    .catch(error => {
        // Handle errors
        console.error('Error:', error);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.edit-view').forEach(editView => {
        editView.style.display = 'none';
    });
    document.querySelectorAll('.post-view').forEach(postView => {
        postView.style.display = 'block';
    });


});


$('.like-button').on("click", function (event) {
    var likeId = $(this).attr("data-like");
    event.preventDefault();
    var currentLikes = parseInt(document.querySelector('.current-likes').innerHTML);

    fetch(`/like/${likeId}`, {
        method: 'PUT',
        body: JSON.stringify({
            likes: currentLikes + 1
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        // Check if the response status is ok (2xx)
        if (response.ok) {
            // Parse the JSON response
            return response.json();
        } else {
            // Handle error responses
            console.error('Error:', response.statusText);
            throw new Error('Failed to edit post');
        }
    })
    .then(responseData => {
        // Redirect to the desired URL
        window.location.href = '/allposts';
    })
    .catch(error => {
        // Handle errors
        console.error('Error:', error);
    });

});


// Function to show form and prepopulate field with old post
$('.edit-post').on("click", function () {
    var editId = $(this).attr("data-id");
    document.querySelector(`#edit-view-${editId}`).style.display = 'block';
    document.querySelector(`#post-view-${editId}`).style.display = 'none';
    fetch(`/edit/${editId}`)
        .then(response => response.json())
        .then(post => {
            $(`#post-body-${editId}`).text(post.body);

        })
});


