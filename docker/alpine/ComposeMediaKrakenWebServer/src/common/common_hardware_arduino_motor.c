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

#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"

Adafruit_MotorShield AFMSbottom(0x60); // Default address, no jumpers

// Connect two steppers with 200 steps per revolution (1.8 degree) to the bottom shield
Adafruit_StepperMotor *QueenStepper = AFMSbottom.getStepper(200, 1);
//Adafruit_StepperMotor *myStepper2 = AFMSbottom.getStepper(200, 2);

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
// wrappers for the first motor!
void QueenForwardStep_Single()
{
    QueenStepper->onestep(FORWARD, SINGLE);
}

void QueenBackwardStep_Single()
{
    QueenStepper->onestep(BACKWARD, SINGLE);
}
/*
// wrappers for the second motor!
void forwardstep2()
{
    myStepper2->onestep(FORWARD, DOUBLE);
}

void backwardstep2()
{
    myStepper2->onestep(BACKWARD, DOUBLE);
}
*/
// Now we'll wrap the 2 steppers in an AccelStepper object
AccelStepper AccelQueenStepper(QueenForwardStep_Single, QueenBackwardStep_Single);
//AccelStepper stepper2(forwardstep2, backwardstep2);

void setup()
{
    AFMSbottom.begin(); // Start the bottom shield
    AccelQueenStepper.setMaxSpeed(100.0);
    AccelQueenStepper.setAcceleration(100.0);
    AccelQueenStepper.moveTo(24);

//    stepper2.setMaxSpeed(200.0);
//    stepper2.setAcceleration(100.0);
//    stepper2.moveTo(50000);
}

void loop()
{
    // Change direction at the limits
    if (AccelQueenStepper.distanceToGo() == 0)
        AccelQueenStepper.moveTo(-AccelQueenStepper.currentPosition());

//    if (stepper2.distanceToGo() == 0)
//        stepper2.moveTo(-stepper2.currentPosition());

    AccelQueenStepper.run();
//    stepper2.run();
}
