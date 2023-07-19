
      const socket = new WebSocket(
        "ws://"
         + window.location.host
         + "/ws/start/1/"
        );
      socket.onclose = function(e) {
        console.log('Socket closed unexpectedly 1');
        };
        socket.addEventListener("close", (event) => {
            console.log("Socket was closed, SSSSSSSSSSS")
        })
      socket.onopen = function(){
             socket.send(JSON.stringify({
            'message': {
            "type": "start_refresh",
            }
          }));
        }
      socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data.message)
        if (data.message["type"] == "start_playing"){
             playerStatus = document.getElementById(data.message["player_pk"])
             rivalStatus = document.getElementById(data.message["rival_pk"])
            playerStatus.innerHTML = "Yes"
            rivalStatus.innerHTML = "Yes"

        };
        if (data.message["type"] == "end_playing"){
             playerStatus = document.getElementById(data.message["winner"])
             rivalStatus = document.getElementById(data.message["loser"])
            playerStatus.innerHTML = "No"
            rivalStatus.innerHTML = "No"
        };
        };
