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


  function timer (count) {
    alert(count);
    setInterval(function(){
        count--;
        document.getElementById('countDown').innerHTML = count;
        if (count == 0) {
            window.location = '/'; 
        }
    },1000);('Redirect()', 5000); 

  };