var ws = undefined;

function ws_init(callback_dict, room, specific) {
    var hostname = window.document.location.hostname;
    var port = window.document.location.port;

    if ("WebSocket" in window) {
        var wsproto = "ws";

        if (hostname == "localhost" || hostname == "127.0.0.1") {
            ws = new WebSocket(wsproto + "://" + hostname + ":8080/ws/" + room + "/" + specific);
        }
        else {
            ws = new WebSocket(wsproto + "://" + hostname + ":8000/ws/" + room + "/" + specific);
        }
        ws.onmessage = function (msg) {
            var data = JSON.parse(msg.data);
            var channel = data["channel"];
            if (channel) {
                if (callback_dict[channel])
                    callback_dict[channel](data);
            }
        };
    }
    else {
        alert("No WebSocket support in your browser.");
    }
}

function dummy(msg) {
    console.log(msg);
}