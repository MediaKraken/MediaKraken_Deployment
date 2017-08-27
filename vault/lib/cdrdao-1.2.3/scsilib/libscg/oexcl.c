#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>

int openexcl(const char *device, int mode)
{
  int f, i;

  f = open(device, mode | O_EXCL);

  if (f < 0) {
    f = open(device, mode);

    if (f >= 0) {
      close(f);
      f = -1;
      for (i = 0; (i < 10) && (f == -1); i++) {
	fprintf(stderr, "Error trying to open %s exclusively ... retrying in 1 second.\n", device);
	usleep(1000000 + 100000.0 * rand()/(RAND_MAX+1.0));
	f = open(device, O_RDONLY | O_NONBLOCK | O_EXCL);
      }
    }
  }

  return f;
}
