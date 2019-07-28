#ifndef __TESTUTILS_H
#define __TESTUTILS_H

#include "libvidstab.h"

typedef struct _test_data {
  VSFrameInfo fi;
  VSFrameInfo fi_color;
  VSFrame frames[5];
} TestData;


VSTransform getTestFrameTransform(int i);

void fillArrayWithNoise(unsigned char* buffer, int length, float corr);

void paintRectangle(unsigned char* buffer, const VSFrameInfo* fi, int x, int y,
                    int sizex, int sizey, unsigned char color);

inline static unsigned char randPixel(){
  return rand()%256;
}

inline static short randUpTo(short max){
  return rand()%max;
}


int loadPGMImage(const char* filename, VSFrame* frame, VSFrameInfo* fi);

int storePGMImage(const char* filename, const uint8_t* data, VSFrameInfo fi );

#endif
