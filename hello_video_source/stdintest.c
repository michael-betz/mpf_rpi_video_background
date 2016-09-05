#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/time.h>

int input_timeout (int filedes, unsigned int seconds) {
  fd_set set;
  struct timeval timeout;
  /* Initialize the file descriptor set. */
  FD_ZERO (&set);
  FD_SET (filedes, &set);

  /* Initialize the timeout data structure. */
  timeout.tv_sec = seconds;
  timeout.tv_usec = 0;

  /* select returns 0 if timeout, 1 if input available, -1 if error. */
  return select(FD_SETSIZE, &set, NULL, NULL, &timeout);
}

int readStdin( char *datBuffer, int maxSize){
    int retVal = -1;
    char *pos;
    retVal = read(STDIN_FILENO, datBuffer, maxSize);
    if( retVal>0 && retVal<maxSize ){
        datBuffer[retVal] = '\0';
        if ((pos=strchr(datBuffer, '\n')) != NULL)
            *pos = '\0';
    }
    return( retVal );
}            

int main (void) {
    int retVal = -1;
    char datBuffer[256];
    while(1){
        retVal = input_timeout(STDIN_FILENO, 1);
        fprintf (stderr, "select=%d [", retVal );
        if( retVal > 0 ){
            readStdin( datBuffer, 255 );
            fprintf (stderr, "%s", datBuffer );
        }
        fprintf(stderr, "]\n");
        //sleep(3);
    }
  return 0;
}