let startingBoard = [...Array(9)].map(e => Array(9));
let board = [...Array(9)].map(e => Array(9));

fetch('/new_board')
    .then(response => response.json())
    .then(data => {
        //console.log(data);
        board = data;
        startingBoard = data;
    })
    .catch(error => console.error('Error:', error));

let number = 0;

function selectNumber(object) {
    number = object.dataset.number;
    //console.log("selected number : '" + number + "'");
}

function writeNumber(object) {
    object.innerHTML = parseInt(number) != 0 ? number : "";
    object.dataset.value = number;
    board[object.dataset.x][object.dataset.y] = parseInt(number);
    //console.log("grid coordinates: [" + object.dataset.x + ", " + object.dataset.y + "]");
    //console.log("new board[" + object.dataset.x + "][" + object.dataset.y + "] = " + board[object.dataset.x][object.dataset.y]);
    if(isBoardFull()) {
        //console.log("Board is full.");
        fetch('/player_board', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(board),
        })
        .then(response => response.json())
        .then(responseData => {
            //console.log("Solved: " + responseData.status);
            if(responseData.status) {
                document.getElementById("success").style.display = 'flex';
                setTimeout(function() { hide(document.getElementById("success")); }, 3000);
            } else {
                document.getElementById("fail").style.display = 'flex';
                setTimeout(function() { hide(document.getElementById("fail")); }, 3000);
            }
            //alert(responseData.message);
        })
        .catch(error => console.error('Error:', error));
    }
}

function isBoardFull() {
    let zeroCount = 0;
    for(let i = 0; i < 9; i++) {
        for(let j = 0; j < 9; j++) {
            if(board[i][j] == 0) {
                zeroCount++;
            }
        }
    }
    //console.log("Zero count is: <" + zeroCount + ">");
    return zeroCount == 0;
}

function hide(object) {
    object.style.display = 'none';
}