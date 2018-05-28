$(document).ready(function () {


    $("#js-add-new-user-btn").click( function () {
        $.ajax({
          url: '/classroom/add/course/',
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
            url: '/classroom/add/course/',
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


    $("#soulsTable").on("click", "tbody tr ", function () {
        var row = $(this);
        rowUrl = row.attr("data-href");
        $.ajax({
          type: "get",
          url: row.attr("data-href"),
          dataType: 'json',
          success: function (data){
            $(".form-data").html(data.html_form);
            $("#js-update-soul-modal").css('display', 'block');
    
          }
        });
    
      });


});