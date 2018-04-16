//
//  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>
//
//  This program is free software; you can redistribute it and/or
//  modify it under the terms of the GNU General Public License
//  version 2, as published by the Free Software Foundation.
//
//  This program is distributed in the hope that it will be useful, but
//  WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
//  General Public License version 2 for more details.
//
//  You should have received a copy of the GNU General Public License
//  version 2 along with this program; if not, write to the Free
//  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
//  MA 02110-1301, USA.
//

#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"
#include <SoftwareSerial.h>

Adafruit_MotorShield AFMSbottom(0x60);

// define the stepper motors
Adafruit_StepperMotor *stepper_cd_spinner = AFMSbottom.getStepper(200, 1);
Adafruit_StepperMotor *stepper_move_arm_horizontal = AFMSbottom.getStepper(200, 2);
Adafruit_StepperMotor *stepper_move_arm_vertical = AFMSbottom.getStepper(200, 3);
SoftwareSerial robobuff_serial(10, 11); // RX, TX

// steppers forward and reverse code
void stepper_cd_spinner_forward()
{
    stepper_cd_spinner->onestep(FORWARD, MICROSTEP);
}

void stepper_cd_spinner_backward()
{
    stepper_cd_spinner->onestep(BACKWARD, MICROSTEP);
}

void stepper_arm_horizontal_forward()
{
    stepper_move_arm_horizontal->onestep(FORWARD, MICROSTEP);
}

void stepper_arm_horizontal_backward()
{
    stepper_move_arm_horizontal->onestep(BACKWARD, MICROSTEP);
}

void stepper_arm_vertical_forward()
{
    stepper_move_arm_vertical->onestep(FORWARD, MICROSTEP);
}

void stepper_arm_vertical_backward()
{
    stepper_move_arm_vertical->onestep(BACKWARD, MICROSTEP);
}

// setup the accellstepper
AccelStepper Accelstepper_cd_spinner(stepper_cd_spinner_forward, stepper_cd_spinner_backward);
AccelStepper Accelstepper_move_arm_horizontal(stepper_arm_horizontal_forward, stepper_arm_horizontal_backward);
AccelStepper Accelstepper_move_arm_vertical(stepper_arm_vertical_forward, stepper_arm_vertical_backward);

void setup()
{
    AFMSbottom.begin(); // Start the bottom board
    // Setup cd spinner motor
    Accelstepper_cd_spinner.setMaxSpeed(100.0);
    Accelstepper_cd_spinner.setAcceleration(100.0);
    Accelstepper_cd_spinner.moveTo(24);
    // setup move horizontal motor
    Accelstepper_move_arm_horizontal.setMaxSpeed(200.0);
    Accelstepper_move_arm_horizontal.setAcceleration(100.0);
    Accelstepper_move_arm_horizontal.moveTo(50000);
    // setup move vertical motor
    Accelstepper_move_arm_vertical.setMaxSpeed(200.0);
    Accelstepper_move_arm_vertical.setAcceleration(100.0);
    Accelstepper_move_arm_vertical.moveTo(50000);
    // line serial communication
    robobuff_serial.begin(1200);
}

void loop()
{
    // Change direction at the limits
    if (Accelstepper_cd_spinner.distanceToGo() == 0)
        Accelstepper_cd_spinner.moveTo(-Accelstepper_cd_spinner.currentPosition());

    if (Accelstepper_move_arm_horizontal.distanceToGo() == 0)
        Accelstepper_move_arm_horizontal.moveTo(-Accelstepper_move_arm.currentPosition());

    Accelstepper_cd_spinner.run();
    Accelstepper_move_arm_horizontal.run();
    if (robobuff_serial.available())
        Serial.write(robobuff_serial.read());
    if (Serial.available())
        robobuff_serial.write(Serial.read());
}
