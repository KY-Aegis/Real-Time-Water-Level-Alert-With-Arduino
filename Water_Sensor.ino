#include <Wire.h>
#include <LCD_I2C.h>
LCD_I2C lcd(0x27, 16, 2);
int sensorVal=0;//variable to store sensor value
int sensorPin=A4;//variable for sensor pin
int lowerLimit=600;
int upperLimit=650;
int red=0;
int yellow=1;
int green=2;

void setup(){
  Serial.begin(9600);
  lcd.begin();
  lcd.backlight();
  for (int i=8;i<11;i++){
    pinMode(i,OUTPUT); 
  }
  
}

void lightUp(int light){
  for (int i=8;i<11;i++){
    if (i!=light){
      digitalWrite(i,LOW);
    }
    else{
      digitalWrite(i,HIGH);
    }
  }
}
void loop(){
  sensorVal=analogRead(sensorPin);//read the analog on pin A5
  lcd.clear();
  lcd.print("Water level:");
  lcd.setCursor(0,1); 
  Serial.println(sensorVal);
  if (sensorVal>-1 && sensorVal<=20){ 
    lcd.print("Empty");
    lightUp(8);
    delay(500);
  }
  else if (sensorVal>20 && sensorVal<=lowerLimit){ 
    lcd.print("Low");
    lightUp(8);
    delay(500);
  }
  else if (sensorVal>lowerLimit && sensorVal<=upperLimit){ 
    lcd.print("Normal");
    lightUp(9);
    delay(500);
  }
  else if (sensorVal>upperLimit){  
    lcd.print("Full");
    lightUp(10);
    delay(500);
  } 
}
