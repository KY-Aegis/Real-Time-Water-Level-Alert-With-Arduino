#include <Wire.h>           //import wire library
#include <LCD_I2C.h>        //import lcd library
LCD_I2C lcd(0x27, 16, 2);   //initialize the lcd
int sensorVal=0;            //variable to store sensor value
int sensorPin=A4;           //variable for sensor pin
int lowerLimit=600;         //declare the lowerLimit
int upperLimit=650;         //declare the upperLimit
int red=0;                  //declare the pin for the red LED
int yellow=1;               //declare the pin for the yellow LED
int green=2;                //declare the pin for the green LED

void setup(){               //function to initialize I/O
  Serial.begin(9600);       //initialize the serial import
  lcd.begin();              //start the led
  lcd.backlight();          //on the backlight of the led
  for (int i=8;i<11;i++){   //loop 3 times to activate the pins
    pinMode(i,OUTPUT);      //initialize the pin i as output
  }
  
}

void lightUp(int light){        //function to control the pattern of the LEDs
  for (int i=8;i<11;i++){       //loop 3 times
    if (i!=light){              //if i is not equals to the pin passed from the main function
      digitalWrite(i,LOW);      //turn off the other LED
    }
    else{                       //if i is equals to the pin passed from the main function
      digitalWrite(i,HIGH);     //turn on the LED
    }
  }
}

void loop(){                            //main function
  sensorVal=analogRead(sensorPin);      //read the analog pin
  lcd.clear();                          //clear the output of the LCD
  lcd.print("Water level:");            //display water level on the LCD
  lcd.setCursor(0,1);                   //start a new line on the LCD
  Serial.println(sensorVal);            //print the water level at the serial monitor
  if (sensorVal>-1 && sensorVal<=20){   //if the value is between 0 and 20
    lcd.print("Empty");                 //display Empty on the LCD
    lightUp(8);                         //light up the red LED
    delay(500);                         //delay for 500 milliseconds
  }
  else if (sensorVal>20 && sensorVal<=lowerLimit){//if the value is between 21 and lowerLimit
    lcd.print("Low");   //display Low on the LCD
    lightUp(8);         //light up the red LED
    delay(500);         //delay for 500 milliseconds
  }
  else if (sensorVal>lowerLimit && sensorVal<=upperLimit){//if the value is between lowerLimit and upperlimit
    lcd.print("Normal");    //display Normal on the LCD
    lightUp(9);             //light up the yellow LED
    delay(500);             //delay for 500 milliseconds
  }
  else if (sensorVal>upperLimit){//if the value is more than the upperlimit
    lcd.print("Full");  //display Full on the LCD
    lightUp(10);        //light up the green LED
    delay(500);         //delay for 500 milliseconds
  } 
}
