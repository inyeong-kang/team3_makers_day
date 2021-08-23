/*코드 요약
 동일한 규격의 개체(박스)들이 있다.
 초음파 센서와 개체 간의 거리가 10cm 이하면 빨간색 led로 경고, "FULL" 이라고 Serial 창에 표시
 20cm 이하면 노란색 led로 경고, "OKAY"
 30cm 이하면 초록색, "GOOD"
 30cm 초과면 EMPTY
 Serial 창에 거리에 따른 셔츠 개수(재고) 표시
*/
#include <Servo.h> // 서보모터 라이브러리 사용
Servo servo;  // 서보모터 객체를 servo로 생성
Servo servo1;
Servo servo2;

int TRIG = 6;
int ECHO = 7;

int RED = 8;
int YELLOW = 9;
int GREEN = 10;

int servoPin = 11;
int servoPin1 = 4;
int servoPin2 = 12;

int angle = 0; // servo position in degrees 

int shirt=3;
float distance=10;

void setup(){

 Serial.begin(9600);
 pinMode(TRIG,OUTPUT);
 pinMode(ECHO,INPUT);
 pinMode(RED,OUTPUT);
 pinMode(GREEN,OUTPUT);
 pinMode(YELLOW,OUTPUT);

 servo.attach(servoPin); //서보 12핀에 연결
 servo1.attach(servoPin1);
 servo2.attach(servoPin2);
}


void loop(){

  digitalWrite(TRIG, LOW);
  digitalWrite(ECHO, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  float  duration = pulseIn(ECHO, HIGH);

// echoPin 이 HIGH를 유지한 시간을 저장 한다.

  float distance = ((float)(340 * duration) / 10000) / 2;
  //float distance1 = ((float)(340 * duration) / 10000) / 2;  
// HIGH 였을 때 시간(초음파가 보냈다가 다시 들어온 시간)을 가지고 거리를 계산 한다.
  Serial.print('\n');
  Serial.print(distance);
  //Serial.println("cm"); // distance값 뒤에 문자 출력

  delay(500);
   
  if (distance > 20 &distance<=27) {
    
    digitalWrite(GREEN, HIGH); // on
    digitalWrite(YELLOW, LOW); // OFF
    digitalWrite(RED, LOW); // OFF
    shirt=1;
    //Serial.println(shirt);
    //Serial.print(" T-shirts LEFT ");  
    //Serial.print("\n");
  }

  else if (distance > 10 & distance <= 20){
     digitalWrite(GREEN, LOW); // OFF
     digitalWrite(YELLOW, HIGH); // on
     digitalWrite(RED, LOW); // OFF
     shirt=2;
    //Serial.println(shirt);
    //Serial.print(" T-shirts LEFT ");  
    //Serial.print("\n");    
   }

   else if (distance > 0 & distance <= 10)  {
    digitalWrite(GREEN, LOW); //OFF
    digitalWrite(YELLOW, LOW); // OFF
    digitalWrite(RED, HIGH); //on
    shirt=3;
    //Serial.println(shirt);
    //Serial.print(" T-shirts LEFT ");  
    //Serial.print("\n");
   }
   else{
    digitalWrite(GREEN, LOW); //OFF
    digitalWrite(YELLOW, LOW); // OFF
    digitalWrite(RED, LOW); //OFF
    shirt=0;
    //Serial.print("EMPTY\n");
    //Serial.print("\n");  
   }

   //서보모터 작동
   while(Serial.available()>0) {
    char c=Serial.read();
    if(c=='y'){
       for(angle = 0; angle<90; angle++){
        servo2.write(angle);
        delay(20);
       }
       delay(500);

        for(angle = 0; angle < 80; angle++){ 
             servo.write(180-angle);
             servo1.write(angle); 
             delay(20); 
         } 
         
  // now scan back from 180 to 0 degrees
        for(angle = 80; angle > 0; angle--){ 
            servo.write(180-angle); 
            servo1.write(angle);
            delay(20); 
        }        
        
        for(angle=90; angle>0; angle--){
        servo2.write(angle);
        delay(20);
        }
        
        
    }
    else if (c=='n') {
      //exit(1);
    }
 }

     
  

}
