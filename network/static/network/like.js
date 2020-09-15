document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll('#like').forEach(a => {
       a.onclick = function(){
        let status = document.querySelector(`#like${a.dataset.post}`).innerHTML;
        fetch(`/like/${a.dataset.post}`, {
        method : "PUT",
        body : JSON.stringify({
            status : status,
            id : a.dataset.post
        })
       })
       .then((response) => response.json())
       .then (result => {
           console.log(result)
        document.querySelector(`#like${a.dataset.post}`).innerHTML = result['status'];
        document.querySelector(`#likes${a.dataset.post}`).textContent = `Likes : ${result["likes"]}`
       })
       } 
    });
})