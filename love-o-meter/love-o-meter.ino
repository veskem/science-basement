#include <LiquidCrystal.h>

// Setup the LiquidCrystal library with the pin numbers we have
// physically connected the module to.
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

// The analog pin the TMP36's Vout (sense) pin is connected to.
// The resolution is 10 mV / degree centigrade with a 
// 500 mV offset to allow for negative temperatures.
const int temperature_pin = 0;     

const int period = 500;     // total cycle length in ms
const int n_samples = 100;  // # samples to be averaged

void setup() {
    lcd.begin(16, 2);   // Setup # LCD columns and rows
    Serial.begin(9600); // specify serial port baud rate
}

void loop() {
    // make several measurements to reduce the noise
    float temperature = 0.0;
    for (int i = 0; i < n_samples; ++i) {
        int adc_reading = analogRead(temperature_pin);  
        float voltage = adc_reading * 5.0 / 1024.0;
        temperature += (voltage - 0.5) * 100 ;
        delay(0.5);
    }
    temperature *= 1.0 / n_samples;
    
    // write the measurement results to LCD                              
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("  Temp= ");
    lcd.print(temperature, 1);
    lcd.print("C");

    lcd.setCursor(0, 1);
    lcd.print("  t= ");
    lcd.print(millis() / 1000, 10);
    lcd.print("sec");

    // write the measurement results to serial port     
    Serial.println(temperature);

    // wait before the next loop
    delay(period - (millis() % period));
}






 
 



