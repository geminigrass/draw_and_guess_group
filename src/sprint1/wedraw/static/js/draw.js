var context;
var startX;
var startY;
var start = false;
var rect;
var dataURL;
var word;

// get the canvas element using the DOM
var canvas = $('#drawing-area').get(0);
context = canvas.getContext("2d");
var timer;
//draw canvas
//global variable for the DEFAULT brush effect
//these can be changes by clicking the button
var curTool = "Pencil";
var curRadius = 15;
//remember to change the color for BOTH fillstyle and strockstyle
var curColor = "rgb(0,0,0)";//bule
const webSocketBridge = new channels.WebSocketBridge();
webSocketBridge.connect('/chat/');
webSocketBridge.listen(function(action, stream) {
  console.log("======data here!!===")
  console.log(action, stream);
  console.log(action.x)
  console.log(action.y)

});
// #=====================================================================================
// #
// #  Code chunk 1 : painter - functions (copy from draw.js)
// #
// #============================================================================

// function draw() {
//   $.get("/wedraw/guesser")
//       .done(function(data) {

//   if(!canvas) {
//     alert("Can't find the canvas element");
//     return;
//   }

//   if(!(canvas.getContext)) {
//     alert("Sorry, can't find context");
//     return;
//   }

//   // get the graph context
//   context = canvas.getContext("2d");

//   // get canvas area
//   rect = canvas.getBoundingClientRect();

//   });

// }

//helper function for Tools
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

//initlize word information, hints, ect.
function wordInfoset(){
  $.get("/wedraw/getWordInfo/")
  .done(function(data) {
    localStorage.setItem('word',data['word']);    
    painter_mod();
});
}

// userlist
function getUserList() {

  var list = $("#user-list");
  var max_time = list.data("max-time")

  $.get("/wedraw/appendNewUser/"+max_time)
  .done(function(data) {

      list.data('max-time', data['max-time']);
      for (var i = 0; i < data.items.length; i++) {
         var item = data.items[i];
         var new_item = item.username;
         var id = item.userid;
         var idHTML = id +"_inList";
         var score = item.userscore;
         var html = "<h4 "+ "id="+"'"+idHTML+"'" +">"+new_item+" : "+score+" "+"</h4>";
         list.prepend(html);
      }
  });
}

// update list score
function updateListScore() {

  var list = $("#user-list");
  var max_time = "1970-01-01T00:00+00:00";
  list.html('');
  $.get("/wedraw/appendNewUser/"+max_time)
  .done(function(data) {

      list.data('max-time', data['max-time']);
      for (var i = 0; i < data.items.length; i++) {
         var item = data.items[i];
         var new_item = item.username;
         var id = item.userid;
         var idHTML = id +"_inList";
         var score = item.userscore;
         var html = "<h4 "+ "id="+"'"+idHTML+"'" +">"+new_item+" : "+score+" "+"</h4>";
         list.prepend(html);
      }
  });
}

// #=====================================================================================
// #
// #  Code chunk 2 : painter - DOM (copy from draw.js)
// #
// #=========================================================================================
// get the start position of the mouse, when mouse is down, start drawing
$( "#drawing-area" ).mousedown(function(event) {
    event.preventDefault();;
  // get the x and y coordinate in drawing-area
  // need to substract rect.left and rect.top in order to get the right coordinate
   startX = event.clientX - rect.left;
   startY = event.clientY - rect.top;
   start = true;
});

// When user resize the browser window, relocate the draw area
$(window).resize(function() {
  // draw();
});

