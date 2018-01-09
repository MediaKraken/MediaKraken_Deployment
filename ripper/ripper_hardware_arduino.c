//
//  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>
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

// the track/arm motor shield
Adafruit_MotorShield AFMSbottom(0x60);

// define the stepper motors
Adafruit_StepperMotor *stepper_cd_spinner = AFMSbottom.getStepper(200, 1);
Adafruit_StepperMotor *stepper_track = AFMSbottom.getStepper(200, 2);
Adafruit_StepperMotor *stepper_arm = AFMSbottom.getStepper(200, 3);

// define serial communication ports
SoftwareSerial ripper_serial(10, 11); // RX, TX

// setup the accellstepper
AccelStepper Accelstepper_cd_spinner(stepper_cd_spinner->onestep(FORWARD, MICROSTEP), stepper_cd_spinner->onestep(BACKWARD, MICROSTEP));
AccelStepper Accelstepper_track(stepper_track->onestep(FORWARD, MICROSTEP), stepper_track->onestep(BACKWARD, MICROSTEP));
AccelStepper Accelstepper_arm(stepper_arm->onestep(FORWARD, MICROSTEP), stepper_arm->onestep(BACKWARD, MICROSTEP));

# setup the devices and home them
void setup()
{
    AFMSbottom.begin(); // Start the bottom board
    // Setup cd spinner motor
    Accelstepper_cd_spinner.setMaxSpeed(100.0);
    Accelstepper_cd_spinner.setAcceleration(100.0);
    Accelstepper_cd_spinner.moveTo(24);
    // setup move track motor
    Accelstepper_track.setMaxSpeed(200.0);
    Accelstepper_track.setAcceleration(100.0);
    Accelstepper_track.moveTo(50000);
    // setup move arm motor
    Accelstepper_arm.setMaxSpeed(200.0);
    Accelstepper_arm.setAcceleration(100.0);
    Accelstepper_arm.moveTo(50000);
    // line serial communication
    ripper_serial.begin(1200);
}

// begin main loop
void loop()
{
    while (ripper_serial.available() > 0)
    {
        serial_char = ripper_serial.read();
        if (serial_char == '\n')
        {
            if (txtMsg.length() > 3)
            {
                // check for wipe mode
                if (txtMsg.substring(0,1) == "W")
                {

                }
            }
            txtMsg = "";
        }
        else
        {
            txtMsg.concat(serial_char);
        }
    }
}
