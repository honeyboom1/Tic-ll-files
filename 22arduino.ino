#include <DHT.h>

#define DHTPIN 5
#define DHTTYPE DHT11
const int ledred = 9;
const int ledgre = 10;
const int ledblu = 11;
const int BUTTON_PIN = 2;
const int buton2 = 6;
const int pinjoystick = 3;

int alive_cells;
DHT dht(DHTPIN, DHTTYPE);

// Definir los intervalos de condiciones
volatile bool Reiniciar_flag = false;

// Prototipo de la función de interrupción
void Reiniciarjuego();

void setup() {
  // Configurar pines como salida
  pinMode(ledred, OUTPUT);
  pinMode(ledgre, OUTPUT);
  pinMode(ledblu, OUTPUT);
  dht.begin();
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(buton2, INPUT_PULLUP);
  pinMode(pinjoystick, INPUT_PULLUP);

  // Inicializar comunicación serial
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {




    if (alive_cells == 'S') {       //blue es para sobrepoblacion
      digitalWrite(ledblu, HIGH);   
      digitalWrite(ledgre, LOW);
      digitalWrite(ledred, LOW);
    } else if (alive_cells == 'C') { //green es subpoblacion
      digitalWrite(ledblu, LOW);
      digitalWrite(ledgre, HIGH);
      digitalWrite(ledred, LOW);
    } else if (alive_cells == 'E') { //red es para estabilidad
      digitalWrite(ledblu, LOW);
      digitalWrite(ledgre, LOW);
      digitalWrite(ledred, HIGH);
    }
  }

  if (digitalRead(buton2) == LOW) {
    // 
    Serial.println("n_1");
    // 
    delay(100);
  }

  
  if (digitalRead(pinjoystick) == LOW) {
    // 
    Serial.println("h_1");
    // delay parar evitar multples cliclos
    delay(100);
  }
  
  
  if (digitalRead(BUTTON_PIN) == LOW) {
    //
    Serial.println("Reiniciar");
    //  
    delay(100);
  }
  }












