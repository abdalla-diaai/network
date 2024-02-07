// Edit post function
$('.post-edit').on("click", function (event) {
    event.preventDefault();

    var editId = $(this).attr("data-edit");
    fetch(`/edit/${editId}`, {
        method: 'PUT',
        body:
            JSON.stringify({
                body: $(`#post-body-${editId}`).val(),
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
            console.log(response);
        })
        .catch(error => {
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