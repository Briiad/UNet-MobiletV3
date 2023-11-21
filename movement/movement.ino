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
int pwm_speed[4] = {0, 0, 0, 0};
int max_left = 40;
int max_right = 40 * 0.9;
int state = 0;
int last_state = 0;
int spam_counter = 0;

void forward(){
  pwm_speed[1] = 0;
  pwm_speed[3] = 0;
  pwm_speed[0] += 10;
  pwm_speed[2] += 10;
  pwm_speed[0] = pwm_speed[0] > max_left ? max_left : pwm_speed[0];
  pwm_speed[2] = pwm_speed[2] > max_right ? max_right : pwm_speed[2];
  return;
}

void backward(){
  pwm_speed[0] -= 10;
  pwm_speed[2] -= 10;
  pwm_speed[1] = 40 * 0.86;
  pwm_speed[3] = 40;
  pwm_speed[0] = pwm_speed[0] < 0 ? 0 : pwm_speed[0];
  pwm_speed[2] = pwm_speed[2] < 0 ? 0 : pwm_speed[2];
}

void stop(){
  pwm_speed[0] -=10;
  pwm_speed[1] -=10;
  pwm_speed[2] -=10;
  pwm_speed[3] -=10;
  pwm_speed[0] = pwm_speed[0] < 0 ? 0 : pwm_speed[0];
  pwm_speed[1] = pwm_speed[1] < 0 ? 0 : pwm_speed[1];
  pwm_speed[2] = pwm_speed[2] < 0 ? 0 : pwm_speed[2];
  pwm_speed[3] = pwm_speed[3] < 0 ? 0 : pwm_speed[3];
  return;
}

void right(){
  pwm_speed[1] = 0;
  pwm_speed[3] = 0;
  pwm_speed[0] -= 40;
  pwm_speed[2] += 40;
  pwm_speed[0] = pwm_speed[0] < 0 ? 0 : pwm_speed[0];
  pwm_speed[2] = pwm_speed[2] > max_right ? max_right : pwm_speed[2];
  return;
}

void left(){
  pwm_speed[1] = 0;
  pwm_speed[3] = 0;
  pwm_speed[0] += 40;
  pwm_speed[2] -= 40;
  pwm_speed[0] = pwm_speed[0] > max_left ? max_left : pwm_speed[0];
  pwm_speed[2] = pwm_speed[2] < 0 ? 0 : pwm_speed[2];
  return;
}

void loop(){
  if (Serial.available() > 0){
    state = Serial.readString().toInt();
  }

  // State Read
  switch(state){
    case 0: stop(); break;
    case 1: forward(); break;
    case 2: left(); break;
    case 3: right(); break;
    case 4: backward(); break;
    default: break;
  }

  // PWM Write
  if (state != last_state){
    spam_counter = 0;
  }

  if (spam_counter < 10){
    analogWrite(PWM_0, pwm_speed[0]);
    analogWrite(PWM_1, pwm_speed[1]);
    analogWrite(PWM_2, pwm_speed[2]);
    analogWrite(PWM_3, pwm_speed[3]);
    spam_counter++;
  }

  last_state = state;
  delay(100);
}
