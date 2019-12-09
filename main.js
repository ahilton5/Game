let PLAYING = 1;
let PAUSED = 0;
let DONE = 2;
let LEFT = 0;
let UP = 1;
let RIGHT = 2;
let DOWN = 3;

let gameState;
let blueDirection;
let greenDirection;
let blueX;
let blueY;
let greenX;
let greenY;
let board;
let currentColor;
let currentColorTail;
let otherColor;
let otherColorTail;

const isInBounds = (x, y) => {
    if (x < 0 || x == 50 || y < 0 || y == 20) return false;
    else return true;
}

const isValidPath = (x, y, itteration) => {
    let originalX = x;
    let originalY = y;
    let isEnclosedUp = false;
    let isEnclosedRight = false;
    let isEnclosedDown = false;
    let isEnclosedLeft = false;
    if (itteration > 4) return true;
    for (x = originalX; x < 50; x++) {
        if (board[x][y].classList.contains(currentColor) || board[x][y].classList.contains(currentColorTail)) {
            isEnclosedRight = isValidPath(x - 1, y, itteration + 1);
            break;
        }
    }
    if (!isEnclosedRight) return false;
    for (x = originalX; x >= 0; x--) {
        if (board[x][y].classList.contains(currentColor) || board[x][y].classList.contains(currentColorTail)) {
            isEnclosedLeft = isValidPath(x + 1, y, itteration + 1);
            break;
        }
    }
    if (!isEnclosedLeft) return false;
    x = originalX;
    for (y = originalY; y < 20; y++) {
        if (board[x][y].classList.contains(currentColor) || board[x][y].classList.contains(currentColorTail)) {
            isEnclosedUp = isValidPath(x, y - 1, itteration + 1);
            break;
        }
    }
    if (!isEnclosedUp) return false;
    for (y = originalY; y >= 0; y--) {
        if (board[x][y].classList.contains(currentColor) || board[x][y].classList.contains(currentColorTail)) {
            isEnclosedDown = isValidPath(x, y + 1, itteration + 1);
            break;
        }
    }
    if (!isEnclosedDown) return false;
    return (isEnclosedDown && isEnclosedLeft && isEnclosedRight && isEnclosedUp);
}

const claimRange = (x, y) => {
    if (x < 0) x = 49;
    else if (x > 49) x = 0;
    if (y < 0) y = 19;
    else if (y > 19) y = 0;
    if (board[x][y].classList.contains(currentColor)) return;
    if (board[x][y].classList.contains(currentColorTail) || isValidPath(x, y, 1)) {
        claimUnit(board[x][y]);
        claimRange(x - 1, y);
        claimRange(x + 1, y);
        claimRange(x, y - 1);
        claimRange(x, y + 1);
    }
}

const claimUnit = (div) => {
    div.classList.remove(otherColor);
    div.classList.remove(otherColorTail);
    div.classList.remove(currentColorTail);
    div.classList.add(currentColor);
}

const switchColors = (color) => {
    if (color == "green") {
        currentColor = "green";
        currentColorTail = "green_tail";
        otherColor = "blue";
        otherColorTail = "blue_tail";
    }
    else {
        currentColor = "blue";
        currentColorTail = "blue_tail";
        otherColor = "green";
        otherColorTail = "green_tail";
    }
}

const moveGreenToCoordinate = (x, y) => {
    board[greenX][greenY].classList.remove("current");
    greenX = x;
    greenY = y;
    switchColors("green");
    finishMove(x, y);
}

const moveBlueToCoordinate = (x, y) => {
    board[blueX][blueY].classList.remove("current");
    blueX = x;
    blueY = y;
    switchColors("blue");
    finishMove(x, y);
}

const finishMove = (x, y) => {
    board[x][y].classList.add("current");
    if (board[x][y].classList.contains(currentColorTail)) {
        //showDialog(otherColor + " won!");
        board[x][y].classList.add(currentColorTail);
        regenerate(currentColor);
    }
    else if (board[x][y].classList.contains(otherColorTail)) {
       // showDialog(currentColor + " won!");
       if (!board[x][y].classList.contains(currentColor)) {
        board[x][y].classList.add(currentColorTail);
       }
       regenerate(otherColor);
    }
    else if(!board[x][y].classList.contains(currentColor)) {
        board[x][y].classList.add(currentColorTail);
    }
    else {
        claimRange(x - 1, y);
        claimRange(x + 1, y);
        claimRange(x, y - 1);
        claimRange(x, y + 1);
        updatePlayerScore(currentColor, false);
    }
}

const initialize = () => {
    gameState = PAUSED;
    blueDirection = RIGHT;
    greenDirection = LEFT;    
    let main = document.querySelector("main");
    /* 
     * Create a 50 by 20 grid.
     * Define (0, 0) to be the bottom left corner of grid.
     * Define (49, 19) to be the top right corner of grid.
    */
    board = new Array(50);
    for (let x = 0; x < 50; x++) {
        board[x] = new Array(20);
        for (let y = 0; y < 20; y++) {
            board[x][y] = document.createElement("div");
            board[x][y].classList.add("unit");
        }
    }
    for (let y = 19; y >= 0; y--) {
        for (let x = 0; x < 50; x++) {
            main.appendChild(board[x][y]);
        }
    }
    for (let x = 1; x < 4; x++) {
        switchColors("blue");
        claimUnit(board[x][9]);
        claimUnit(board[x][10]);
        claimUnit(board[x][11]);
    }
    blueX = 2;
    blueY = 10;
    moveBlueToCoordinate(2, 10);
    for (let x = 46; x < 49; x++) {
        switchColors("green");
        claimUnit(board[x][9]);
        claimUnit(board[x][10]);
        claimUnit(board[x][11]);
    }
    greenX = 47;
    greenY = 10;
    moveGreenToCoordinate(47, 10);
    document.querySelector("#dialog").style.display = "none";
};

