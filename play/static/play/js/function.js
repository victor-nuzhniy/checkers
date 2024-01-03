
const playerPk = JSON.parse(document.getElementById('player_pk').textContent);
const rivalPk = JSON.parse(document.getElementById('rival_pk').textContent);
const currentUser = JSON.parse(document.getElementById('current_user').textContent);
const receiver = JSON.parse(document.getElementById('receiver').textContent);
const userId = JSON.parse(document.getElementById('user_id').textContent);

let socket = null;

function connectSocket() {
    socket = new WebSocket(
        "ws://"
         + window.location.host
         + "/ws/play/"
         + playerPk
         + "/"
         + rivalPk
         + "/"
    );
    socket.onclose = function(e) {
        console.log("WebSocket socket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connectSocket();
        }, 2000);
    };
    socket.onerror = function(err) {
        console.log("WebSocket socket encountered an error: " + err.message);
        console.log("Closing the socket.");
        socket.close();
    };
}
connectSocket();
socket.onopen = function() {
    socket.onmessage = function(e){
        const data = JSON.parse(e.data);
        if (data.type == "user_play_join_message"){
            const joinedUserId = data.message.user_id;
            let playerBoard = null
            if (joinedUserId == playerPk) {
                playerBoard = document.getElementById("white_player")
            } else {
                playerBoard = document.getElementById("black_player")
            };
            if (Boolean(data.message.board) && playerBoard.innerHTML !== "Active"){
                board = data.message.board
                currentPlayer = data.message.player
                setCurrentPlayer(currentPlayer)
                buildBoard(true);
            }
            playerBoard.innerHTML = "Active";
            playerBoard.setAttribute("style", "color:blue")
        } else if (data.type == "user_play_leave_message"){
            const joinedUserId = data.message.user_id;
            let playerBoard = null
            if (joinedUserId == playerPk) {
                playerBoard = document.getElementById("white_player")
            } else {
                playerBoard = document.getElementById("black_player")
            }
            playerBoard.innerHTML = "Not active.";
            playerBoard.removeAttribute("style")
        } else if (data.type == "play_message") {
            if (data.message.receiver == userId){
                board = data.message.board;
                currentPlayer = data.message.player;
                buildBoard(true);
                displayCurrentPlayer();
            };
        } else if(data.type == "ask_rival") {
            if (
                userId != data.message.user_id && (
                data.message.user_id == playerPk && document.getElementById("black_player").innerHTML == "Active" ||
                data.message.user_id == rivalPk && document.getElementById("black_player").innerHTML == "Active"
                )
            ){
                socket.send(JSON.stringify({
                    "type": "answer_rival"
                }));
            };
        } else if(data.type == "answer_rival") {
            let blackStatus = document.getElementById("black_player")
            blackStatus.innerHTML = "Active"
            blackStatus.setAttribute("style", "color:blue")
            let whiteStatus = document.getElementById("white_player")
            whiteStatus.innerHTML = "Active"
            whiteStatus.setAttribute("style", "color:blue")
        } else if (data.type == "user_message") {
            const today = new Date()
            const chat = document.getElementById("chat")
            chat.value += `${today.toLocaleDateString()} ${today.toLocaleTimeString()} ${data.message.username} ${data.message.text} \n`;
            chat.scrollTop = chat.scrollHeight
        } else if (data.type == "propose_draw") {
            if (data.message.receiver == userId) {
                document.getElementById("proposeDraw").style.display = "none";
                document.getElementById("agreeDraw").style.display = "block";
                document.getElementById("refuseDraw").style.display = "block";
            }
        } else if (data.type == "agree_draw") {
            if (data.message.receiver == userId){
                gameOverDraw();
            };
        } else if (data.type == "refuse_draw") {
            if (data.message.receiver == userId) {
                const answerDraw = document.getElementById("answerDraw")
                answerDraw.innerHTML = "Rival refused";
                setTimeout(() => {
                    answerDraw.innerHTML = "Waiting for an answer";
                    answerDraw.style.display = "none";
                    document.getElementById("proposeDraw").style.display = "block";
                }, 5000);
            }
        } else {
            console.log("Unknown message type!");
        };
    };
    if (
        userId == playerPk && document.getElementById("black_player").innerHTML != 'Active' ||
        userId == rivalPk && document.getElementById("white_player").innerHTML != 'Active'
    ) {
        socket.send(JSON.stringify({
            "type": "ask_rival",
            "message": {"user_id": userId}
        }));
    }
};

