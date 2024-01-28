function updateLikes(post_id) {
    fetch(`/allposts/${post_id}`)
        .then(response => response.json())
        .then(data => {
            data = JSON.parse(JSON.stringify(data));
            document.querySelector('.likes').textContent(data.likes)}
        )}