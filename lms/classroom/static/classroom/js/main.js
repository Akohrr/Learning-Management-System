    // using jQuery to obtain csrf tokens from cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    function openStatus(evt, statusName) {
        var i, x, tablinks;
        x = document.getElementsByClassName("status");
        for (i = 0; i < x.length; i++) {
            x[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablink");
        for (i = 0; i < x.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" w3-teal", "");
        }
        document.getElementById(statusName).style.display = "block";
        evt.currentTarget.className += " w3-teal";
    }


    $("#js-close-new-choice-modal").click( function () {
        $("#js-add-new-choice-modal").hide();
    });


      
$(document).ready(function () {
    $('table.w3-table').DataTable({
        language: {
            emptyTable: "", // 
            loadingRecords: "Please wait .. ", // default Loading...
            zeroRecords: ""
        }
    });
});

