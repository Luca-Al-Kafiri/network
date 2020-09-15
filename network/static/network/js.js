document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('#edit').forEach(function(a){
        a.onclick = function(){
            document.querySelector(`#post${a.dataset.post}`).style.display = 'none';
            document.querySelector(`#hide${a.dataset.post}`).style.display = 'none';
            document.querySelector(`#edit${a.dataset.post}`).style.display = 'block';
            let form = document.querySelector(`#form${a.dataset.post}`);
            form.onsubmit = function(event){
            event.preventDefault(); 
            let new_post = document.querySelector(`#content${a.dataset.post}`).value;
            fetch(`/`, {
            method: 'PUT',
            body: JSON.stringify({
            post: new_post,
            id: a.dataset.post,
           })
        })
            .then((response) => response.json())
            .then((result) => {
                document.querySelector(`#hide${a.dataset.post}`).style.display = 'block';
                document.querySelector(`#post${a.dataset.post}`).style.display = 'block';
                document.querySelector(`#edit${a.dataset.post}`).style.display = 'none';
                document.querySelector(`#content2${a.dataset.post}`).innerHTML = result['content'];
            })
        }}
    })
    });
