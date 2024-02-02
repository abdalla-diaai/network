// listner to load page
// document.addEventListener('DOMContentLoaded', function () {
//     console.log('working?')
//     document.querySelector('#likes').onclick = () => {
//         console.log('clicked!')
//         like()
//     }
//     });


document.querySelector('#likes').addEventListener('click', function() {
    console.log('clicked!')
})



function like() {
console.log('starting')
// PUT to the resource with id = 5 to change the name of task
fetch('/allposts/', {
method: 'GET',
body: JSON.stringify({
likes: post.likes++,

}),
headers: {'Content-type': 'application/json; charset=UTF-8'}
})
.then(response => response.json())
.then(json => console.log(json))
}

