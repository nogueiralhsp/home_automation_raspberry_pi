#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h> 

// used to debug on Development
//#include <LiquidCrystal_I2C.h>
//LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

#define ONE_WIRE_BUS 4

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

 float Celcius=0;
 bool clean = true;
 unsigned int millisOld =0;
/***************************************************/

void setup() {
  // initialize the serial communication:
  Serial.begin(9600);

  sensors.begin();

// used to debug on Development
//  lcd.init(); // initialize the lcd 
//  lcd.init();
//  // Print a message to the LCD.
//  lcd.backlight();
//
//  lcd.setCursor(0,0);
//  lcd.print("Room Temperature"); 
}
void loop() {
  
  byte brightness;

  sensors.requestTemperatures(); 
  Celcius=sensors.getTempCByIndex(0);


  if (millis()> millisOld+1000){
    Serial.println(Celcius);//sends celcius value to serial port
    
//used to debug on i2c display
//    //display printing
//    lcd.setCursor(0,1);
//    lcd.print(Celcius);    
//    lcd.setCursor(5,1);
//    lcd.print(" C");
  }
  
}
