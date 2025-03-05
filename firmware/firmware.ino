#include <Servo.h>
#include <Wire.h>

// Variables to store previous error values for X and Y axes
float previous_error_x = 0;  
float previous_error_y = 0;  

// Control loop period for X and Y axes
int period_x = 1;            
int period_y = 1;            

// Servo angles for X and Y axes
int servoAngleX, servoAngleY; 

// Variable to store the previous time for timing control
unsigned long previousMillis = 0; 

// Define servo control pins
static const int servoPin1 = 16; // Control pin for servo 1
static const int servoPin2 = 17; // Control pin for servo 2

// Create servo objects
Servo servo1; 
Servo servo2; 

// Define error variables
float x_error = -1, y_error = -1; // Initial error values for X and Y axes

void setup() {
  // Initialize Serial communication with a baud rate of 115200
  Serial.begin(115200);
  
  // Attach servos to their respective pins
  servo1.attach(servoPin1); 
  servo2.attach(servoPin2); 
  
  // Set initial servo angles
  servo1.write(55); 
  servo2.write(55); 
}

void loop() {
  unsigned long currentMillis = millis();  // Get the current time
  
  // Check if enough time has passed
  if (currentMillis - previousMillis >= 1) { 
    previousMillis = currentMillis; // Update the previous time
    processData(); // Process incoming Serial data
    
    // Update the servo angles based on error values
    servo1.write(x_error); 
    processData(); // Process Serial data again
    servo2.write(y_error); 
  }
}

void processData() {
  // Check if there is available data from Serial
  if (Serial.available() > 0) { 
    String input = Serial.readStringUntil('\n'); // Read the input string until a newline character (\n)
    
    // Check if the ball is detected
    if (input == "no") {
      x_error = -1; // If no ball is detected, set X-axis error to -1
      y_error = -1; // If no ball is detected, set Y-axis error to -1
    } else {
      // Split the input string into X and Y components
      int separatorIndex = input.indexOf('x'); // Find the position of the 'x' separator
      if (separatorIndex != -1) { // Check if the separator exists
        String x_str = input.substring(0, separatorIndex); // Extract the X part
        String y_str = input.substring(separatorIndex + 1); // Extract the Y part
  
        // Convert X and Y values from String to float
        x_error = (float)x_str.toInt(); 
        y_error = (float)y_str.toInt(); 
      }
    }
  }
}
