#include <Arduino.h>

#define PWM_0 5
#define PWM_1 6
#define PWM_2 9
#define PWM_3 10

void setup() {
  pinMode(PWM_0, OUTPUT);
  pinMode(PWM_1, OUTPUT);
  pinMode(PWM_2, OUTPUT);
  pinMode(PWM_3, OUTPUT);
  Serial.begin(115200);
  Serial.setTimeout(0.1);
}

// GLOBAL VARIABLES
int pmw_speed[4] = {0, 0, 0, 0};
int max_left = 40 * 0.86;
int max_right = 40;
int state = 0;
int last_state = 0;
int spam_counter = 0;

void forward(){
  pmw_speed[0] = max_left;
  pmw_speed[2] = max_right;
  return;
}

// Backward, Im using IBT H-Bridge
void backward(){
  pmw_speed[1] = max_left;
  pmw_speed[3] = max_right;
}

void stop(){
  pmw_speed[0] = 0;
  pmw_speed[1] = 0;
  pmw_speed[2] = 0;
  pmw_speed[3] = 0;
  return;
}

void right(){
  pmw_speed[0] = 0;
  pmw_speed[2] = max_right;
  return;
}

void left(){
  pmw_speed[0] = max_left;
  pmw_speed[2] = 0;
  return;
}

void loop(){
  if (Serial.available() > 0){
    char input = Serial.read();

    switch(input){
      case 'w':
        forward();
        state = 1;
        break;
      case 's':
        stop();
        state = 0;
        break;
      case 'a':
        left();
        state = 2;
        break;
      case 'd':
        right();
        state = 3;
        break;
      case 'q':
        backward();
        state = 4;
        break;
      default:
        break;
    }
  }
  // PWM Write
  analogWrite(PWM_0, pmw_speed[0]);
  analogWrite(PWM_1, pmw_speed[1]);
  analogWrite(PWM_2, pmw_speed[2]);
  analogWrite(PWM_3, pmw_speed[3]);

  Serial.println(String(speed[0]) + "+" + String(speed[1]) + "+" + String(speed[2]) + "+" + String(speed[3]));
}