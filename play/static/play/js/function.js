
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
    socket.onopen = function(){
        console.log("Socket successfully connected to the WebSocket.");
    };
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
    socket.send(JSON.stringify({
        'message': {
            "player_pk": playerPk,
            "rival_pk": rivalPk,
        },
    }));
};

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
        'message': {
            "type": "start_playing",
            "player_pk": playerPk,
            "rival_pk": rivalPk,
        }
    }));
}

startSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type == "play_message") {
        if (data.message["type"] == "start_refresh"){
            startSocket.send(JSON.stringify({
                'message': {
                        "type": "start_playing",
                        "player_pk": playerPk,
                        "rival_pk": rivalPk,
                    }
            }));
        };
    } else {
        console.log("Unknown message type!");
    };
};

function movePiece(e) {
    let piece = e.target;
    const row = parseInt(piece.getAttribute("row"));
    const column = parseInt(piece.getAttribute("column"));
    const value = parseInt(piece.getAttribute("val"));
    let p = new Piece(row, column, value);

    if (capturedPosition.length > 0) {
        enableToCapture(p);
    } else {
        if (posNewPosition.length > 0) {
          enableToMove(p);
        };
    };
    posNewPosition = [];
    capturedPosition = [];
    capturedMap = new Map();
    if (currentPlayer * value > 0 && currentPlayer === currentUser) {
        player = reverse(currentPlayer);
        if (currentPlayer * value > 1) {
            findKingNewPosition(p, player)
        } else {
            if (!findPieceCaptured(p, player)) {
                findPossibleNewPosition(p, player);
            };
        };
    };
}

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
            if (pos.row === 0 && pos.val === 1) {
                board[pos.row][pos.column] = 2;
            } else if (pos.row === 9 && pos.val === -1) {
                board[pos.row][pos.column] = -2;
            } else {
                board[pos.row][pos.column] = pos.val;
            };
            board[readyToMove.row][readyToMove.column] = 0; // delete the old position
            // delete the piece that had been captured
            old.forEach((element) => {
                board[element.row][element.column] = 0;
            });

            // reinit ready to move value

            readyToMove = null;
            capturedPosition = [];
            posNewPosition = [];
            capturedMap = new Map();
            displayCurrentPlayer();

            socket.send(JSON.stringify({
               'message': {"receiver": receiver, "board": board},
            }));

            buildBoard();
            // check if there are possibility to capture other piece
            currentPlayer = reverse(currentPlayer);
        } else {
            buildBoard();
        };
    };
}

function enableToMove(p) {
    let find = false;
    let newPosition = null;
    // check if the case where the player play the selected piece can move on
    posNewPosition.forEach((element) => {
        if (element.compare(p)) {
          find = true;
          newPosition = element;
          return;
        };
    });

    if (find) moveThePiece(newPosition);
    else buildBoard();
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
        posNewPosition = [];
        capturedPosition = [];
        capturedMap = new Map();

        socket.send(JSON.stringify({
            'message': {"receiver": receiver, "board": board},
        }));


        currentPlayer = reverse(currentPlayer);

        displayCurrentPlayer();
        buildBoard();
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

function markPossiblePosition(p, player = 0, direction = 0) {
    attribute = parseInt(p.row + player) + "-" + parseInt(p.column + direction);

    position = document.querySelector("[data-position='" + attribute + "']");
    if (position) {
        position.style.background = "green";
        // // save where it can move
        posNewPosition.push(new Piece(p.row + player, p.column + direction, p.val));
    };
}

function buildBoard() {
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
                if (j % 2 === 0) {
                    caseType = "Whitecase";
                } else {
                    caseType = "blackCase";
                };
            } else {
                if (j % 2 !== 0) {
                    caseType = "Whitecase";
                } else {
                    caseType = "blackCase";
                };
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

    if (black === 0 || white === 0) {
        modalOpen(black);
        let result = 0;
        if (white && currentUser > 0) {
            result = white;
        } else if (black && currentUser < 0) {
            result = black;
        }
        startSocket.send(JSON.stringify({
            'message': {
            "type": "game_over",
            "user_id": userId,
            "rival_id": receiver,
            "result": result,
            }
        }));
    };

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type == "play_message") {
            if (data.message["receiver"] == userId){
                board = data.message["board"];
                buildBoard();
                currentPlayer = reverse(currentPlayer);
                displayCurrentPlayer();
            };
        } else {
            console.log("Unknown message type!");
        };
    };
}

function displayCurrentPlayer() {
    var container = document.getElementById("next-player");
    if (container.classList.contains("whitePiece")) {
        container.setAttribute("class", "occupied blackPiece");
    } else {
        container.setAttribute("class", "occupied whitePiece");
    };
}

function pieceInCapturedPosition(p){
    let arr = [];
    capturedPosition.forEach((element) => {
        if (element.newPosition.compare(p)){
            arr = element.pieceCaptured
            return;
        }
    });
    return arr;
}

