const currentUserId = JSON.parse(document.getElementById('current_user_id').textContent);
const currentUserName = JSON.parse(document.getElementById('current_username').textContent);

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
        "type": "refresh",
    }));
}

startSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type == "start_playing"){
        playerStatus = document.getElementById(data.message.player_pk);
        playerStatus.innerHTML = "Busy";
        playerStatus.removeAttribute("style");
    } else if (data.type == "game_over"){
        playerStatus = document.getElementById(data.message.user_id);
        rivalStatus = document.getElementById(data.message.rival_id);
        playerStatus.innerHTML = "Yes";
        rivalStatus.innerHTML = "Yes";
        playerStatus.setAttribute("style", "cursor:pointer; color:blue");
        rivalStatus.setAttribute("style", "cursor:pointer; color:blue");
    } else if (data.type == "user_join_message") {
        let addedUserId = data.message.user_id
        if (document.getElementById("table_" + addedUserId) == null){
            const addedUserData = data.message["user_data"]
            const addedUsername = data.message["username"]
            const tableBody = document.getElementById("table_body")
            const row = createTableRow(addedUserData, addedUserId, addedUsername)
            tableBody.appendChild(row)
        };
    } else if (data.type == "user_leave_message") {
        let addedUserId = data.message.user_id
        const row = document.getElementById("table_" + addedUserId)
        if (row !== null) {
            const tableBody = document.getElementById("table_body")
            tableBody.removeChild(row)
            }
    } else if (data.type == "user_message") {
        const today = new Date()
        const chat = document.getElementById("chat")
        chat.value += `${today.toLocaleDateString()} ${today.toLocaleTimeString()} ${data.message.username} ${data.message.text} \n`;
        chat.scrollTop = chat.scrollHeight
    } else if (data.type == "propose") {
        if (data.message.rival_id === currentUserId){
            const message = document.getElementById("proposal_" + data.message.player_id)
            const a = document.createElement("a")
            const link =
                'http://'
                + window.location.host
                + '/'
                + data.message.player_id
                + '/'
                + currentUserId
                + '/'
            a.setAttribute("href", link)
            a.innerHTML = data.message.player_username + " invite!"
            const board = document.getElementById("board")
            a.addEventListener("click", (event) => {

                startSocket.send(JSON.stringify({
                   "type": "agree",
                   "message": {
                       "player_id": currentUserId,
                       "rival_id": data.message.player_id,
                       "player_username": currentUserName,
                       }
                }));
            });
            const cloneA = a.cloneNode(true)
            cloneA.addEventListener("click", (event) => {

                startSocket.send(JSON.stringify({
                   "type": "agree",
                   "message": {
                       "player_id": currentUserId,
                       "rival_id": data.message.player_id,
                       "player_username": currentUserName,
                       }
                }));
            });
            message.appendChild(a)
            board.insertBefore(cloneA, board.firstChild)
        };
    } else if (data.type == "agree") {
        if (data.message.rival_id === currentUserId) {
            const returnMessage = document.getElementById("proposal_" + data.message.player_id)
            const board = document.getElementById("board");
            const a = document.createElement("a")
            const link =
                "http://"
                + window.location.host
                + '/'
                + currentUserId
                + '/'
                + data.message.player_id
                + '/'
            a.setAttribute("href", link)
            a.innerHTML = "Join " + data.message.player_username + "!"
            const cloneA = a.cloneNode(true)
            returnMessage.appendChild(a)
            board.insertBefore(cloneA, board.firstChild)
        };
    } else {
        console.log("Unknown message type!");
    };
};

let statuses = document.getElementsByClassName("ready-to-play");

for(let i=0; i<statuses.length; i++){
    if (currentUserId != statuses[i].id && statuses[i].innerHTML == 'Ready'){
        statuses[i].addEventListener("click", (event) => {
            startSocket.send(JSON.stringify({
                "type": "propose",
                "message": {
                    "player_id": currentUserId,
                    "player_username": currentUserName,
                    "rival_id": parseInt(statuses[i].id),
                }
            }));
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
    cell.innerHTML = "Ready"
    cell.addEventListener("click", (event) => {
        startSocket.send(JSON.stringify({
            "type": "propose",
            "message": {
                "player_id": currentUserId,
                "player_username": currentUserName,
                "rival_id": parseInt(userId),
            }
        }));
    });
    row.appendChild(cell)
    cell = document.createElement("th")
    cell.setAttribute("id", "proposal_" + userId)
    cell.setAttribute("style", "font-size:12px")
    row.appendChild(cell)
    return row
};

const chatMessageInput = document.getElementById("chat-message-input");
const chatMessageSubmit = document.getElementById("chat-message-submit");

chatMessageInput.focus();
chatMessageInput.onkeyup = function(e) {
    if (e.key === "Enter") {
        chatMessageSubmit.click();
    };
};

chatMessageSubmit.onclick = function(e) {
    const message = chatMessageInput.value;
    if(Boolean(message)) {
        startSocket.send(JSON.stringify({
            "type": "user_message",
            "message": {"text": message}
        }));
        chatMessageInput.value = "";
    }
};
