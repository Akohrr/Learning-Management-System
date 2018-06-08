$('.js-answer-assignment').click( function () {
    row = $(this);
    $.ajax({
      url: row.attr("data-href"),
      type: 'get',
      dataType: 'json',
    
      success: function (data) {
        $("#js-question-modal").show();
        console.log('akoh');
        $("#display-form-content").html(data.html_form);
        $("#answer-countdown").html("tesing");
        var count = 5;
        setInterval(function(){
            count--;
            // document.getElementById('countDown').innerHTML = count;
            $("#answer-countdown").html("tesing");
            if (count == 0) {
                window.location = '/'; 
            }
        },1000);('Redirect()', 5000);

      }

    });
});

$(document).on("submit","#js-question-form", function (e) {
  e.preventDefault();
  form = $(this);
  form = form.append($("#token").find('input[name=csrfmiddlewaretoken]')[0]);
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    data: form.serialize(),
    dataType: 'json',
    success: function (info) {
    if (info.submitted_successfully) {
      $("#js-question-modal").hide();
      location.reload();
    }else if(info.already_submitted){
      console.log(info.already_submitted)
      console.log('no me p')
      $("#js-question-modal").hide();
      swal("You are only allowed to submit once", "Submitted assignments are graded automatically after submission", "info");
    } else {
      input = jQuery(" <input type='hidden' name=csrfmiddlewaretoken value="+''+getCookie('csrftoken')+">");
      $("#token").append(input);
      $("#display-form-content").html(info.html_form);
    }
    }
  });
});
