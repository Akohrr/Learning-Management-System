var count = 5;
setInterval(function(){
    count--;
    document.getElementById('countDown').innerHTML = count;
    if (count == 0) {
        window.location = '/'; 
    }
},1000);('Redirect()', 5000); 