// When the mouse is moving, draw as the mouse goes
$( "#drawing-area" ).mousemove(function(event) {
  event.preventDefault();
  if(!start) {
    return;
  }

  // get the x and y coordinate in drawing-area
  var x = event.clientX - rect.left;
  var y = event.clientY - rect.top;
 
  //   // draw something
  console.log("tools!")
  console.log(curTool)
  if (curTool == "Pencil") {
    context.lineWidth = curRadius;
    context.fillStyle = curColor;
    context.strokeStyle = curColor;
  }

  // TODO:implement tools
  if (curTool == "Eraser"){
    //TODO:reset radius,color,tool etc
    console.log("===========================eraser!")
    context.strokeStyle = "rgb(255,255,255)";//white
    context.fillStyle = "rgb(255,255,255)";
    curColor = "rgb(255,255,255)";
    context.lineWidth = 20;//this is the default radius for eraser
  }

  // context.moveTo(startX, startY);
  // context.lineTo(x, y);
  console.log("=====here")
  var contentSend = new Object();
  contentSend.x = x;
  contentSend.y = y;
  contentSend.startX = startX;
  contentSend.startY = startY;
  contentSend.drawstyle = curTool;
  contentSend.curColor = curColor;
  contentSend.curRadius = curRadius;
  contentSend.command = "draw";
  // contendSend.drawstyle = 1;
  webSocketBridge.send(JSON.stringify(contentSend));
  context.strokeStyle = curColor;
  context.beginPath();
  context.moveTo(x, y);
  context.lineTo(startX, startY);
  context.closePath();
  context.stroke();

 
  // socket = new WebSocket("ws://" + window.location.host + "/chat/");
  // socket.onmessage = function(e) {
  //   // draw(e.x, e.y, e.context);
  //   console.log("======data here")
  //   console.log(e)
    
  //   context.beginPath();
  //   context.moveTo(e.tartX, e.startY);
  //   context.lineTo(e.x, e.y);
  //   context.stroke();
  //   context.save();
  // }
  
  // socket.onopen = function() {
  //     var contentSend = new Object();
  //     contentSend.x = x;
  //     contentSend.y = y;
  //     contentSend.startX = startX;
  //     contentSend.startY = startY;

  //     console.log(JSON.stringify(contentSend))
  //     socket.send(JSON.stringify(contentSend));
  // }
  // if (socket.readyState == WebSocket.OPEN) socket.onopen();



  startX = x;
  startY = y;

  // dataURL = canvas.toDataURL();
  // localStorage.setItem( 'objectToPass', dataURL );
});

// when mouse is up, stop drawing
$( "#drawing-area" ).mouseup(function(event) {
  event.preventDefault();
  start = false;
  // store canvas's image url to local storage
  // later pass it to the guesser. Not useful, implement webSocket in sprint2
  // dataURL = canvas.toDataURL();
  // localStorage.setItem( 'objectToPass', dataURL );
});

// when user moves his mouse out of the bound of canvas, stop drawing
$( "#drawing-area" ).mouseout(function(event) {
  event.preventDefault();
  start = false;
  //dataURL = canvas.toDataURL();
  // localStorage.setItem( 'objectToPass', dataURL );
});

// #=====================================================================================
// #
// #  Code chunk 3 ： code that initially in guess.js
// #
// #===================================================================================

// time counter
function counter(seconds) {
  // get the counter element in the html template
  var counter = $('#counter');

  // set a timer to run for every 1000ms, that's 1 second
  timer = setInterval(function(){
    seconds--;

    // display the remaining time
    counter[0].innerHTML = seconds;
    // if time counts down to 0, stop timing
    if(seconds == 0)
        clearInterval(timer);

    },1000);

}

// #=====================================================================================
// #
// #  Code chunk 4 ： code for game logic
// #
// #===================================================================================
//helper function for degub
function painter_mod() {

    document.getElementById("painter-hint").innerHTML = localStorage.getItem('word');
    rect = canvas.getBoundingClientRect();
}

// #=====================================================================================
// #
// #  Code chunk 5 ：
// #
// #===================================================================================


$(document).ready(function () {

  wordInfoset();
  // draw();
  getUserList();
  counter(60);

  window.setInterval(updateListScore, 5000);
  // window.setInterval(newATurn, 1000);
  $('#clear-room').click(function () {
      $.post("clear-room",{})
          .done(function (data) {
      })
  });


  $('#clear-btn').click(function () {
      context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
    //   webSocketBridge.send({
    //     "command": "clear",
    //     "message": "aaa"
    // });
    window.location.reload();
      
  });

  $('#tool-form input[type="button"]').click(function(){
      curTool = this.value;
  });

// Choose color
  $('#color-form input[type="button"]').click(function(){

    var color = this.value;
    if(color == "Red") {
      curColor = "rgb(255, 0, 0)";
    } else if (color == "Blue")
    curColor = "rgb(0, 153, 255)";
    else if (color == "Yellow") {
      curColor = "rgb(255, 255, 0)";
    }
    else if (color == "Black") {
      curColor = "rgb(0,0,0)";
    }
});

$('#size-form input[type="button"]').click(function(){
  var color = this.value;
  if(color == "Big") {
    curRadius = 25;
  } else if (color == "Medium")
  curRadius = 15;
  else if (color == "Small") {
    curRadius = 5;
  }
});

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });

});
