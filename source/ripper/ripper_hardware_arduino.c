#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <SoftwareSerial.h>

#define water_pin 5
#define vaccuum_pin 6
#define home_switch_spindle 7   // Pin 7 connected to Home Switch (MicroSwitch)
#define home_switch_arm 8       // Pin 8 connected to Home Switch (MicroSwitch)
#define home_switch_track 9     // Pin 9 connected to Home Switch (MicroSwitch)
long initial_arm_homing = -1;   // Used to Home Stepper at startup
long initial_track_homing = -1; // Used to Home Stepper at startup
char serialdata[20];

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

void arm_home()
{
  // home the arm
  while (digitalRead(home_switch_arm))
  {                                              // Make the Stepper move CCW until the switch is activated
    Accelstepper_arm.moveTo(initial_arm_homing); // Set the position to move to
    initial_arm_homing--;                        // Decrease by 1 for next move if needed
    Accelstepper_arm.run();                      // Start moving the stepper
    delay(5);
  }
  Accelstepper_arm.setCurrentPosition(0);  // Set the current position as zero for now
  Accelstepper_arm.setMaxSpeed(100.0);     // Set Max Speed of Stepper (Slower to get better accuracy)
  Accelstepper_arm.setAcceleration(100.0); // Set Acceleration of Stepper
  initial_arm_homing = 1;
  while (!digitalRead(home_switch_arm))
  { // Make the Stepper move CW until the switch is deactivated
    Accelstepper_arm.moveTo(initial_arm_homing);
    Accelstepper_arm.run();
    initial_arm_homing++;
    delay(5);
  }
  Accelstepper_arm.setCurrentPosition(0);
}

void track_home()
{
  // home the track
  while (digitalRead(home_switch_track))
  {                                                  // Make the Stepper move CCW until the switch is activated
    Accelstepper_track.moveTo(initial_track_homing); // Set the position to move to
    initial_track_homing--;                          // Decrease by 1 for next move if needed
    Accelstepper_track.run();                        // Start moving the stepper
    delay(5);
  }
  Accelstepper_track.setCurrentPosition(0);  // Set the current position as zero for now
  Accelstepper_track.setMaxSpeed(100.0);     // Set Max Speed of Stepper (Slower to get better accuracy)
  Accelstepper_track.setAcceleration(100.0); // Set Acceleration of Stepper
  initial_track_homing = 1;
  while (!digitalRead(home_switch_track))
  { // Make the Stepper move CW until the switch is deactivated
    Accelstepper_track.moveTo(initial_track_homing);
    Accelstepper_track.run();
    initial_track_homing++;
    delay(5);
  }
  Accelstepper_track.setCurrentPosition(0);
}

// setup the devices and home them
void setup()
{
  AFMSbottom.begin(); // Start the bottom board
  // Setup cd spinner motor
  Accelstepper_cd_spinner.setMaxSpeed(400.0);
  Accelstepper_cd_spinner.setAcceleration(100.0);
  // line serial communication
  ripper_serial.begin(1200);
  arm_home();
  track_home();
}

// begin main loop
void loop()
{
  while (ripper_serial.available() > 0)
  {
    String serialdata = ripper_serial.readStringUntil('|');
    if (serialdata == "arm")
    {
      Accelstepper_arm.moveTo(ripper_serial.parseInt());
      Accelstepper_arm.run();
    }
    else if (serialdata == "track")
    {
      Accelstepper_track.moveTo(ripper_serial.parseInt());
      Accelstepper_track.run();
    }
    else if (serialdata == "pickup")
    {
      while (digitalRead(home_switch_spindle))
      {
        Accelstepper_arm.moveTo(initial_arm_homing);
        initial_arm_homing--;
        Accelstepper_arm.run();
        delay(5);
      }
      digitalWrite(vaccuum_pin, HIGH);
      arm_home();
    }
    else if (serialdata == "drop")
    {
      Accelstepper_arm.moveTo(ripper_serial.parseInt());
      Accelstepper_arm.run();
      digitalWrite(vaccuum_pin, LOW);
      arm_home();
    }
    else
    {
      // stepper_to_move = Accelstepper_cd_spinner;
    }
  }
}
