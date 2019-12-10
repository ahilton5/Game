let PLAYING = 1;
let PAUSED = 0;
let DONE = 2;
let LEFT = "left";
let UP = "up";
let RIGHT = "right";
let DOWN = "down";
let timer;

const initialize = () => {
    document.querySelector("#dialog").style.display = "none";
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            nseconds = JSON.parse(this.responseText)['nseconds'];
            timer = setInterval(sync, nseconds);
        } 
      };
      xhttp.open("GET", "/nseconds", true);
      xhttp.send();
};

const change_dir = (dir) => {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          board = JSON.parse(this.responseText)['board'];
          let squares = document.querySelectorAll('.unit');
          for (let x = 0; x < 50; x++) {
              for (let y = 0; y < 20; y++) {
                  // console.log(board[x][y])
                  if (board[x][y] == 0) {
                      squares[x + y*50].className = "unit";
                  }
                  else if (board[x][y] == 1) {
                      // blue
                      squares[x + y*50].className = "unit blue";
                  }
                  else if (board[x][y] == 2) {
                      // blue tail
                      squares[x + y*50].className = "unit blue_tail";
                  }
                  else if (board[x][y] == 3) {
                      // blue current
                      squares[x + y*50].className = "unit blue current";
                  }
                  else if (board[x][y] == 4) {
                      // blue current tail
                      squares[x + y*50].className = "unit blue_tail current";
                  }
                  else if (board[x][y] == 5) {
                      // green
                      squares[x + y*50].className = "unit green"
                  }
                  else if (board[x][y] == 6) {
                      // green tail
                      squares[x + y*50].className = "unit green_tail";
                  }
                  else if (board[x][y] == 7) {
                      // green current
                      squares[x + y*50].className = "unit green current";
                  }
                  else if (board[x][y] == 8) {
                      // green current tail
                      squares[x + y*50].className = "unit green_tail current";
                  }
                  else {
                      console.log(board[x][y]);
                  }
              }
          }
        }
      };
      xhttp.open("GET", "/change_dir?player=green&direction=" + dir, true);
      xhttp.send();
}

const sync = () => {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        board = JSON.parse(this.responseText)['board'];
        let squares = document.querySelectorAll('.unit');
        let ngreen = 0
        let nblue = 0
        for (let x = 0; x < 50; x++) {
            for (let y = 0; y < 20; y++) {
                // console.log(board[x][y])
                if (board[x][y] == 0) {
                    squares[x + y*50].className = "unit";
                }
                else if (board[x][y] == 1) {
                    // blue
                    squares[x + y*50].className = "unit blue";
                    nblue += 1
                }
                else if (board[x][y] == 2) {
                    // blue tail
                    squares[x + y*50].className = "unit blue_tail";
                }
                else if (board[x][y] == 3) {
                    // blue current
                    squares[x + y*50].className = "unit blue current";
                    nblue += 1
                }
                else if (board[x][y] == 4) {
                    // blue current tail
                    squares[x + y*50].className = "unit blue_tail current";
                }
                else if (board[x][y] == 5) {
                    // green
                    squares[x + y*50].className = "unit green"
                    ngreen += 1
                }
                else if (board[x][y] == 6) {
                    // green tail
                    squares[x + y*50].className = "unit green_tail";
                }
                else if (board[x][y] == 7) {
                    // green current
                    squares[x + y*50].className = "unit green current";
                    ngreen += 1
                }
                else if (board[x][y] == 8) {
                    // green current tail
                    squares[x + y*50].className = "unit green_tail current";
                }
                else {
                    console.log(board[x][y]);
                }
            }
        }
        updatePlayerScore("green", ngreen)
        updatePlayerScore("blue", nblue)
      }
    };
    xhttp.open("GET", "/sync", true);
    xhttp.send();
}

const updatePlayerScore = (player, n) => {
    let alpha = n / 1000 + .5;
    if (player == "blue") {
        let bar = document.querySelector("#blue-progress");
        bar.style.width = n.toString() + "px";
        bar.style.opacity = alpha.toString();
    }
    else if (player == "green") {
        let bar = document.querySelector("#green-progress");
        bar.style.width = n.toString() + "px";
        bar.style.opacity = alpha.toString();
    }
    if (n >= 500) {
        clearInterval(timer);
        showDialog(player + " won!");
    }
}

const showDialog = (winner) => {
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/pause", true);
    xhttp.send();
    document.querySelector("#dialog").style.display = "block";
    document.querySelector("h2").innerHTML = winner;
}

document.onkeydown = function(e){
    // Space Bar
    if(e.keyCode == 32) { 
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", "/pause", true);
        xhttp.send();
    }
    // left arrow
    else if (e.keyCode == 37) {
        change_dir("left")
    }
    // up arrow
    else if (e.keyCode == 38) {
        change_dir("up")
    }
    // right arrow
    else if (e.keyCode == 39) {
        change_dir("right")
    }
    // down arrow
    else if (e.keyCode == 40) {
        change_dir("down")
    }
    // esc
    else if (e.keyCode == 27) {
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", "/reset", true);
        xhttp.send();
    }
}

document.addEventListener('DOMContentLoaded', initialize);