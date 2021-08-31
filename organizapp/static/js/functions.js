function showInputLink(){
    var x = document.getElementById('inputLink');
    if (x.style.display == 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}

/* redirecciona al evento desde link */
function goEvent(){
    var x = document.getElementById('event_link').value;
    window.location = x;
}