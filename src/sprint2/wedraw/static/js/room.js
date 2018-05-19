var webSocketBridge = new channels.WebSocketBridge();

var room = $("p.room");
roomId = room.attr("data-room-id");

var ws_path = "/room/"+roomId;

webSocketBridge.connect(ws_path);
webSocketBridge.listen(function(data) {
    // Decode the JSON
    if(data.user == undefined) {
        var begin = data.text;
        if (begin.command == "begin") {
            if ($("#begingame").length == 0) {
                window.location.href = "guesser"
            } else if ($("#begingame").length == 1) {
                window.location.href = "drawer";
            }

        }
    } else {

        var user = $("<li>" + data.user + "</li>");
        $("#player").append(user);
    }

});


$(document).ready(function () {
    $('#begingame').click(function () {
        var roomInfoSend = new Object();
        roomInfoSend.command = "begin";
        webSocketBridge.send(JSON.stringify(roomInfoSend));
    });
});