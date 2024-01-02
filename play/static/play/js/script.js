class Piece {
  constructor(row, column, val=0) {
    this.row = row;
    this.column = column;
    this.val = val
  }

  compare(piece) {
    if (!piece){
        return false;
    };
    return piece.row === this.row && piece.column === this.column;
  };
};

const modal = document.getElementById("easyModal");
let game = document.getElementById("game");
let currentPlayer = 1;
let posNewPosition = new Set();
let prePosNewPosition = [];
let capturedPosition = [];
let capturedMap = new Map();


let board = [
  [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
  [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
  [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
  [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
];


class Direction {
    constructor(row, column) {
        this.row = row;
        this.column = column
    };

    checkPiece(row, column, player) {
        return (
            (this.row > 0 ? row < 8 : row > 1) &&
            (this.column > 0 ? column < 8 : column > 1) &&
            (board[row + this.row][column + this.column] * player > 0) &&
            (board[row + 2 * this.row][column + 2 * this.column] === 0)
        )
    };
};

const directionList = [
    new Direction(-1, -1),
    new Direction(-1, 1),
    new Direction(1, -1),
    new Direction(1, 1)
]
