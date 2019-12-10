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
        %for row in range(len(board[0])):
            %for col in range(len(board)):
                <%
                    if board[col][row] == states['blue']:
                        class_list = 'unit blue'
                    elif board[col][row] == states['blue_current']:
                        class_list = 'unit blue current'
                    elif board[col][row] == states['blue_tail']:
                        class_list = 'unit blue_tail'
                    elif board[col][row] == states['blue_current_tail']:
                        class_list = 'unit blue_tail current'
                    elif board[col][row] == states['green']:
                        class_list = 'unit green'
                    elif board[col][row] == states['green_current']:
                        class_list = 'unit green current'
                    elif board[col][row] == states['green_tail']:
                        class_list = 'unit green_tail'
                    elif board[col][row] == states['green_current_tail']:
                        class_list = 'unit green_tail current'
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
            <form method="GET" action="/reset">
                <button>Reset</button>
            </form>
        </div>
    </div>
</body>
</html>