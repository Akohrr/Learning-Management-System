function accordionFunction(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else { 
        x.className = x.className.replace(" w3-show", "");
    }
  }
  
  
$(document).ready(function () {



    // $("#js-add-new-choice-btn").click( function () {
    //   button = $(this);
    //     $.ajax({
    //       url: button.attr("data-href"),
    //       type: 'get',
    //       dataType: 'json',
        
    //       success: function (data) {
    //         $("#js-add-new-choice-modal").show();
    //         $("#display-form-content").html(data.html_form);
    //       }
    
    //     });
    //   });

      



    $(".js-add-question-assignment").click( function () {
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




});