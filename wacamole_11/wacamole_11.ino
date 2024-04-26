// Definición de pines
const int ledPins[] = {2, 3, 4};  // Pines para los LEDs
const int buttonPins[] = {6, 7, 8}; // Pines para los botones
const int buzzerPin = 10; // Pin para el buzzer

// Variables de juego
int score = 90; // Puntuación inicial del jugador
int level = 1; // Nivel de dificultad inicial
int successfulHits = 0; // Número de golpes exitosos
int missedHits = 0;
int racha = 0; // contador de racha
int tiempoEncendidoLED = 0;
int tmax = 3000;




void setup() {
  Serial.begin(9600); // Inicialización del monitor serial
  randomSeed(analogRead(0)); // Solicitar al usuario que elija la dificultad
  Serial.println("Por favor, elija la dificultad introduciendo el número correspondiente:");
  Serial.println("1. Fácil (Los topos se mostraran por solo 0,5 s)");
  Serial.println("2. Medio (Los topos se mostraran por solo 0,3 s)");
  Serial.println("3. Difícil (Los topos se mostraran por solo 0,1 s)");
  Serial.println("4. Extremo (Los topos se mostraran por solo 0,1 s y tendras menos tiempo para golpearlos!)");
  while (!Serial.available()) {
    // Esperar hasta que se ingrese algo en el monitor serial
  }
  
  // Leer la opción de dificultad del usuario
  int dificultad = Serial.parseInt();
  
  // Configurar el tiempo de acuerdo a la dificultad elegida
  switch (dificultad) {
    case 1:
      tiempoEncendidoLED = 500; // Fácil
      break;
    case 2:
      tiempoEncendidoLED = 300; // Medio
      break;
    case 3:
      tiempoEncendidoLED = 100; // Difícil
      break;
    case 4:
      tiempoEncendidoLED = 100; // Extremo
      tmax = 1500;              // tiempo para golpear reducido a la mitad 
      break;
    default:
      Serial.println("Dificultad no válida. Se usará la dificultad predeterminada.");
      tiempoEncendidoLED = 500; // Por defecto, se utiliza la dificultad fácil
      break;
  }// Inicializar pines de LEDs como salida
  //for (int i = 0; i < sizeof(ledPins); i++) {
   // pinMode(pin, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);

  // Inicializar pines de botones como entrada
  for (int i = 0; i < sizeof(buttonPins); i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }

  // Inicializar pin de buzzer como salida
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  // Lógica del juego
  while (score > 0) {
    // Generar secuencia aleatoria de LEDs a encender
    int lednumber = random(2, 5);
    digitalWrite(lednumber, HIGH);
    delay(tiempoEncendidoLED); // Tiempo que permanece encendido el LED
    digitalWrite(lednumber, LOW);

    // Esperar a que el jugador golpee el LED
    unsigned long startTime = millis();
    int  = -1;
    while (buttonPressed == -1 && millis() - startTime < tmax) {
      for (int i = 0; i < sizeof(buttonPins)/sizeof(buttonPins[0]); i++) {
        if (digitalRead(buttonPins[i]) == LOW) {
          buttonPressed = i + 2;
          break;
        }
      }
    }

    // Comprobar si el jugador golpeó correctamente
    if (buttonPressed == lednumber) {
      score += 10;
      successfulHits++;
      racha += 1;
      tone(buzzerPin, 1000, 200); // Tono para golpe exitoso
    } else {
      score -=30;
      missedHits++;
      racha = 0;
      tone(buzzerPin, 200, 500); // Tono para golpe errado
    }

    // Actualizar monitor serial
    Serial.print(lednumber);
    Serial.print("Score: ");
    Serial.print(score);
    Serial.print(" | Level: ");
    Serial.print(level);
    Serial.print(" | Successful Hits: ");
    Serial.print(successfulHits);
    Serial.print(" | Missed Hits: ");
    Serial.println(missedHits);
    Serial.print(" | Successful Hits consecutivos: ");
    Serial.println(racha);

    // Aumentar nivel si es necesario
    if (racha % 10 == 0 && racha > 0) {
    level++;
    
    }
    if (racha == 0) {
    level = 0;
    }
  }

  // Reproducir melodía de fin de juego
  for (int i = 1000; i < 2000; i += 100) {
    tone(buzzerPin, i, 100);
    delay(50);
  }

  // Reiniciar variables de juego
  score = 50;
  level = 1;
  successfulHits = 0;
  missedHits = 0;
  racha = 0;
}
