// for (i=0; i < n; i++) {
//      Draw 16 black pixels at the beginning of row i
// }

// Pseudocode:

// addr = SCREEN
// n = RAM[0]
// i = 0

// LOOP:
//     if i > n goto END
//     RAM[addr] = -1
//     addr = addr + 32
//     i = i + 1
//     goto LOOP

// END:
//     goto END

    @R0
    D=M
    @n
    M=D     // n = RAM[0]

    @i
    M=0     // i = 0

    @SCREEN
    D=A
    @addr
    M=D     // addr = 16384

(LOOP)
    @i
    D=M
    @n
    D=D-M
    @END
    D;JGT   // if i > n goto END

    @addr
    A=M
    M=-1    // RAM[addr] = 11..

    @i
    M=M+1   // i = i + 1
    @32
    D=A
    @addr
    M=D+M   // addr = addr + 32
    @LOOP
    0;JMP   // goto loop

(END)
    @END
    0;JMP