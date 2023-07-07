# py-chess
Simple text-based chess written in python. I work on this when I'm bored / on my break at work.

Almost working version! Most systems are implemented!I think the visualization of the legal moves looks very cool :-)

TODO:
- ~~SELF-CHECK detection in get_all_legal_moves~~
- ~~En Passant capturing~~
- Castling
- ~~Checkmate detection~~
- ~~Win case (Game over screen)~~
- Make a dumb bot
- Add a function to see which pieces you're allowed to move (for when you're restricted in CHECK)
- Play the silly thing to find any bugs.

"Screenshot":
```
    a   b   c   d   e   f   g   h  
  +---+---+---+---+---+---+---+---+
8 |bRb|bNb|bBb|   |bKb|bBb|bNb|bRb| 8
  +---+---+---+---+---+---+---+---+
7 |bPb|bPb|bPb|bPb|bPb|bPb|bPb|bPb| 7
  +---+---+---+---+---+---+---+---+
6 |   |   |▒▒▒|▒▒▒|▒▒▒|   |   |   | 6
  +---+---+---+---+---+---+---+---+
5 |▒▒▒|▒▒▒|▒▒▒|bQb|▒▒▒|▒▒▒|▒▒▒|▒▒▒| 5
  +---+---+---+---+---+---+---+---+
4 |   |   |▒▒▒|▒▒▒|▒▒▒|   |   |   | 4
  +---+---+---+---+---+---+---+---+
3 |   |▒▒▒|   |▒▒▒|   |▒▒▒|   |   | 3
  +---+---+---+---+---+---+---+---+
2 |▓P▓|wPw|wPw|▓P▓|wPw|wPw|▓P▓|wPw| 2
  +---+---+---+---+---+---+---+---+
1 |wRw|wNw|wBw|wQw|wKw|wBw|wNw|wRw| 1
  +---+---+---+---+---+---+---+---+
    a   b   c   d   e   f   g   h  

| The legal moves for the Queen at d5 are: 
| c5, b5, a5, e5, f5, g5, h5, d6, d4, d3, c4, b3, c6, e6, e4, f3, d2, a2, g2
```