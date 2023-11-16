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
  Serial.begin(9600);
  Serial.setTimeout(0.1);
}

// GLOBAL VARIABLES
int pmw_speed[4] = {0, 0, 0, 0};
int max_left = 30;
int max_right = 30 * 0.92;
int state = 0;
int last_state = 0;
int spam_counter = 0;

void forward(){
  pmw_speed[0] += 10;
  pmw_speed[2] += 10;
  pmw_speed[0] = pmw_speed[0] > max_left ? max_left : pmw_speed[0];
  pmw_speed[2] = pmw_speed[2] > max_right ? max_right : pmw_speed[2];
  return;
}

void backward(){
  pmw_speed[1] = 40;
  pmw_speed[3] = 40;
}

void stop(){
  pmw_speed[0] -=10;
  pmw_speed[1] -=10;
  pmw_speed[2] -=10;
  pmw_speed[3] -=10;
  pmw_speed[0] = pmw_speed[0] < 0 ? 0 : pmw_speed[0];
  pmw_speed[1] = pmw_speed[1] < 0 ? 0 : pmw_speed[1];
  pmw_speed[2] = pmw_speed[2] < 0 ? 0 : pmw_speed[2];
  pmw_speed[3] = pmw_speed[3] < 0 ? 0 : pmw_speed[3];
  return;
}

void right(){
  pmw_speed[0] -= 40;
  pmw_speed[2] += 40;
  pmw_speed[0] = pmw_speed[0] < 0 ? 0 : pmw_speed[0];
  pmw_speed[2] = pmw_speed[2] > max_right ? max_right : pmw_speed[2];
  return;
}

void left(){
  pmw_speed[0] += 40;
  pmw_speed[2] -= 40;
  pmw_speed[0] = pmw_speed[0] > max_left ? max_left : pmw_speed[0];
  pmw_speed[2] = pmw_speed[2] < 0 ? 0 : pmw_speed[2];
  return;
}

void loop(){
  if (Serial.available() > 0){
    state = Serial.readString().toInt();

    // State Read
    switch(state){
      case 0: stop(); break;
      case 1: forward(); break;
      case 2: left(); break;
      case 3: right(); break;
      default: break;
    }

    // PWM Write
    if (state != last_state){
      spam_counter = 0;
    }

    if (spam_counter < 10){
      analogWrite(PWM_0, pmw_speed[0]);
      analogWrite(PWM_1, pmw_speed[1]);
      analogWrite(PWM_2, pmw_speed[2]);
      analogWrite(PWM_3, pmw_speed[3]);
      spam_counter++;
    }

    last_state = state;
    delay(10);
  }
}