const int s0 = 8;  
const int s1 = 9;  
const int s2 = 12;  
const int s3 = 11;  
const int out = 10;   
// LED pins connected to Arduino 
// Variables  
int red = 0;  
int green = 0;  
int blue = 0;  
#define LM1 5 // left motor M1a
#define LM2 4 // left motor M2a
#define RM1 7 // right motor M2a
#define RM2 6 // right motor M2b
    
void setup()   
{  
  Serial.begin(9600); 
  pinMode(s0, OUTPUT);  
  pinMode(s1, OUTPUT);  
  pinMode(s2, OUTPUT);  
  pinMode(s3, OUTPUT);  
  pinMode(out, INPUT);  
      
  digitalWrite(s0, HIGH);  
  digitalWrite(s1, HIGH);  
pinMode(LM1, OUTPUT);
pinMode(LM2, OUTPUT);
pinMode(RM1, OUTPUT);
pinMode(RM2, OUTPUT);
}  
    
void loop() 
{  
  color(); 
  //Serial.print("R Intensity:");  
  //Serial.print(red, DEC);  
  //Serial.print(" G Intensity: ");  
  //Serial.print(green, DEC);  
  //Serial.print(" B Intensity : ");  
  //Serial.print(blue, DEC);  
  //Serial.println();  

  if(red < blue && green < blue)
  {
    if(-15<=red-green || red-green <=15)
    {
      Serial.println("Yellow colour");
      digitalWrite(LM1, HIGH);
      digitalWrite(LM2, LOW);
      digitalWrite(RM1, HIGH);
      digitalWrite(RM2, LOW);
    }
  }
  if(red <=20  || blue <= 20 || green <= 20)
  {
    Serial.println("White colour");
    digitalWrite(LM1, HIGH);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, HIGH);
    digitalWrite(RM2, LOW);
  }
  else{
  Serial.println("NO COLOUR");  
  }
  delay(300);   
  digitalWrite(LM1, LOW);
  digitalWrite(LM2, LOW);
  digitalWrite(RM1, LOW);
  digitalWrite(RM2, LOW);
 }  
    
void color()  
{    
  digitalWrite(s2, LOW);  
  digitalWrite(s3, LOW);  
  //count OUT, pRed, RED  
  red = pulseIn(out, digitalRead(out) == HIGH ? LOW : HIGH);  
  digitalWrite(s3, HIGH);  
  //count OUT, pBLUE, BLUE  
  blue = pulseIn(out, digitalRead(out) == HIGH ? LOW : HIGH);  
  digitalWrite(s2, HIGH);  
  //count OUT, pGreen, GREEN  
  green = pulseIn(out, digitalRead(out) == HIGH ? LOW : HIGH);  
}
