function showInputLink(){
    let input = document.getElementById('inputLink');
    input.style.display = input.style.display == 'none' ? 'block' : 'none';
}

/* redirecciona al evento desde link */
function goEvent(){
    let link = document.getElementById('event_link').value;

    if (link != null && link.length > 0){
        window.location = link.substring(0,link.length-1);
    } else {
        alert("Url invalida");
    }
}