let startSocket = null

function connectStartSocket() {

    startSocket = new WebSocket(
        "ws://"
         + window.location.host
         + "/ws/start/1/"
        );
    startSocket.onclose = function(e) {
        console.log("WebSocket with startSocket connection closed unexpectedly. Trying to reconnect in 2s...");
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

startSocket.onopen = function() {
    startSocket.send(JSON.stringify({
        "type": "start_playing",
        "message": {"player_pk": userId}
    }));
}

startSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type == "refresh") {
        startSocket.send(JSON.stringify({
            "type": "start_playing",
            'message': {"player_pk": userId}
        }));
    } else {
        console.log("Unknown message type!");
    };
};

function draw() {
    const proposeDraw = document.getElementById("proposeDraw");
    const answerDraw = document.getElementById("answerDraw");
    const agreeDraw = document.getElementById("agreeDraw");
    const refuseDraw = document.getElementById("refuseDraw");
    proposeDraw.addEventListener("click", () => {
        socket.send(JSON.stringify({
            "type": "propose_draw",
            "message": {"receiver": receiver}
        }));
        proposeDraw.style.display = "none";
        answerDraw.style.display = "block";
    });
    agreeDraw.addEventListener("click", () => {
        socket.send(JSON.stringify({
            "type": "agree_draw",
            "message": {"receiver": receiver}
        }));
        gameOverDraw();
    });
    refuseDraw.addEventListener("click", () => {
        socket.send(JSON.stringify({
            "type": "refuse_draw",
            "message": {"receiver": receiver}
        }));
        agreeDraw.style.display = "none";
        refuseDraw.style.display = "none";
        proposeDraw.style.display = "block";
    });
};

draw();

function movePiece(e) {
    let piece = e.target;
    const row = parseInt(piece.getAttribute("row"));
    const column = parseInt(piece.getAttribute("column"));
    const value = parseInt(piece.getAttribute("val"));
    let p = new Piece(row, column, value);

    if (capturedPosition.length > 0) {
        enableToCapture(p);
    } else {
        if (posNewPosition.size > 0) {
          enableToMove(p);
        };
    };
    posNewPosition = new Set();
    capturedPosition = [];
    capturedMap = new Map();
    if (currentPlayer * value > 0 && currentPlayer === currentUser) {
        player = reverse(currentPlayer);
        if (!findCapturedPieces(p, player)) {
            findPossibleNewPosition(p, player);
        };
    };
};

function enableToCapture(p) {
    let find = false;
    if (currentPlayer == currentUser){
        let pos = null;
        capturedPosition.forEach((element) => {
            if (element.newPosition.compare(p)) {
                find = true;
                pos = element.newPosition;
                old = element.pieceCaptured;
                return;
            };
        });

        if (find) {
            // if the current piece can move on, edit the board and rebuild
            board[pos.row][pos.column] = pos.val; // move the piece

            board[readyToMove.row][readyToMove.column] = 0; // delete the old position
            // delete the piece that had been captured
            old.forEach((element) => {
                board[element.row][element.column] = 0;
            });

            // reinit ready to move value

            readyToMove = null;
            capturedPosition = [];
            posNewPosition = new Set();
            capturedMap = new Map();
            displayCurrentPlayer();

            socket.send(JSON.stringify({
               "type": "play_message",
               "message": {"receiver": receiver, "board": board, "player": reverse(currentPlayer)},
            }));
            currentPlayer = reverse(currentPlayer);
            buildBoard(true);
            // check if there are possibility to capture other piece
        } else {
            buildBoard();
        };
    };
}

function enableToMove(p) {
    if (posNewPosition.has(`${p.row}${p.column}`)) {
        moveThePiece(p)
    } else {
        buildBoard();
    }
}

