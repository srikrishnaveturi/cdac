char dataString[50] = {0};
int a =0; 

void setup() {
Serial.begin(9600); 
pinMode(13,OUTPUT);

Serial.println("HI PIIII");//Starting serial communication
}
  
void loop() {
     Serial.println("H");                      // a value increase every loop
  if(Serial.available()){
    flash(Serial.parseInt());
    Serial.flush();
    }              
    delay(2000);// give the loop some break
}
void flash(int n){
Serial.println(n);
for(int i=0;i<n;i++){
  digitalWrite(13,HIGH);
  delay(100);
  digitalWrite(13,LOW);
  delay(100);
  Serial.println(i+1);
  }
  Serial.println("Blinked");
}
