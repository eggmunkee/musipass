musipass
========

A pygame program to compose passwords based on musical notes and intervals.

Disclaimer and Security Warning
===============================
This program is not a secure password storage system. Its ability to store passwords is simple--it just pickles the plain-text passwords and mapped key-values entered.

Do not store passwords you want to keep hidden in this program's "Passmode". They can be stolen by anyone who gains access to your computer.

Let me state that again. Do not store passwords you want to keep hidden using this program's "Passmode". They can be stolen by anyone who gains access to your computer.

Controls
========

Escape - quit program

Enter - finish password sequence. Mode dependant. In Musimode, it simply clears the screen. In Passmode, the first time will save a password in memory and the second will confirm that they match, and the third will specify the name to save in the database. In Testmode, the first time will accept a password name to test and the second will report if the password matched the database entry or not.

Backquote - reset sequence and clear the screen.

Backspace - delete 1 character from sequence

Page Up/Page Down - cycle through keysets

Tab - cycle through modes (Passmode - enter/update passwords in db, Musimode - compose melodies/passwords, Testmode - test entries in db)

Any other key - if mapped in the current keyset, it will play the sound, draw the color block and the character, adding on to the password sequence