function moveThePiece(newPosition) {
    if (currentPlayer == currentUser){
        // if the current piece can move on, edit the board and rebuild
        if (newPosition.row === 0 && newPosition.val === 1) {
            board[newPosition.row][newPosition.column] = 2;
        } else if (newPosition.row === 9 && newPosition.val === -1) {
            board[newPosition.row][newPosition.column] = -2;
        } else {
            board[newPosition.row][newPosition.column] = newPosition.val;
        };
        board[readyToMove.row][readyToMove.column] = 0;
        // init value
        readyToMove = null;
        posNewPosition = new Set();
        capturedPosition = [];
        capturedMap = new Map();
        currentPlayer = reverse(currentPlayer);
        socket.send(JSON.stringify({
            "type": "play_message",
            "message": {"receiver": receiver, "board": board, "player": currentPlayer},
        }));
        displayCurrentPlayer();
        buildBoard(true);
    };
}

function findPossibleNewPosition(piece, player) {
    if (board[piece.row + player][piece.column + 1] === 0) {
        readyToMove = piece;
        markPossiblePosition(piece, player, 1);
    };
    if (board[piece.row + player][piece.column - 1] === 0) {
        readyToMove = piece;
        markPossiblePosition(piece, player, -1);
    };
}

function markPossiblePosition(p, player = 0, direction = 0, prevPosition=null) {
    attribute = parseInt(p.row + player) + "-" + parseInt(p.column + direction);
    position = document.querySelector("[data-position='" + attribute + "']");
    if (position) {
        position.style.background = "green";
        position.setAttribute("val", p.val)
        posNewPosition.add(`${p.row + player}${p.column + direction}`);
    };
};

function buildBoard(checkBoard=false) {
    game.innerHTML = "";
    let black = 0;
    let white = 0;
    for (let i = 0; i < board.length; i++) {
        const element = board[i];
        let row = document.createElement("div"); // create div for each row
        row.setAttribute("class", "r");

        for (let j = 0; j < element.length; j++) {
            const elmt = element[j];
            let col = document.createElement("div"); // create div for each case
            let piece = document.createElement("div");
            let caseType = "";
            let occupied = "";

            if (i % 2 === 0) {
                caseType = j % 2 === 0 ? "Whitecase" : "blackCase"
            } else {
                caseType = j % 2 !== 0 ? "Whitecase" : "blackCase"
            };

            // add the piece if the case isn't empty
            if (board[i][j] === 1) {
                occupied = "whitePiece";
            } else if (board[i][j] === 2) {
                occupied = "kingWhitePiece";
            } else if (board[i][j] === -1) {
                occupied = "blackPiece";
            } else if (board[i][j] === -2) {
                occupied = "kingBlackPiece";
            } else {
                occupied = "empty";
            };

            piece.setAttribute("class", "occupied " + occupied);

            // set row and colum in the case
            piece.setAttribute("row", i);
            piece.setAttribute("column", j);
            piece.setAttribute("val", board[i][j]);
            piece.setAttribute("data-position", i + "-" + j);

            //add event listener to each piece
            piece.addEventListener("click", movePiece);

            col.appendChild(piece);

            col.setAttribute("class", "column " + caseType);
            row.appendChild(col);

            // counter number of each piece
            if (board[i][j] < 0) {
                black++;
            } else if (board[i][j] > 0) {
                white++;
            };
            //display the number of piece for each player
            displayCounter(black, white);
        };
        game.appendChild(row);
    };
    if (checkBoard) {
        if (!checkPossibilityToMove()) {
            if (black > 0 && white > 0) {
                currentPlayer > 0 ? white = 0 : black = 0;
            };
            modalOpen(black);
            document.getElementById("game_over").innerHTML = "Game over";
            const resultDiv = document.getElementById("result");
            resultDiv.setAttribute("class", "counter mt-2");
            let showResult = white ? 'White' : 'Black';
            resultDiv.innerHTML =
                showResult
                + ' wins! <a href="http://'
                + window.location.host
                + '/start/">Go and see result!</a>'
            let result = 0;
            if (white && currentUser > 0) {
                result = white;
            } else if (black && currentUser < 0) {
                result = black;
            }
            startSocket.send(JSON.stringify({
                "type": "game_over",
                "message": {
                "user_id": userId,
                "rival_id": receiver,
                "result": result,
                "white": currentUser > 0 ? true : false,
                }
            }));
        };
    };
};

