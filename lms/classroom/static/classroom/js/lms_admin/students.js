$(document).ready(function () {


    $("#js-add-new-user-btn").click( function () {
        $.ajax({
          url: '/classroom/add/student/',
          type: 'get',
          dataType: 'json',
        
          success: function (data) {
            $("#js-add-new-user-modal").show();
            $("#display-form-content").html(data.html_form);
          }
    
        });
      });

      
    $(document).on("submit","#js-new-user-form", function (e) {
        e.preventDefault();
        form = $(this);
        form = form.append($("#token").find('input[name=csrfmiddlewaretoken]')[0]);
        $.ajax({
            url: '/classroom/add/student/',
            type: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken)')},
            data: form.serialize(),
            dataType: 'json',
            success: function (info) {
            if (info.valid) {
                $("#js-add-new-user-modal").hide();
                location.reload();
            }
            else {
                input = jQuery(" <input type='hidden' name=csrfmiddlewaretoken value="+''+getCookie('csrftoken')+">");
                $("#token").append(input);
                $("#display-form-content").html(info.html_form);
            }
            }
        });
    });

});