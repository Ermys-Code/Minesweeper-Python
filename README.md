# Minesweeper-Python
Minesweeper game on terminal using a client-server connection made with Python

It uses a 2D array to generate the map and another 2D array for the visualization for the player.
Also, there is a Deep First Search algorithm designed by myself to find which ones of the coordinates in the
array aren't bombs when the player selects a coordinate.



To play, first start the server with a terminal, then start the client on a different terminal to start
the connection.

Once you are in the menu, you can select one of the two options, 1 to start the game and 2 to close
the client, to select an option type the number of the option desired and then click enter.

When you start the game, it will appear the map of the game, it will be all "X", representing that all
the coordinates are hidden.

To chose a coordinate you have to type the coordinate on X and Y, where X is the number of coordinates
horizontal and Y on vertical, separated by "/", for example 3/2, 3rd coordinate horizontal and 2nd
coordinate vertical, then you click enter to confirm the selection.

If the coordinate selected its a mine, it will appear a Fail message and a question where you can select
to play again or close the client, if you type "yes", another game will start, if instead you type
"no", the client will close itself.

If the coordinate isn't a mine, you will see the map, but this time it will be another symbol, it can
be "-", which means that there's no mines around this coordinate, or it can be a number, which means that
there are so many mines as the number indicate around the coordinate.

Once you have discovered all the coordinates that aren't mines, a Win message will appear and a question
where you can select to play again or close the client, if you type "yes", another game will start, if
instead you type "no", the client will close itself.