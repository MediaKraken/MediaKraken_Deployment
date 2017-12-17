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

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <SoftwareSerial.h>

Adafruit_PWMServoDriver robobuff_servo_manager = Adafruit_PWMServoDriver();
SoftwareSerial robobuff_serial(10, 11); // RX, TX

#define SERVOMIN  100
#define SERVOMAX  750

void setup() {
  // usb port debugger
  Serial.begin(9600);
  Serial.println("Stepper Code Start");
  robobuff_servo_manager.begin();
  robobuff_servo_manager.setPWMFreq(60);
  // line serial communication
  robobuff_serial.begin(4800);
}

void setServoPulse(uint8_t servo_num, double pulse) {
  double pulselength;
  pulselength = 1000000;
  pulselength /= 60;
  pulselength /= 4096;
  pulse *= 1000;
  pulse /= pulselength;
  Serial.println(pulse);
  robobuff_servo_manager.setPWM(servo_num, 0, pulse);
}

void loop() {
  if (robobuff_serial.available())
    Serial.write(robobuff_serial.read());
  if (Serial.available())
    robobuff_serial.write(Serial.read());
}
