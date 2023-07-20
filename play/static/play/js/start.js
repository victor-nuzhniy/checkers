const currentUserId = JSON.parse(document.getElementById('current_user_id').textContent);
const currentUserName = JSON.parse(document.getElementById('current_username').textContent);
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
            playerStatus.innerHTML = "No"
            rivalStatus.innerHTML = "No"
            playerStatus.removeAttribute("style")
            rivalStatus.removeAttribute("style")
        };
        if (data.message["type"] == "end_playing"){
             playerStatus = document.getElementById(data.message["winner"])
             rivalStatus = document.getElementById(data.message["loser"])
            playerStatus.innerHTML = "Yes"
            rivalStatus.innerHTML = "Yes"
            playerStatus.setAttribute("style", "cursor:pointer; color:blue")
            rivalStatus.setAttribute("style", "cursor:pointer; color:blue")
        };
        };

    const startSocket = new WebSocket(
            "ws://"
             + window.location.host
              + "/ws/propose/"
              + currentUserId
              + "/"
        );
    startSocket.onclose = function(e) {
        console.log('Socket closed unexpectedly 1');
        };
    startSocket.addEventListener("close", (event) => {
            console.log("Socket was closed, start")
        })
    startSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data.message, "outside", 9999999999999)
        if (
            data.message["type"] == "propose_to_play"
            && data.message["player_id"] != currentUserId
            && data.message["rival_id"] == currentUserId
        ) {
            let message = document.getElementById("proposal_" + data.message["player_id"])
            message.innerHTML =
            '<a href="http://'
            + window.location.host
            + '/'
            + data.message["player_id"]
            + '/'
            + currentUserId
            + '/">'
            + data.message["player_username"]
            + " invite!</a>"
            let board = document.getElementById("board")
            board.innerHTML =
                '<div>'
                + data.message["player_username"]
                + ' invite!'
                + '</div>'
                + board.innerHTML
            message.addEventListener("click", (event) => {
                const answerSocket = new WebSocket(
                    "ws://"
                     + window.location.host
                      + "/ws/propose/"
                      + currentUserId
                      + "/"
                    );
                answerSocket.onclose = function(e) {
                    console.log('Socket closed unexpectedly 777777777777');
                    };
                answerSocket.addEventListener("close", (event) => {
                        console.log("Socket was closed, start")
                    })
                answerSocket.onopen = function(){
                     answerSocket.send(JSON.stringify({
                    'message': {
                    "type": "agree_to_play",
                    "player_id": currentUserId,
                    "player_username": currentUserName,
                    }
                  }));
                }
            });
        };
        };

let statuses = document.getElementsByClassName("ready-to-play")


for(let i=0; i<statuses.length; i++){
    console.log(statuses[i].innerHTML)
    console.log(statuses[i].id)
    if (currentUserId != statuses[i].id && statuses[i].innerHTML == 'Yes'){
        statuses[i].addEventListener("click", (event) => {

            const proposeSocket = new WebSocket(
                "ws://"
                 + window.location.host
                  + "/ws/propose/"
                  + statuses[i].id
                  + "/"
                );
            proposeSocket.onclose = function(e) {
                console.log('Socket closed unexpectedly');
                };
            proposeSocket.addEventListener("close", (event) => {
                    console.log("Socket was closed, start 4444444444")
                })
            proposeSocket.onopen = function(){
                 proposeSocket.send(JSON.stringify({
                'message': {
                "type": "propose_to_play",
                "player_id": currentUserId,
                "player_username": currentUserName,
                "rival_id": statuses[i].id,
                }
              }));
            };
        proposeSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log(data.message, "outside")
            if (
                data.message["type"] == "agree_to_play"
                && data.message["player_id"] == statuses[i].id
            ) {
                let returnMessage = document.getElementById("proposal_" + data.message["player_id"])
                returnMessage.innerHTML =
                '<a href="http://'
                + window.location.host
                + '/'
                + currentUserId
                + '/'
                + data.message["player_id"]
                + '/">Join '
                + data.message["player_username"]
                + '!</a>'
                let board = document.getElementById("board")
                board.innerHTML = '<div>' + returnMessage.innerHTML + '</div>' + board.innerHTML
            };
            };
        })
    }
}
