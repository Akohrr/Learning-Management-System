  function accordionFunction(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else { 
        x.className = x.className.replace(" w3-show", "");
    }
  }
  
  
$(document).ready(function () {



  $("#js-close-quiz-modal").click( function () {
    $("#quiz-modal").hide();
  });


    $("#js-add-new-user-btn").click( function () {
        $.ajax({
          url: '/classroom/instructor/add/quiz/',
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
            url: '/classroom/instructor/add/quiz/',
            type: "POST",
            // headers: {'X-CSRFToken': getCookie('csrftoken)')},
            data: form.serialize(),
            dataType: 'json',
            success: function (info) {
              title = $("#id_name").val() + " quiz";
            if (info.valid) {
              $("#js-add-new-user-modal").hide();
              location.reload();
              
              // $("#quiz-modal-title").html(title);

              // $("#quiz-modal").fadeOut(800, function(){
              //   $("#quiz-modal").fadeIn().delay(2000);

              // });

              // $("#quiz-modal").show();
            }
            else {
                input = jQuery(" <input type='hidden' name=csrfmiddlewaretoken value="+''+getCookie('csrftoken')+">");
                $("#token").append(input);
                $("#display-form-content").html(info.html_form);
            }
            }
        });
    });


    $("#js-question-btn").click( function () {
      $.ajax({
        url: '/classroom/instructor/add/question/',
        type: 'get',
        dataType: 'json',
      
        success: function (data) {
          $("#js-add-new-user-modal").show();
          $("#display-form-content").html(data.html_form);
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