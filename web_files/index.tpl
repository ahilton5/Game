<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Paper Game - Alden Hilton</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="main.css" />
    <link rel="icon" href="../favicon.png">
    <script src="main.js"></script>
</head>
<body>
    <main>
        %for row in range(board.shape[0]):
            %for col in range(board.shape[1]):
                <%
                    if board[row, col] == states['blue']:
                        class_list = 'unit blue'
                    elif board[row, col] == states['blue_current']:
                        class_list = 'unit blue current'
                    elif board[row, col] == states['green']:
                        class_list = 'unit green'
                    elif board[row, col] == states['green_current']:
                        class_list = 'unit green current'
                    else:
                        class_list = 'unit'
                    end
                %>
                <div class="{{class_list}}"></div>                
            %end
        %end

    </main>
    <div id="bar" class="progress-bar">
        <div id="blue-progress" class="progress-bar"></div>
        <div id="green-progress" class="progress-bar"></div>
    </div>
    
    <div id="dialog">
        <div id="dialog-content">
            <h2>Javasript Error -- Unable to load page</h2>
            <form>
                <button>Reset</button>
            </form>
        </div>
    </div>
</body>
</html>