  function accordionFunction(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else { 
        x.className = x.className.replace(" w3-show", "");
    }
  }
  


  $("#js-close-quiz-modal").click( function () {
    $("#quiz-modal").hide();
  });


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

      
  // $(document).on("submit","#js-new-choice-form", function (e) {
  //   e.preventDefault();
  //   form = $(this);
  //   form = form.append($("#token").find('input[name=csrfmiddlewaretoken]')[0]);
  //   $.ajax({
  //     url: form.attr("action"),
  //     type: "POST",
  //     data: form.serialize(),
  //     dataType: 'json',
  //     success: function (info) {
  //     if (info.valid) {
  //       $("#js-add-new-choice-modal").hide();
  //       location.reload();
  //     }
  //     else {
  //       input = jQuery(" <input type='hidden' name=csrfmiddlewaretoken value="+''+getCookie('csrftoken')+">");
  //       $("#token").append(input);
  //       $("#display-form-content").html(info.html_form);
  //     }
  //     }
  //   });
  // });


    $(".js-add-question-quiz").click( function () {
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