function gameOverDraw() {
    modalOpen(null);
    document.getElementById("game_over").innerHTML = "Game over"
    const resultDiv = document.getElementById("result");
    resultDiv.setAttribute("class", "counter mt-2");
    resultDiv.innerHTML =
        'Draw! <a href="http://'
        + window.location.host
        + '/start/">Go and see result!</a>';
    startSocket.send(JSON.stringify({
        "type": "game_over",
        "message": {
        "user_id": userId,
        "rival_id": receiver,
        "result": -1,
        "white": currentUser > 0 ? true : false,
        }
    }));
};

function displayCurrentPlayer() {
    var container = document.getElementById("next-player");
    if (container.classList.contains("whitePiece")) {
        container.setAttribute("class", "occupied blackPiece");
    } else {
        container.setAttribute("class", "occupied whitePiece");
    };
}

function setCurrentPlayer(currentPlayer) {
    var container = document.getElementById("next-player");
    if (currentPlayer < 0) {
        container.setAttribute("class", "occupied blackPiece");
    } else {
        container.setAttribute("class", "occupied whitePiece");
    };
};

function pieceInCapturedPosition(p){
    let arr = [];
    capturedPosition.forEach((element) => {
        if (element.newPosition.compare(p)){
            arr = element.pieceCaptured;
            return;
        };
    });
    return arr;
}

function findCapturedPieces(p, player, prev=null, first=true) {
    if (p.val * (-player) === 1) {
        return findSimplePieceCaptured(p, player, prev);
        };
    return findKingNewPosition(p, player, first)
};

function findSimplePieceCaptured(p, player, prev=null) {
    let found = false;
    let existPieceCapturedArr = pieceInCapturedPosition(p);
    let localCapturedPosition = [];
    directionList.forEach(direction => {
        if (direction.checkPiece(p.row, p.column, player)) {
            const limit = direction.row > 0 ? 9 : 0;
            const coef = p.row + 2 * direction.row === limit ? 2 : 1;
            newPosition = new Piece(
                p.row + 2 * direction.row,
                p.column + 2 * direction.column,
                coef * p.val
            );
            if (!newPosition.compare(prev)) {
                found = true;
                if (!prev) {
                    readyToMove = p;
                };
                markPossiblePosition(newPosition, 0, 0, p);
                let pieceCapturedArr = [...existPieceCapturedArr];
                pieceCapturedArr.push(
                    new Piece(p.row + direction.row, p.column + direction.column)
                );
                localCapturedPosition.push({
                    newPosition: newPosition,
                    pieceCaptured: pieceCapturedArr
                });
            };
        };
    });
    localCapturedPosition.forEach(element => {
        capturedPosition.push(element);
        findCapturedPieces(element.newPosition, player, p, false);
    });
    return found;
};

function displayCounter(black, white) {
    var blackContainer = document.getElementById("black-player-count-pieces");
    var whiteContainer = document.getElementById("white-player-count-pieces");
    blackContainer.innerHTML = black;
    whiteContainer.innerHTML = white;
}

function modalOpen(black=null) {
    if (black === null) {
        document.getElementById("winner").innerHTML = "Draw";
        document.getElementById("loser").innerHTML = "Draw";
    } else {
        document.getElementById("winner").innerHTML = black === 0 ? "White" : "Black";
        document.getElementById("loser").innerHTML = black !== 0 ? "White" : "Black";
    }
    modal.classList.add("effect");
}

function modalClose() {
    modal.classList.remove("effect");
}

function reverse(player) {
    return player === -1 ? 1 : -1;
}

function findPieceInArr(p, arr) {
    return arr.every(element => !element.compare(p))
};

