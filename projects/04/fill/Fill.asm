// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

    @SCREEN
    D=A
    @screen_addr
    M=D

    @24575
    D=A
    @n
    M=D

    @color
    M=0

(LOOP)
    // Resets the color to white as default
    @color
    M=0
    // Reset the screen_addr variable
    @SCREEN
    D=A
    @screen_addr
    M=D

    @KBD
    D=M

    @COLOR_SCREEN   // Sets Screen to White
    D;JEQ
    @BLACK          // Sets Screen to Black
    D;JNE

(BLACK)
    @color
    M=-1        // Sets color to black

(COLOR_SCREEN)
    @screen_addr
    D=M
    @n
    D=M-D
    @LOOP
    D;JLT

    @color
    D=M
    @screen_addr
    A=M
    M=D

    @screen_addr
    M=M+1
    @COLOR_SCREEN
    0;JMP

(END)
    @END
    0;JMP