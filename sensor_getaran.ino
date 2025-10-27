int PinAlarm = A0;
int PinGetar = 3;

void setup() {
  Serial.begin(9600);
  pinMode(PinAlarm, OUTPUT);
  pinMode(PinGetar, INPUT);
}

void loop() {
  long nilaigetar = analogRead(PinGetar);
  Serial.print(nilaigetar);

  if (nilaigetar == 0) {
    Serial.println(nilaigetar);
    Serial.println("Tidak ada getaran");
    digitalWrite(PinAlarm, LOW);
  } else if (nilaigetar > 0 && nilaigetar < 3000) {
    Serial.println(nilaigetar);
    Serial.println("Getaran rendah");
    digitalWrite(PinAlarm, LOW);
  } else if (nilaigetar >= 3000) {
    Serial.println(nilaigetar);
    Serial.println("Getaran tinggi");
    digitalWrite(PinAlarm, HIGH);
  }
  delay(10);
  Serial.println("");
}

long nilai() {
  delay(1000);
  long nilaigetar = pulseIn(PinGetar, HIGH);
  return nilaigetar;
}
