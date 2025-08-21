#include <SPI.h>
#include <Ethernet.h>
#include <LiquidCrystal.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192,168,0,16);

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

float Power=0;
float Energy=0;

const int analogchannel = 0;
int sensitivity = 100;
float adcvalue= 0;
int offsetvoltage = 2500; 
double Voltage = 0;
double Irms = 0;

char server[] = "192.168.0.11";
EthernetClient client;

void setup() {
  Serial.begin(9600);
  lcd.begin(20, 4);
  lcd.setCursor(1,1);
  delay(100);
}

uint16_t get_max() {
  uint16_t max_v = 0;
  for(uint8_t i = 0; i < 100; i++) {
    uint16_t r = analogRead(3);
    if(max_v < r) max_v = r;
    delayMicroseconds(200);
    Ethernet.begin(mac, ip);
  }
  return max_v;
} 

void loop(){
  lcd.display();
  lcd.setCursor(1,0);
  lcd.print("SMART ENERGY METER");
  char buf[10];
  uint32_t Vrms = get_max();
  Vrms = Vrms * 1100/1023;
  Vrms /= sqrt(2);
  Vrms=Vrms*2.035;
  sprintf(buf, "%03u Volts", Vrms);
  
  lcd.setCursor(0, 1);
  lcd.print("Vrms = ");//Diplays Vrms
  lcd.print(buf);//Display voltage
  
  unsigned int temp=0;
  float maxpoint = 0;
  int i=0;
  
  for(i=0;i<500;i++){
    if(temp = analogRead(analogchannel),temp>maxpoint){
      maxpoint = temp;
    }
  }

  adcvalue = maxpoint; 
  Voltage = (adcvalue / 1024.0) * 5000;
  Irms = ((Voltage - offsetvoltage) / sensitivity);
  Irms = ( Irms ) / ( sqrt(2) );
  
  Power=Vrms*Irms;
  
  unsigned long time;
  time= millis()/1000;
  
  Energy= (Power*time)/3600;

  lcd.setCursor(0,2);
  lcd.print("Irms = ");
  lcd.print(Irms,3);
  lcd.print("Amps");

  lcd.setCursor(0,3);
  lcd.print("E = ");
  lcd.print(Energy,3);
  lcd.print("Wh");
  delay(1000);
  
}
