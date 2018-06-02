
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
        }
        else {
          input = jQuery(" <input type='hidden' name=csrfmiddlewaretoken value="+''+getCookie('csrftoken')+">");
          $("#token").append(input);
          $("#display-form-content").html(info.html_form);
        }
        }
      });
    });


$(document).ready( function () {

    $('.js-answer-quiz').click( function () {
        row = $(this);
        $.ajax({
          url: row.attr("data-href"),
          type: 'get',
          dataType: 'json',
        
          success: function (data) {
            $("#js-add-new-choice-modal").show();
            $("#display-form-content").html(data.html_form);
          }
    
        });
    });

});