function findKingNewPositionDirection(y, x, p, player, first) {
    let localCapturedPosition = [];
    let i = p.row + y;
    let j = p.column + x;
    const row_limit = y > 0 ? 10 : -1;
    const column_limit = x > 0 ? 10 : -1;
    while (i != row_limit && j != column_limit){
        if (board[i][j] === 0){
            if (first){
                let piece = new Piece(i, j, p.val);
                prePosNewPosition.push(piece)
                readyToMove = p;
            };
        } else {
            let flag = true
            if (i + y != row_limit && j + x != column_limit) {
                if (board[i][j] * player > 0 && board[i + y][j + x] === 0) {
                    let pieceCapturedArr = [...pieceInCapturedPosition(p)];
                    const newPiece = new Piece(i, j)
                    if (findPieceInArr(newPiece, pieceCapturedArr)) {
                        pieceCapturedArr.push(newPiece);
                        if (first){
                            readyToMove = p;
                        };
                        i += y;
                        j += x;
                        while (i != row_limit && j != column_limit) {
                            if (board[i][j] === 0){
                                let newPosition = new Piece(i, j, p.val);
                                if (!capturedMap.has(i.toString() + j.toString())){
                                    capturedMap.set(i.toString() + j.toString(), [-y, -x]);
                                    markPossiblePosition(newPosition);
                                    localCapturedPosition.push({
                                        newPosition: newPosition,
                                        pieceCaptured: pieceCapturedArr,
                                    });
                                };
                            } else {
                                break;
                            };
                            i += y;
                            j += x;
                        }
                    } else {
                        flag = false;
                    };
                };
            };
            if (flag) {
                return localCapturedPosition;
            };
        };
        i += y;
        j += x;
    };
    return localCapturedPosition;
}

function isDifferent(objA, objB) {
    if (objA.row !== objB.row || objA.column !== objB.column) {
        return true;
    };
    return false;
}
function findKingNewPosition(p, player, first=true){
    let localCapturedPosition = [];
    let forbiddenDirection = capturedMap.get(p.row.toString() + p.column.toString());
    if (!forbiddenDirection){
        forbiddenDirection = new Direction(0, 0);
    };
    directionList.forEach((elem) => {
        if (isDifferent(elem, forbiddenDirection)) {
            findKingNewPositionDirection(elem.row, elem.column, p, player, first).forEach((element) => {
                localCapturedPosition.push(element);
            });
        };
    });
    localCapturedPosition.forEach((element) => {
        capturedPosition.push(element);
    });
    localCapturedPosition.forEach((element) => {
        findKingNewPosition(element.newPosition, player, false);
    });
    if (!capturedPosition.length) {
        prePosNewPosition.forEach((element) => {
            markPossiblePosition(element);
        });
    };
    prePosNewPosition = [];
    return true
};

// chat message block

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
        socket.send(JSON.stringify({
            "type": "user_message",
            "message": {"text": message}
        }));
        chatMessageInput.value = "";
    }
};
//end chat message block

// check moving possibilities block

function checkPossibilityToMove() {
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++) {
            if (board[i][j] * currentPlayer > 0) {
//                const piece = new Piece(i, j, board[i][j])
                if (getPieceMovingPossibilities(i, j, board[i][j], reverse(currentPlayer))) {
                    return true;
                };
            };
        };
    };
    return false;
}

function getPieceMovingPossibilities(row, column, val, player) {
    if (val * (-player) > 1) {
        if (checkKingCapturedPiece(row, column, val, player)) {
            return true;
        }
    } else {
        if (checkSimpleCapturedPiece(row, column, player)) {
            return true;
        };
        if (checkPossibleNewPosition(row, column, player)) {
            return true;
        };
    }
    return false;
};


function checkSimpleCapturedPiece(row, column, player) {
    for (const direction of directionList) {
        // this place for refactor
        if (direction.checkPiece(row, column, player)) {
            return true;
        };
    };
    return false;
};

function checkKingCapturedPiece(row, column, val, player) {
    for (const direction of directionList) {
        let i = row + direction.row
        let j = column + direction.column
        const row_limit = direction.row > 0 ? 10 : -1;
        const column_limit = direction.column > 0 ? 10 : -1;
        if (i != row_limit && j != column_limit){
            if (board[i][j] === 0){
                return true;
            };
        };
        if (i + direction.row >= row_limit && j + direction.column >= column_limit) {
            if (board[i + direction.row][j + direction.column] === 0) {
                return true;
            };
        };
    };
    return false;
};

function checkPossibleNewPosition(row, column, player) {
    if (row + player >= 0 && row + player < 10) {
        if (board[row + player][column + 1] === 0) {
            return true;
        };
        if (board[row + player][column - 1] === 0) {
            return true;
        };
    };
    return false;
};

// end check moving possibilities block
