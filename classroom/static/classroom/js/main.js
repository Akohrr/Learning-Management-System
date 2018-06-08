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


    function accordionFunction(id) {
        var x = document.getElementById(id);
        if (x.className.indexOf("w3-show") == -1) {
            x.className += " w3-show";
        } else { 
            x.className = x.className.replace(" w3-show", "");
        }
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

    $("#js-close-question-modal").click( function () {
        $("#js-question-modal").hide();
    });

    $("#js-add-new-choice-btn").click( function () {
        button = $(this);
          $.ajax({
            url: button.attr("data-href"),
            type: 'get',
            dataType: 'json',
          
            success: function (data) {
              $("#js-add-new-choice-modal").show();
              $("#display-form-content").html(data.html_form);
            }
      
          });
    });
  


    $(document).on("submit","#js-new-choice-form", function (e) {
        e.preventDefault();
        form = $(this);
        form = form.append($("#token").find('input[name=csrfmiddlewaretoken]')[0]);
        $.ajax({
          url: form.attr("action"),
          type: "POST",
          data: form.serialize(),
          dataType: 'json',
          success: function (info) {
          if (info.valid) {
            $("#js-add-new-choice-modal").hide();
            location.reload();
          } else {
            input = jQuery(" <input type='hidden' name=csrfmiddlewaretoken value="+''+getCookie('csrftoken')+">");
            $("#token").append(input);
            $("#display-form-content").html(info.html_form);
          }
          }
        });
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