function findPieceCaptured(p, player, prev=null) {
    let found = false;
    let existPieceCapturedArr = pieceInCapturedPosition(p);
    let localCapturedPosition = [];
  if (
        p.row > 1 &&
        p.column > 1 &&
        board[p.row - 1][p.column - 1] * player > 0 &&
        board[p.row - 2][p.column - 2] === 0
    ) {
        newPosition = new Piece(p.row - 2, p.column - 2, p.val);
        if (!newPosition.compare(prev)){
            found = true;
            if (!prev){
                readyToMove = p;
            };
            markPossiblePosition(newPosition);
            let pieceCapturedArr = [...existPieceCapturedArr];
            pieceCapturedArr.push(new Piece(p.row - 1, p.column - 1));
            // save the new position and the opponent's piece position
            localCapturedPosition.push({
                newPosition: newPosition,
                pieceCaptured: pieceCapturedArr,
            });
        };
      }

    if (
            p.column < 8 &&
            p.row > 1 &&
            board[p.row - 1][p.column + 1] * player > 0 &&
            board[p.row - 2][p.column + 2] === 0
        ) {
            newPosition = new Piece(p.row - 2, p.column + 2, p.val);
            if (!newPosition.compare(prev)){
                found = true;
                if (!prev){
                    readyToMove = p;
                };
                markPossiblePosition(newPosition);
                let pieceCapturedArr = [...existPieceCapturedArr];
                pieceCapturedArr.push(new Piece(p.row - 1, p.column + 1));
                // save the new position and the opponent's piece position
                localCapturedPosition.push({
                    newPosition: newPosition,
                    pieceCaptured: pieceCapturedArr,
                });
            };
        };

    if (
            p.row < 8 &&
            p.column > 1 &&
            board[p.row + 1][p.column - 1] * player > 0 &&
            board[p.row + 2][p.column - 2] === 0
        ) {
            newPosition = new Piece(p.row + 2, p.column - 2, p.val);
            if (!newPosition.compare(prev)){
                found = true;
                if (!prev){
                    readyToMove = p;
                };
                markPossiblePosition(newPosition);
                let pieceCapturedArr = [...existPieceCapturedArr];
                pieceCapturedArr.push(new Piece(p.row + 1, p.column - 1));
                // save the new position and the opponent's piece position
                localCapturedPosition.push({
                    newPosition: newPosition,
                    pieceCaptured: pieceCapturedArr,
                });
            };
        };

    if (
            p.row < 8 &&
            p.column < 8 &&
            board[p.row + 1][p.column + 1] * player > 0 &&
            board[p.row + 2][p.column + 2] === 0
        ) {
            newPosition = new Piece(p.row + 2, p.column + 2, p.val);
            if (!newPosition.compare(prev)){
                found = true;
                if (!prev){
                    readyToMove = p;
                };
                markPossiblePosition(newPosition);
                let pieceCapturedArr = [...existPieceCapturedArr];
                pieceCapturedArr.push(new Piece(p.row + 1, p.column + 1));
                // save the new position and the opponent's piece position
                localCapturedPosition.push({
                    newPosition: newPosition,
                    pieceCaptured: pieceCapturedArr,
                });
            };
        };
    localCapturedPosition.forEach((element) => {
        capturedPosition.push(element);
    });
    localCapturedPosition.forEach((element) => {
        findPieceCaptured(element.newPosition, player, p);
    });

    return found;
}

function displayCounter(black, white) {
    var blackContainer = document.getElementById("black-player-count-pieces");
    var whiteContainer = document.getElementById("white-player-count-pieces");
    blackContainer.innerHTML = black;
    whiteContainer.innerHTML = white;
}

function modalOpen(black) {
    document.getElementById("winner").innerHTML = black === 0 ? "White" : "Black";
    document.getElementById("loser").innerHTML = black !== 0 ? "White" : "Black";
    modal.classList.add("effect");
}

function modalClose() {
    modal.classList.remove("effect");
}

function reverse(player) {
    return player === -1 ? 1 : -1;
}

function findKingNewPositionDirection(y, x, p, player, first) {
    let localCapturedPosition = [];
    let i = p.row + y;
    let j = p.column + x;
    row_limit = y > 0 ? 10 : -1;
    column_limit = x > 0 ? 10 : -1;
    while (i != row_limit && j != column_limit){
        if (board[i][j] === 0){
            if (first){
                let piece = new Piece(i, j, p.val);
                prePosNewPosition.push(piece)
                readyToMove = p;
            };
        } else {
            if (i + y != row_limit && j + x != column_limit) {
                if (board[i][j] * player > 0 && board[i + y][j + x] === 0) {
                    let pieceCapturedArr = [...pieceInCapturedPosition(p)];
                    pieceCapturedArr.push(new Piece(i, j));
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
                    };
                };
            };
            return localCapturedPosition;
        };
        i += y;
        j += x;
    };
    return localCapturedPosition;
}

function isDifferent(arrA, arrB) {
    for (let i = 0; i < arrA.length; i++){
        if (arrA[i] !== arrB[i]) {
            return true;
        };
    };
    return false;
}

function findKingNewPosition(p, player, first=true){
    let localCapturedPosition = [];
    let directions = [[-1, -1], [-1, 1], [1, -1], [1, 1]];
    let forbiddenDirection = capturedMap.get(p.row.toString() + p.column.toString());
    if (!forbiddenDirection){
        forbiddenDirection = [0, 0];
    };
    directions.forEach((elem) => {
        if (isDifferent(elem, forbiddenDirection)) {
            findKingNewPositionDirection(elem[0], elem[1], p, player, first).forEach((element) => {
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
        })
        prePosNewPosition = [];
    }
};
