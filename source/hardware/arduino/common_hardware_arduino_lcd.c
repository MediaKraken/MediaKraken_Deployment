// include fat libs so can load raw images from sd card
#include <tinyFAT.h>
#include <UTFT.h>
#include <UTFT_tinyFAT.h>

// Declare which fonts we will be using
extern uint8_t SmallFont[];
extern uint8_t BigFont[];
extern uint8_t SevenSegNumFont[];

// ID for Mega
UTFT myGLCD(ITDB32S,38,39,40,41);
UTFT_tinyFAT myFiles(&myGLCD);

// List of filenames for pictures to display.
char* files320[]= {"PIC101.RAW", "PIC102.RAW", "PIC103.RAW", "PIC104.RAW", "PIC105.RAW", "PIC106.RAW", "PIC107.RAW", "PIC108.RAW", "PIC109.RAW", "PIC110.RAW"}; // 240x320
char* files400[]= {"PIC201.RAW", "PIC202.RAW", "PIC203.RAW", "PIC204.RAW", "PIC205.RAW", "PIC206.RAW", "PIC207.RAW", "PIC208.RAW", "PIC209.RAW", "PIC210.RAW"}; // 240x400
char* files220[]= {"PIC501.RAW", "PIC502.RAW", "PIC503.RAW", "PIC504.RAW", "PIC505.RAW", "PIC506.RAW", "PIC507.RAW", "PIC508.RAW", "PIC509.RAW", "PIC510.RAW"}; // 176x220
char* files[10];

int picsize_x, picsize_y;
boolean display_rendertime=false;  // Set this to true if you want the rendertime to be displayed after a picture is loaded
boolean display_filename=false;  // Set this to false to disable showing of filename

word res;
long sm, em;

void setup()
{
    Serial.begin(9600);
    delay(250);
    myGLCD.InitLCD(PORTRAIT);
    myGLCD.clrScr();
    file.initFAT();
    myGLCD.setFont(BigFont);
    picsize_x=myGLCD.getDisplayXSize();
    picsize_y=myGLCD.getDisplayYSize();
    switch (picsize_y)
    {
    case 220:
        for (int z=0; z<sizeof(files220)/sizeof(*files220); z++)
            files[z] = files220[z];
        break;
    case 320:
        for (int z=0; z<sizeof(files320)/sizeof(*files320); z++)
            files[z] = files320[z];
        break;
    case 400:
        for (int z=0; z<sizeof(files400)/sizeof(*files400); z++)
            files[z] = files400[z];
        break;
    }
}

boolean isValidNumber(String str)
{
    boolean isNum=false;
    if(!(str.charAt(0) == '+' || str.charAt(0) == '-' || isDigit(str.charAt(0)))) return false;
    for(byte i=1; i<str.length(); i++)
    {
        if(!(isDigit(str.charAt(i)) || str.charAt(i) == '.')) return false;
    }
    return true;
}