const advanceBlue = () => {
    switch(blueDirection) {
        case LEFT: 
            if (blueX > 0) {
                moveBlueToCoordinate(blueX - 1, blueY);
            }
            else {
                moveBlueToCoordinate(49, blueY);
            }
            break;
        case UP:
            if (blueY != 19) {
                moveBlueToCoordinate(blueX, blueY + 1);
            }
            else {
                moveBlueToCoordinate(blueX, 0);
            }
            break;
        case RIGHT:
            if (blueX != 49) {
                moveBlueToCoordinate(blueX + 1, blueY);
            }
            else {
                moveBlueToCoordinate(0, blueY);
            }
            break;
        case DOWN:
            if (blueY != 0) {
                moveBlueToCoordinate(blueX, blueY - 1);
            }
            else {
                moveBlueToCoordinate(blueX, 19);
            }
            break;
    }
}

const advanceGreen = () => {
    switch(greenDirection) {
        case LEFT: 
            if (greenX > 0) {
                moveGreenToCoordinate(greenX - 1, greenY);
            }
            else {
                moveGreenToCoordinate(49, greenY);
            }
            break;
        case UP:
            if (greenY != 19) {
                moveGreenToCoordinate(greenX, greenY + 1);
            }
            else {
                moveGreenToCoordinate(greenX, 0);
            }
            break;
        case RIGHT:
            if (greenX != 49) {
                moveGreenToCoordinate(greenX + 1, greenY);
            }
            else {
                moveGreenToCoordinate(0, greenY);
            }
            break;
        case DOWN:
            if (greenY != 0) {
                moveGreenToCoordinate(greenX, greenY - 1);
            }
            else {
                moveGreenToCoordinate(greenX, 19);
            }
            break;
    }
}


const advance = () => {
    let random = Math.floor(Math.random() * 2);
    if (random == 0) {
        advanceBlue();
        advanceGreen();
    }
    else {
        advanceGreen();
        advanceBlue();
    }
}

async function regenerate(color) {
    updatePlayerScore(color, true);
    let tail;
    if (color == "blue") tail = "blue_tail";
    else tail = "green_tail";
    for (let x = 0; x < 50; x++) {
        for (let y = 0; y < 20; y++) {
            if (board[x][y].classList.contains(color)) {
                board[x][y].classList.remove(color);
            }
            if (board[x][y].classList.contains(tail)) {
                board[x][y].classList.remove(tail);
            }
        }
    }
    let randomX = Math.floor(Math.random() * 47) + 1;
    let randomY = Math.floor(Math.random() * 17) + 1;
    for (let x = randomX - 1; x <= randomX + 1; x++) {
        switchColors(color);
        claimUnit(board[x][randomY - 1]);
        claimUnit(board[x][randomY]);
        claimUnit(board[x][randomY + 1]);
    }
    if (color == "blue") {
        board[blueX][blueY].classList.remove("current");
        blueX = randomX;
        blueY = randomY;
        moveBlueToCoordinate(randomX, randomY);
    }
    else {
        board[greenX][greenY].classList.remove("current");
        greenX = 2;
        greenY = 10;
        moveGreenToCoordinate(randomX, randomY);
    }
}

const getPlayerTotal = (color, regenerate) => {
    if (regenerate) {
        return 9;
    }
    let total = 0;
    for (let x = 0; x < 50; x++) {
        for (let y = 0; y < 20; y++) {
            if (board[x][y].classList.contains(color)) {
                total++;
            }
        }
    }
    return total;
}

const updatePlayerScore = (color, regenerate) => {
    let playerTotal = getPlayerTotal(color, regenerate);
    let alpha = playerTotal / 1000 + .5;
    if (color == "blue") {
        let bar = document.querySelector("#blue-progress");
        bar.style.width = playerTotal.toString() + "px";
        bar.style.opacity = alpha.toString();
    }
    else if (color == "green") {
        let bar = document.querySelector("#green-progress");
        bar.style.width = playerTotal.toString() + "px";
        bar.style.opacity = alpha.toString();
    }
    if (playerTotal >= 500) {
        showDialog(color + " won!");
    }
}

const showDialog = (winner) => {
    gameState = DONE;
    clearInterval(timer)
    document.querySelector("#dialog").style.display = "block";
    document.querySelector("h2").innerHTML = winner;
}

document.onkeydown = function(e){
    // Space Bar
    if(e.keyCode == 32) { 
        if (gameState == PAUSED) {
            gameState = PLAYING;
            timer = setInterval(advance, 150);
        }
        else if (gameState == PLAYING) {
            gameState = PAUSED;
            clearInterval(timer);
        }
        else {
            document.querySelector("form").submit();
        }
    }
    // a (blue left)
    else if (e.keyCode == 65) {
        blueDirection = LEFT;
    }
    // w (blue up)
    else if (e.keyCode == 87) {
        blueDirection = UP;
    }
    // d (blue right)
    else if (e.keyCode == 68) {
        blueDirection = RIGHT;
    }
    // s (blue down)
    else if (e.keyCode == 83) {
        blueDirection = DOWN;
    }
    // left arrow (green left)
    else if (e.keyCode == 37) {
        greenDirection = LEFT;
    }
    // up arrow (green up)
    else if (e.keyCode == 38) {
        greenDirection = UP;
    }
    else if (e.keyCode == 39) {
        greenDirection = RIGHT;
    }
    else if (e.keyCode == 40) {
        greenDirection = DOWN;
    }
}

document.addEventListener('DOMContentLoaded', initialize);