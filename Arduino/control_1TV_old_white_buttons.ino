// This is for compatibility with both arduino 1.0 and previous versions
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#include <Wire.h>
#include <DS1307.h> // by "mattt" from the Arduino forum and modified by D. Sjunnesson
#include <IRremote.h>

IRsend irsend;

// setting pin constants
const int usbScanPin = 8;    // input, connected to the button
const int ledPin =  13;      // output, connects to the LED

// variables
int usbState = 0;         // var for saving the button's state
int count = 0;       // counter of time(loops)
int TV_Sleep = 0;    // "sleep" mode of TV
int TV_Work = 0;     // "work" mode of TV

void setup()
{
  Serial.begin(9600); // default speed of 9600 bps
  // initialisation of pin, connected to LED as OUTPUT
  pinMode(ledPin, OUTPUT);
  // initialisation of pin, connected to USB as INPUT
  pinMode(usbScanPin, INPUT);

  // Setting time to RTC (DS-1302, DS-1307, DS-3231 etc.)
  RTC.stop(); // 
  RTC.set(DS1307_SEC,0);        //set the seconds
  RTC.set(DS1307_MIN,33);     //set the minutes
  RTC.set(DS1307_HR,19);       //set the hours
  RTC.set(DS1307_DOW,1);       //set the day of the week
  RTC.set(DS1307_DATE,5);       //set the date
  RTC.set(DS1307_MTH,6);        //set the month
  RTC.set(DS1307_YR,23);         //set the year
  RTC.start(); // */
}

void loop()
{
  Serial.print("\n");
  Serial.print(RTC.get(DS1307_HR, true)); //read the hour and also update all the values by pushing in true
  Serial.print(":");
  Serial.print(RTC.get(DS1307_MIN, false)); //read minutes without update (false)
  Serial.print(":");
  Serial.print(RTC.get(DS1307_SEC, false)); //read seconds
  Serial.print(", day ");             
  Serial.print(RTC.get(DS1307_DOW, false)); //read the day of week

  usbState = digitalRead(usbScanPin); // reading USB state


  // waiting for 8.3 seconds, some TVs require slightly more than 6 seconds
  if ((usbState == HIGH) && (TV_Sleep == 0) && (TV_Work == 0))
  {
    count++;
    Serial.print("   sleep counter  ");
    Serial.print(count);
  }


  // fixing the moment of switching TV to sleep mode, when delay is 4 .. 9 seconds 
  if ((usbState == LOW) && (TV_Sleep == 0) && (TV_Work == 0) && (count >= 8) && (count <= 18))
  {
    Serial.print("\nTV is in sleep mode now");
    TV_Sleep = 1; // change TV_Sleep from 0 to 1
    count = 0; // reset the counter

    // if Work Time from 9:00:00 to 20:58:59 then turn ON 
    // here 1:01 is reserve time for turning ON and booting up TV
    // divide working time range for 2 subranges: 9:00:00 --- 19:59:59 and 20:00:00 --- 20:58:59

    if (   ( ((RTC.get(DS1307_HR, false)) >= 9) && ((RTC.get(DS1307_HR, false)) < 20) ) || ( ((RTC.get(DS1307_HR, false)) == 20) && ((RTC.get(DS1307_MIN, false)) < 59) )   )

    {
      Serial.print("\nStart call");
      delay (500); // 500 reserve msec delay
      start ();    // calling start function
      TV_Work = 1;  // updating state of TV_Work flag
      TV_Sleep = 0;  // updating state of TV_Sleep flag
    }
  }


  // ordinary operating mode
  // turning ON 9:00:00
  if (((RTC.get(DS1307_HR, false)) == 9) && ((RTC.get(DS1307_MIN, false)) == 00) && ((RTC.get(DS1307_SEC, false)) == 00) && (TV_Sleep == 1))
  {
    Serial.print("\nStarting now - 9:00");
    start ();
    TV_Work = 1;
    TV_Sleep = 0;
  }

  // turning OFF 21:00:00
  if (((RTC.get(DS1307_HR, false)) == 21)  && ((RTC.get(DS1307_MIN, false)) == 00) && ((RTC.get(DS1307_SEC, false)) == 00) && (TV_Work == 1))
  {
    Serial.print("\nOff now - 21:00");
    stop ();
    TV_Work = 0;
    TV_Sleep = 1;
  }

  delay (500); // 500 msec = time length of one loop: 1 sec = "counter == 2"
}


// function for turning ON
void start ()
{
  Serial.print("\nSTART WORK: IR_start");
  irsend.sendNEC(0x10EF30CF, 32); // TV On / Off
  Serial.print("\nwaiting of loading TV 12 sec");
  delay (20000);//delay (12000);
  irsend.sendNEC(0x10EFA857, 32); // wright arrow
  delay (200);
  irsend.sendNEC(0x10EFA857, 32); // wright arrow
  delay (200);
  irsend.sendNEC(0x10EF28D7, 32); // OK Central
  delay (200);
  irsend.sendNEC(0x10EF28D7, 32); // OK Central
  delay (200);
  irsend.sendNEC(0x10EFA857, 32); // wright arrow
  delay (500);
  irsend.sendNEC(0x10EF28D7, 32); // OK Central (play)

  // Sound Volume level
  //irsend.sendNEC(0x10EF8877, 32); // Volume "-"
  //irsend.sendNEC(0x10EF08F7, 32); // Volume "+"

  Serial.print("\nSystem started");

  /*Serial.print("\nStart\n");
  digitalWrite(ledPin, HIGH);*/
  return;
}

// function for turning OFF
void stop ()
{
  Serial.print("\nSTOP WORK: IR_stop");
  irsend.sendNEC(0x10EF30CF, 32); // TV On / Off
  return;
}