void loop()
{
    while (Serial.available() > 0)
    {
        serial_char = Serial.read();
        if (serial_char == '\n')
        {
            if (txtMsg.length() > 3)
            {
                // check for TEXT lines
                // type fonttype color color color bcolor bcolor bcolor x y rotation
                // x X NNN NNN NNN nnn nnn nnn NNNN NNNN nnn xxxxxxxxxxxxxxxxxxxx
                // Font Type
                // 1 - Small, 2 - Big, 3 - Segment
                if (txtMsg.substring(0,1) == "T")
                {
                    if (textMsg.substring(1,1) == "S")
                    {
                        myGLCD.setFont(SmallFont);
                    }
                    else
                    {
                        if (textMsg.substring(1,1) == "B")
                        {
                            myGLCD.setFont(BigFont);
                        }
                        else
                        {
                            myGLCD.setFont(SevenSegNumFont);
                        }
                    }
                    // set text color
                    myGLCD.setColor(txtMsg.substring(2,3).toInt(), txtMsg.substring(5,3).toInt(), txtMsg.substring(8,3).toInt());
                    // set background text color
                    myGLCD.setBackColor(txtMsg.substring(11,3).toInt(), txtMsg.substring(14,3).toInt(), txtMsg.substring(17,3).toInt());
                    // print the line to screen
                    if isValidNumber(txtMsg.substring(29,(txtMsg.length() - 29)).toInt()))
                    {
                        myGLCD.printNumF(txtMsg.substring(29,(txtMsg.length() - 29)).toInt(), txtMsg.substring(20,3).toInt(), txtMsg.substring(23,3).toInt(), txtMsg.substring(26,3).toInt());
                    }
                    else
                    {
                        myGLCD.print(txtMsg.substring(29,(txtMsg.length() - 29)).toInt()), txtMsg.substring(20,3).toInt(), txtMsg.substring(23,3).toInt(), txtMsg.substring(26,3).toInt());
                    }
                }
                // check for BITMAP lines
                else
                {
                    // type char, image number
                    // xNNN
                    if (txtMsg.substring(0,1) == "B")
                    {
                        res=myFiles.loadBitmap(0, 0, picsize_x, picsize_y, files[txtMsg.substring(1,3).toInt()]);
                        if (res!=0)
                        {
                            if (res==0x10)
                            {
                                myGLCD.print("File not found...", 0, 0);
                                myGLCD.print(files[i], 0, 14);
                            }
                            else
                            {
                                myGLCD.print("ERROR: ", 0, 0);
                                myGLCD.printNumI(res, 56, 0);
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


    ****************************

    void loop()
    {
        int buf[318];
        int x, x2;
        int y, y2;
        int r;


        myGLCD.setColor(255, 0, 0);
        myGLCD.fillRect(0, 0, 319, 13);
        myGLCD.setColor(64, 64, 64);
        myGLCD.fillRect(0, 226, 319, 239);
        myGLCD.setColor(255, 255, 255);
        myGLCD.setBackColor(255, 0, 0);
        myGLCD.print("* Universal Color TFT Display Library *", CENTER, 1);
        myGLCD.setBackColor(64, 64, 64);
        myGLCD.setColor(255,255,0);
        myGLCD.print("<http://electronics.henningkarlsen.com>", CENTER, 227);

        myGLCD.setColor(0, 0, 255);
        myGLCD.drawRect(0, 14, 319, 225);

// Draw crosshairs
        myGLCD.setColor(0, 0, 255);
        myGLCD.setBackColor(0, 0, 0);
        myGLCD.drawLine(159, 15, 159, 224);
        myGLCD.drawLine(1, 119, 318, 119);
        for (int i=9; i<310; i+=10)
            myGLCD.drawLine(i, 117, i, 121);
        for (int i=19; i<220; i+=10)
            myGLCD.drawLine(157, i, 161, i);

// Draw sin-, cos- and tan-lines
        myGLCD.setColor(0,255,255);
        myGLCD.print("Sin", 5, 15);
        for (int i=1; i<318; i++)
        {
            myGLCD.drawPixel(i,119+(sin(((i*1.13)*3.14)/180)*95));
        }

        myGLCD.setColor(255,0,0);
        myGLCD.print("Cos", 5, 27);
        for (int i=1; i<318; i++)
        {
            myGLCD.drawPixel(i,119+(cos(((i*1.13)*3.14)/180)*95));
        }

        myGLCD.setColor(255,255,0);
        myGLCD.print("Tan", 5, 39);
        for (int i=1; i<318; i++)
        {
            myGLCD.drawPixel(i,119+(tan(((i*1.13)*3.14)/180)));
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);
        myGLCD.setColor(0, 0, 255);
        myGLCD.setBackColor(0, 0, 0);
        myGLCD.drawLine(159, 15, 159, 224);
        myGLCD.drawLine(1, 119, 318, 119);

// Draw a moving sinewave
        x=1;
        for (int i=1; i<(318*20); i++)
        {
            x++;
            if (x==319)
                x=1;
            if (i>319)
            {
                if ((x==159)||(buf[x-1]==119))
                    myGLCD.setColor(0,0,255);
                else
                    myGLCD.setColor(0,0,0);
                myGLCD.drawPixel(x,buf[x-1]);
            }
            myGLCD.setColor(0,255,255);
            y=119+(sin(((i*1.1)*3.14)/180)*(90-(i / 100)));
            myGLCD.drawPixel(x,y);
            buf[x-1]=y;
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);

// Draw some filled rectangles
        for (int i=1; i<6; i++)
        {
            switch (i)
            {
            case 1:
                myGLCD.setColor(255,0,255);
                break;
            case 2:
                myGLCD.setColor(255,0,0);
                break;
            case 3:
                myGLCD.setColor(0,255,0);
                break;
            case 4:
                myGLCD.setColor(0,0,255);
                break;
            case 5:
                myGLCD.setColor(255,255,0);
                break;
            }
            myGLCD.fillRect(70+(i*20), 30+(i*20), 130+(i*20), 90+(i*20));
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);

// Draw some filled, rounded rectangles
        for (int i=1; i<6; i++)
        {
            switch (i)
            {
            case 1:
                myGLCD.setColor(255,0,255);
                break;
            case 2:
                myGLCD.setColor(255,0,0);
                break;
            case 3:
                myGLCD.setColor(0,255,0);
                break;
            case 4:
                myGLCD.setColor(0,0,255);
                break;
            case 5:
                myGLCD.setColor(255,255,0);
                break;
            }
            myGLCD.fillRoundRect(190-(i*20), 30+(i*20), 250-(i*20), 90+(i*20));
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);

// Draw some filled circles
        for (int i=1; i<6; i++)
        {
            switch (i)
            {
            case 1:
                myGLCD.setColor(255,0,255);
                break;
            case 2:
                myGLCD.setColor(255,0,0);
                break;
            case 3:
                myGLCD.setColor(0,255,0);
                break;
            case 4:
                myGLCD.setColor(0,0,255);
                break;
            case 5:
                myGLCD.setColor(255,255,0);
                break;
            }
            myGLCD.fillCircle(100+(i*20),60+(i*20), 30);
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);

// Draw some lines in a pattern
        myGLCD.setColor (255,0,0);
        for (int i=15; i<224; i+=5)
        {
            myGLCD.drawLine(1, i, (i*1.44)-10, 224);
        }
        myGLCD.setColor (255,0,0);
        for (int i=224; i>15; i-=5)
        {
            myGLCD.drawLine(318, i, (i*1.44)-11, 15);
        }
        myGLCD.setColor (0,255,255);
        for (int i=224; i>15; i-=5)
        {
            myGLCD.drawLine(1, i, 331-(i*1.44), 15);
        }
        myGLCD.setColor (0,255,255);
        for (int i=15; i<224; i+=5)
        {
            myGLCD.drawLine(318, i, 330-(i*1.44), 224);
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);

// Draw some random circles
        for (int i=0; i<100; i++)
        {
            myGLCD.setColor(random(255), random(255), random(255));
            x=32+random(256);
            y=45+random(146);
            r=random(30);
            myGLCD.drawCircle(x, y, r);
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);

// Draw some random rectangles
        for (int i=0; i<100; i++)
        {
            myGLCD.setColor(random(255), random(255), random(255));
            x=2+random(316);
            y=16+random(207);
            x2=2+random(316);
            y2=16+random(207);
            myGLCD.drawRect(x, y, x2, y2);
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);

// Draw some random rounded rectangles
        for (int i=0; i<100; i++)
        {
            myGLCD.setColor(random(255), random(255), random(255));
            x=2+random(316);
            y=16+random(207);
            x2=2+random(316);
            y2=16+random(207);
            myGLCD.drawRoundRect(x, y, x2, y2);
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);

        for (int i=0; i<100; i++)
        {
            myGLCD.setColor(random(255), random(255), random(255));
            x=2+random(316);
            y=16+random(209);
            x2=2+random(316);
            y2=16+random(209);
            myGLCD.drawLine(x, y, x2, y2);
        }

        delay(2000);

        myGLCD.setColor(0,0,0);
        myGLCD.fillRect(1,15,318,224);

        for (int i=0; i<10000; i++)
        {
            myGLCD.setColor(random(255), random(255), random(255));
            myGLCD.drawPixel(2+random(316), 16+random(209));
        }

        delay(2000);

        myGLCD.fillScr(0, 0, 255);
        myGLCD.setColor(255, 0, 0);
        myGLCD.fillRoundRect(80, 70, 239, 169);

        myGLCD.setColor(255, 255, 255);
        myGLCD.setBackColor(255, 0, 0);
        myGLCD.print("That's it!", CENTER, 93);
        myGLCD.print("Restarting in a", CENTER, 119);
        myGLCD.print("few seconds...", CENTER, 132);

        myGLCD.setColor(0, 255, 0);
        myGLCD.setBackColor(0, 0, 255);
        myGLCD.print("Runtime: (msecs)", CENTER, 210);
        myGLCD.printNumI(millis(), CENTER, 225);

        delay (10000);
    }
