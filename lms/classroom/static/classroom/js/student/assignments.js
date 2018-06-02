$('.js-answer-assignment').click( function () {
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