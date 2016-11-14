#
#  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  version 2, as published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License version 2 for more details.
#
#  You should have received a copy of the GNU General Public License
#  version 2 along with this program; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

#include <Adafruit_NeoPixel.h>
#ifdef __AVR_ATtiny85__ // Trinket, Gemma, etc.
#include <avr/power.h>
#endif
const int PIN = 3;
// Variables and setttings for LED
// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)

const int NEO_RING_SMALL = 12;
const int NEO_RING_MEDIUM = 16;
const int NEO_RING_LARGE = 24;

int total_neo_pixels = NEO_RING_MEDIUM;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(total_neo_pixels, PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit.

// Setup the variables for the serial communications
char inData[20]; // Allocate some space for the string
char inChar=-1; // Where to store the character read
byte index = 0; // Index into array; where to store the character
String txtMsg = "";
char serial_char;

void setup()
{
    // serial setup
    Serial.begin(9600);
    pinMode(13, OUTPUT);   // digital sensor is on digital pin 2
    // led setup
    strip.begin();
    strip.show(); // Initialize all pixels to 'off'
    //colorWipeAll(strip.Color(0, 127, 0), 50); // green
}

void loop()
{
    #Serial.write("A");
    #digitalWrite(13, HIGH);
    #delay(200);
    while (Serial.available() > 0)
    {
        serial_char = Serial.read();
        if (serial_char == '\n')
        {
            if (txtMsg.length() > 3)
            {
                // check for wipe mode
                if (txtMsg.substring(0,1) == "W")
                {
                    // wipe all
                    if(txtMsg.substring(0,3) == "WA-")
                    {
                        // wa-999 999 999 9999 9999 9999   no actual spaces sent for speed
                        // color, color color, speed, start, end
                        // starting points 3(3), 6(3), 9(3), 12(4), 16(4), 20(4)
                        colorWipeAll(strip.Color(txtMsg.substring(3,3).toInt(), txtMsg.substring(6,3).toInt(), txtMsg.substring(9,3).toInt()), txtMsg.substring(12,4).toInt());
                    }
                    else
                    {
                        // wipe range
                        if(txtMsg.substring(0,3) == "WR-")
                        {
                            colorWipeStartEnd(strip.Color(txtMsg.substring(3,3).toInt(), txtMsg.substring(6,3).toInt(), txtMsg.substring(9,3).toInt()), txtMsg.substring(12,4).toInt(), txtMsg.substring(16,4).toInt(), txtMsg.substring(20,4).toInt());
                        }
                    }
                }
                // check for rainbow
                else
                {
                    if (txtMsg.substring(0,1) == "R")
                    {
                        // rainbow all
                        if (txtMsg.substring(0,3) == "RA-")
                        {
                            // ra-9999
                            // wait time only
                            rainbowAll(txtMsg.substring(3,4).toInt());
                        }
                        else
                        {
                            // rainbow range
                            if (txtMsg.substring(0,3) == "RR-")
                            {
                                // rr-9999 9999 9999
                                // wait, start, end
                                rainbowStartEnd(txtMsg.substring(3,4).toInt(),txtMsg.substring(7,4).toInt(),txtMsg.substring(11,4).toInt());
                            }
                            else
                            {
                                // rainbow cycle all
                                if (txtMsg.substring(0,3) == "RCA")
                                {
                                    // rca9999
                                    // wait time only
                                    rainbowCycleAll(txtMsg.substring(3,4).toInt());
                                }
                                else
                                {
                                    // rainbow cycle range
                                    if (txtMsg.substring(0,3) == "RCR")
                                    {
                                        // rca9999 9999 9999
                                        // wait, start, end
                                        rainbowCycleStartEnd(txtMsg.substring(3,4).toInt(),txtMsg.substring(7,4).toInt(),txtMsg.substring(11,4).toInt());
                                    }
                                }
                            }
                        }
                    }
                    // check for theatre chase
                    else
                    {
                        if (txtMsg.substring(0,1) == "T")
                        {
                            // theatre all
                            if (txtMsg.substring(0,3) == "TA-")
                            {
                                // ta-999 999 999 9999
                                // color, wait time only
                                theaterChaseAll(strip.Color(txtMsg.substring(3,3).toInt(), txtMsg.substring(6,3).toInt(), txtMsg.substring(9,3).toInt()), txtMsg.substring(12,4).toInt());
                            }
                            else
                            {
                                // theatre range
                                if (txtMsg.substring(0,3) == "TR-")
                                {
                                    // tr-999 999 999 9999 9999 9999
                                    // color, wait time, start, end
                                    theaterChaseStartEnd(strip.Color(txtMsg.substring(3,3).toInt(), txtMsg.substring(6,3).toInt(), txtMsg.substring(9,3).toInt()), txtMsg.substring(12,4).toInt(), txtMsg.substring(16,4).toInt(), txtMsg.substring(20,4).toInt());
                                }
                                else
                                {
                                    // theatre rainbow all
                                    if (txtMsg.substring(0,3) == "TRA")
                                    {
                                        // tra-9999
                                        // wait time
                                        theaterChaseRainbowAll(txtMsg.substring(3,4).toInt());
                                    }
                                    else
                                    {
                                        // theatre rainbow range
                                        if (txtMsg.substring(0,3) == "TRR")
                                        {
                                            // trr-9999 9999 9999
                                            // wait time, start, end
                                            theaterChaseRainbowStartEnd(txtMsg.substring(3,4).toInt(),txtMsg.substring(7,4).toInt(),txtMsg.substring(11,4).toInt());
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            // Serial.println(txtMsg);
            txtMsg = "";
        }
        else
        {
            txtMsg.concat(serial_char);
        }
    }
}

// Fill the dots one after the other with a color
void colorWipeAll(uint32_t c, uint8_t wait)
{
    for(uint16_t i=0; i < strip.numPixels(); i++)
    {
        strip.setPixelColor(i, c);
        strip.show();
        delay(wait);
    }
}

// Fill the dots one after the other with a color
void colorWipeStartEnd(uint32_t c, uint8_t wait, uint8_t led_start, uint8_t led_stop)
{
    for(uint16_t i=led_start; i < led_stop; i++)
    {
        strip.setPixelColor(i, c);
        strip.show();
        delay(wait);
    }
}

void rainbowAll(uint8_t wait)
{
    uint16_t i, j;
    for(j=0; j < 256; j++)
    {
        for(i=0; i < strip.numPixels(); i++)
        {
            strip.setPixelColor(i, Wheel((i+j) & 255));
        }
        strip.show();
        delay(wait);
    }
}

void rainbowStartEnd(uint8_t wait, uint8_t led_start, uint8_t led_stop)
{
    uint16_t i, j;
    for(j=0; j < 256; j++)
    {
        for(i=led_start; i < led_stop; i++)
        {
            strip.setPixelColor(i, Wheel((i+j) & 255));
        }
        strip.show();
        delay(wait);
    }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycleAll(uint8_t wait)
{
    uint16_t i, j;
    for(j=0; j < 256*5; j++)   // 5 cycles of all colors on wheel
    {
        for(i=0; i < strip.numPixels(); i++)
        {
            strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
        }
        strip.show();
        delay(wait);
    }
}

void rainbowCycleStartEnd(uint8_t wait, uint8_t led_start, uint8_t led_stop)
{
    uint16_t i, j;
    for(j=0; j < 256*5; j++)   // 5 cycles of all colors on wheel
    {
        for(i=led_start; i < led_stop; i++)
        {
            strip.setPixelColor(i, Wheel(((i * 256 / ((led_stop - led_start) + 1)) + j) & 255));
        }
        strip.show();
        delay(wait);
    }
}


// Theatre-style crawling lights.
void theaterChaseAll(uint32_t c, uint8_t wait)
{
    for (int j=0; j < 10; j++)    //do 10 cycles of chasing
    {
        for (int q=0; q < 3; q++)
        {
            for (int i=0; i < strip.numPixels(); i=i+3)
            {
                strip.setPixelColor(i+q, c);    //turn every third pixel on
            }
            strip.show();
            delay(wait);
            for (int i=0; i < strip.numPixels(); i=i+3)
            {
                strip.setPixelColor(i+q, 0);        //turn every third pixel off
            }
        }
    }
}

void theaterChaseStartEnd(uint32_t c, uint8_t wait, uint8_t led_start, uint8_t led_stop)
{
    for (int j=0; j < 10; j++)    //do 10 cycles of chasing
    {
        for (int q=0; q < 3; q++)
        {
            for (int i=led_start; i < led_stop; i=i+3)
            {
                strip.setPixelColor(i+q, c);    //turn every third pixel on
            }
            strip.show();
            delay(wait);
            for (int i=led_start; i < led_stop; i=i+3)
            {
                strip.setPixelColor(i+q, 0);        //turn every third pixel off
            }
        }
    }
}


// Theatre-style crawling lights with rainbow effect
void theaterChaseRainbowAll(uint8_t wait)
{
    for (int j=0; j < 256; j++)       // cycle all 256 colors in the wheel
    {
        for (int q=0; q < 3; q++)
        {
            for (int i=0; i < strip.numPixels(); i=i+3)
            {
                strip.setPixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
            }
            strip.show();
            delay(wait);
            for (int i=0; i < strip.numPixels(); i=i+3)
            {
                strip.setPixelColor(i+q, 0);        //turn every third pixel off
            }
        }
    }
}

void theaterChaseRainbowStartEnd(uint8_t wait, uint8_t led_start, uint8_t led_stop)
{
    for (int j=0; j < 256; j++)       // cycle all 256 colors in the wheel
    {
        for (int q=0; q < 3; q++)
        {
            for (int i=led_start; i < led_stop; i=i+3)
            {
                strip.setPixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
            }
            strip.show();
            delay(wait);
            for (int i=led_start; i < led_stop; i=i+3)
            {
                strip.setPixelColor(i+q, 0);        //turn every third pixel off
            }
        }
    }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos)
{
    if(WheelPos < 85)
    {
        return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
    }
    else if(WheelPos < 170)
    {
        WheelPos -= 85;
        return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
    }
    else
    {
        WheelPos -= 170;
        return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
    }
}
