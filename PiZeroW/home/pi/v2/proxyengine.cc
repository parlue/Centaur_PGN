#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
 
#define NUM_PIPES          2
 
#define PARENT_WRITE_PIPE  0
#define PARENT_READ_PIPE   1
 
int pipes[NUM_PIPES][2];
 
/* always in a pipe[], pipe[0] is for read and
   pipe[1] is for write */
#define READ_FD  0
#define WRITE_FD 1
 
#define PARENT_READ_FD  ( pipes[PARENT_READ_PIPE][READ_FD]   )
#define PARENT_WRITE_FD ( pipes[PARENT_WRITE_PIPE][WRITE_FD] )
 
#define CHILD_READ_FD   ( pipes[PARENT_WRITE_PIPE][READ_FD]  )
#define CHILD_WRITE_FD  ( pipes[PARENT_READ_PIPE][WRITE_FD]  )
 
main()
{
 
int outfd[2];
int infd[2];
 
FILE *pFile;
 
setbuf(stdout, NULL);
setbuf(stdin, NULL);
setvbuf(stdout, NULL, _IONBF, 0);
setvbuf(stdin, NULL, _IONBF, 0);
 
 
pipe(outfd); /* Where the parent is going to write to */
pipe(infd); /* From where parent is going to read */
 
if(!fork())
{
        close(STDOUT_FILENO);
        close(STDIN_FILENO);
        dup2(outfd[0], STDIN_FILENO);
        dup2(infd[1], STDOUT_FILENO);
        close(outfd[0]); /* Not required for the child */
        close(outfd[1]);
        close(infd[0]);
        close(infd[1]);
        system("/home/pi/centaur/engines/stockfish_pi2");
}
else
{
        fcntl(infd[0],F_SETFL, O_NONBLOCK);
        fcntl(0, F_SETFL, O_NONBLOCK);
        char input[10000];
        close(outfd[0]); /* These are being used by the child */
        close(infd[1]);
        // First read the stockfish headers
        input[read(infd[0],input,10000)] = 0; /* Read from child’s stdout */
        printf("%s", input);
        char inputstring[10000];
        char bbb[2];
        int inputoffset = 0;
while (1==1) {
        char ci = fgetc(stdin);
        if (ci != 255 && ci > 0) {
                pFile = fopen("/home/pi/centaur/engines/ucilog.txt", "a");
                fprintf(pFile,"%c",ci);
                fclose(pFile);
                inputstring[inputoffset] = ci;
                inputstring[inputoffset+1] = 0;
                bbb[0] = ci;
                bbb[1] = 0;
                write(outfd[1],bbb,1);
                inputoffset++;
                if (inputstring[inputoffset-1] == 0x0A) {
                        // Both these two commands clear the log file out so we just keep the
                        // last game
                        if (strcmp(inputstring,"uci\n") == 0) {
//                              pFile = fopen("/home/pi/centaur/engines/ucilog.txt", "w");
 //                             fprintf(pFile,"%s","position startpos\n");
  //                            fclose(pFile);
                        }
                        if (strcmp(inputstring,"position startpos\n") == 0) {
                                system("/usr/bin/php /home/pi/centaur/engines/uci2pgn.php");
                                pFile = fopen("/home/pi/centaur/engines/ucilog.txt", "w");
                                fprintf(pFile,"%s","position startpos\n");
                                fclose(pFile);
                        }
                        inputoffset = 0;
                }
        }
 
 
        char buf[1];
        int c = read(infd[0],buf,1);
        if (c > 0) {
                fprintf(stdout,"%c",buf[0]);
        }
}
        close(outfd[1]);
        close(infd[0]);
}
 
}
