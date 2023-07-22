const currentUserId = JSON.parse(document.getElementById('current_user_id').textContent);
const currentUserName = JSON.parse(document.getElementById('current_username').textContent);
const currentUserData = JSON.parse(document.getElementById('current_user_data').textContent);

let startSocket = null

function connectStartSocket() {
    startSocket = new WebSocket(
        "ws://"
        + window.location.host
        + "/ws/start/1/"
    );
    startSocket.onopen = function(){
        console.log("startSocket successfully connected to the WebSocket.");
    };
    startSocket.onclose = function(e) {
        console.log("WebSocket startSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connectStartSocket();
        }, 2000);
    };
    startSocket.onerror = function(err) {
        console.log("WebSocket startSocket encountered an error: " + err.message);
        console.log("Closing the startSocket.");
        startSocket.close();
    };
};

connectStartSocket();

startSocket.onopen = function () {
    startSocket.send(JSON.stringify({
        'message': {
            "type": "start_refresh",
        }
    }));
    if (currentUserData.length){
        startSocket.send(JSON.stringify({
            'message': {
                "type": "user_data",
                "user_id": currentUserId,
                "username": currentUserName,
                "user_data": currentUserData,
            }
        }))
    }
}

startSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type == "start_message") {
        if (data.message["type"] == "start_playing"){
            playerStatus = document.getElementById(data.message["player_pk"]);
            rivalStatus = document.getElementById(data.message["rival_pk"]);
            playerStatus.innerHTML = "No";
            rivalStatus.innerHTML = "No";
            playerStatus.removeAttribute("style");
            rivalStatus.removeAttribute("style");
        };
        if (data.message["type"] == "end_playing"){
            playerStatus = document.getElementById(data.message["winner"]);
            rivalStatus = document.getElementById(data.message["loser"]);
            playerStatus.innerHTML = "Yes";
            rivalStatus.innerHTML = "Yes";
            playerStatus.setAttribute("style", "cursor:pointer; color:blue");
            rivalStatus.setAttribute("style", "cursor:pointer; color:blue");
        };
    } else if (data.type == "user_message") {
        if (data.message["type"] == "user_data"){
            let addedUserId = data.message["user_id"]
            if (document.getElementById("table_" + addedUserId) == null){
                let addedUserData = JSON.parse(data.message["user_data"])
                let addedUsername = data.message["username"]
                let tableBody = document.getElementById("table_body")
                let row = createTableRow(addedUserData, addedUserId, addedUsername)
                tableBody.appendChild(row)
            };
        };
    } else {
        console.log("Unknown message type!");
    }
};

let proposeSocket = null

function connectProposeSocket() {
    proposeSocket = new WebSocket(
        "ws://"
        + window.location.host
        + "/ws/propose/"
        + currentUserId
        + "/"
    );
    proposeSocket.onopen = function(){
        console.log("proposeSocket successfully connected to the WebSocket.");
    };
    proposeSocket.onclose = function(e) {
        console.log("WebSocket proposeSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connectProposeSocket();
        }, 2000);
    };
    proposeSocket.onerror = function(err) {
        console.log("WebSocket proposeSocket encountered an error: " + err.message);
        console.log("Closing the proposeSocket.");
        proposeSocket.close();
    };
};

connectProposeSocket();

proposeSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type == "propose_message") {
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

                proposeSocket.send(JSON.stringify({
                   'message': {
                       "type": "agree_to_play",
                       "player_id": currentUserId,
                       "player_username": currentUserName,
                       }
                }));
            });
        };
    } else {
        console.log("Unknown message type!");
    };
};

let statuses = document.getElementsByClassName("ready-to-play");

let proposeNewSocket = null

function connectProposeNewSocket(userId) {
    proposeNewSocket = new WebSocket(
        "ws://"
         + window.location.host
         + "/ws/propose/"
         + userId
         + "/"
    );
    proposeNewSocket.onopen = function(){
        console.log("proposeNewSocket successfully connected to the WebSocket.");
    };
    proposeNewSocket.onclose = function(e) {
        console.log("WebSocket socket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connectProposeNewSocket(userId);
        }, 2000);
    };
    proposeNewSocket.onerror = function(err) {
        console.log("WebSocket proposeNewSocket encountered an error: " + err.message);
        console.log("Closing the prososeNewSocket.");
        proposeNewSocket.close();
    };
}

for(let i=0; i<statuses.length; i++){
    if (currentUserId != statuses[i].id && statuses[i].innerHTML == 'Yes'){
        statuses[i].addEventListener("click", (event) => {

        connectProposeNewSocket(statuses[i].id)
        proposeNewSocket.onopen = function() {
            proposeNewSocket.send(JSON.stringify({
                'message': {
                    "type": "propose_to_play",
                    "player_id": currentUserId,
                    "player_username": currentUserName,
                    "rival_id": statuses[i].id,
                }
            }));
        };
            proposeNewSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                if (data.type == 'propose_message') {
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
                        let board = document.getElementById("board");
                        board.innerHTML = '<div>' + returnMessage.innerHTML + '</div>' + board.innerHTML;
                    };
                } else {
                    console.log("Unknown message type!");
                };
            };
        });
    };
}

function createTableRow(userData, userId, username){
    let row = document.createElement("tr")
    row.setAttribute("id", "table_" + userId)
    let cell = document.createElement("th")
    cell.setAttribute("scope", "row")
    cell.innerHTML = username
    row.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = userData.plays
    row.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = userData.loses
    row.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = userData.draws
    row.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = userData.wins
    row.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = userData.points
    row.appendChild(cell)
    cell = document.createElement("th")
    cell.setAttribute("id", userId)
    cell.setAttribute("class", "ready-to-play")
    cell.setAttribute("style", "cursor:pointer; color:blue")
    cell.innerHTML = "Yes"
    cell.addEventListener("click", (event) => {

        connectProposeNewSocket(userId)
        proposeNewSocket.onopen = function() {
            proposeNewSocket.send(JSON.stringify({
                'message': {
                    "type": "propose_to_play",
                    "player_id": currentUserId,
                    "player_username": currentUserName,
                    "rival_id": userId,
                }
            }));
        };
            proposeNewSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                if (data.type == 'propose_message') {
                    if (
                        data.message["type"] == "agree_to_play"
                        && data.message["player_id"] == userId
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
                        let board = document.getElementById("board");
                        board.innerHTML = '<div>' + returnMessage.innerHTML + '</div>' + board.innerHTML;
                    };
                } else {
                    console.log("Unknown message type!");
                };
            };
        });
    row.appendChild(cell)
    cell = document.createElement("th")
    cell.setAttribute("id", "proposal_" + userId)
    cell.setAttribute("style", "font-size:12px")
    row.appendChild(cell)
    return row
};
