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
let posNewPosition = [];
let prePosNewPosition = [];
let capturedPosition = [];
let capturedMap = new Map();

let board = [
  [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
  [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
  [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
  [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
];

buildBoard();

//let board = [
//  [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
//  [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
//  [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
//  [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
//  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
//  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
//  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
//  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
//  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
//  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
//];
