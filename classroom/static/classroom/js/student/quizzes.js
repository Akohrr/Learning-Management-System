
//     $(document).on("submit","#js-new-choice-form", function (e) {
//       e.preventDefault();
//       form = $(this);
//       form = form.append($("#token").find('input[name=csrfmiddlewaretoken]')[0]);
//       $.ajax({
//         url: form.attr("action"),
//         type: "POST",
//         data: form.serialize(),
//         dataType: 'json',
//         success: function (info) {
//         if (info.valid) {
//           $("#js-add-new-choice-modal").hide();
//           location.reload();
//         }
//         else {
//           input = jQuery(" <input type='hidden' name=csrfmiddlewaretoken value="+''+getCookie('csrftoken')+">");
//           $("#token").append(input);
//           $("#display-form-content").html(info.html_form);
//         }
//         }
//       });
//     });


// $(document).ready( function () {

//     $('.js-answer-quiz').click( function () {
//         row = $(this);
//         $.ajax({
//           url: row.attr("data-href"),
//           type: 'get',
//           dataType: 'json',
        
//           success: function (data) {
//             $("#js-add-new-choice-modal").show();
//             $("#display-form-content").html(data.html_form);
//           }
    
//         });
//     });

// });



function countDown (time_of_submission) {
  // Set the date we're counting down to
var countDownDate = new Date(String(time_of_submission)).getTime();

// Update the count down every 1 second
var x = setInterval(function() {

    // Get todays date and time
    var now = new Date().getTime();
    
    // Find the distance between now an the count down date
    var distance = countDownDate - now;
    
    // Time calculations for days, hours, minutes and seconds
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
    // Output the result in an element with id="demo"
    document.getElementById("answer-countdown").innerHTML = days + "d " + hours + "h "
    + minutes + "m " + seconds + "s ";
    
    // If the count down is over, write some text 
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("answer-countdown").innerHTML = "EXPIRED";
        $("#js-question-modal").hide();
        location.reload();
    }
}, 1000);
}

$('.js-answer-quiz').click( function () {
    row = $(this);
    $.ajax({
      url: row.attr("data-href"),
      type: 'get',
      dataType: 'json',
    
      success: function (data) {
        $("#js-question-modal").show();
        console.log('akoh');
        $("#display-form-content").html(data.html_form);
         time_of_submission = $("#answer-countdown").html();
        countDown(time_of_submission);

      },  
      error: function(xhr) { // if error occured
        swal("Please wait", "No questions have been added to the quiz. Please check back later", "info");

      },

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
      swal("You are only allowed to submit once", "Submitted quiz are graded automatically after submission", "info");
    } else {
      input = jQuery(" <input type='hidden' name=csrfmiddlewaretoken value="+''+getCookie('csrftoken')+">");
      $("#token").append(input);
      $("#display-form-content").html(info.html_form);
    }
    }
  });
});

