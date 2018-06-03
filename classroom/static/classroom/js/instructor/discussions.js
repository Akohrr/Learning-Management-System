$(".js-add-comment-discussion").click( function () {
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