cpp
Copy code
int motorPin = 9;          // Pin del motor del ventilador
int waterMotorPin = 10;    // Pin del motor de agua
int ledPin = 11;           // Pin de las luces LED
Se definen variables para almacenar los números de pin del motor del ventilador, motor de agua y luces LED.
cpp
Copy code
void setup() {
  pinMode(motorPin, OUTPUT);        // Configura el pin del motor del ventilador como salida
  pinMode(waterMotorPin, OUTPUT);   // Configura el pin del motor de agua como salida
  pinMode(ledPin, OUTPUT);          // Configura el pin de las luces LED como salida
  Serial.begin(9600);               // Inicia la comunicación serial a 9600 baudios
}
En la función setup(), se establecen los modos de los pines como salida para controlar los dispositivos conectados a ellos (motor del ventilador, motor de agua, luces LED). Además, se inicia la comunicación serial a una velocidad de 9600 baudios.
cpp
Copy code
void loop() {
  if (Serial.available() > 0) {     // Verifica si hay datos disponibles en el puerto serial
    String command = Serial.readStringUntil('\n'); // Lee el comando enviado por el cliente Python hasta encontrar un salto de línea
    
    if (command.equals("FAN_TOGGLE")) {
      toggleFanMotor();              // Si el comando es "FAN_TOGGLE", llama a la función para alternar el motor del ventilador
    } else if (command.equals("WATER_TOGGLE")) {
      toggleWaterPump();            // Si el comando es "WATER_TOGGLE", llama a la función para alternar el motor de agua
    } else if (command.startsWith("LED")) {
      controlLedIntensity(command);  // Si el comando comienza con "LED", llama a la función para controlar la intensidad de las luces LED
    } else if (command.startsWith("FAN_SPEED")) {
      controlFanSpeed(command);     // Si el comando comienza con "FAN_SPEED", llama a la función para controlar la velocidad del ventilador
    } else {
      Serial.println("Comando desconocido"); // Si no coincide con ningún comando conocido, imprime un mensaje de comando desconocido
    }
  }
}
En la función loop(), se verifica si hay datos disponibles en el puerto serial. Si hay datos, se lee el comando enviado por el cliente Python.
Dependiendo del comando recibido, se llama a diferentes funciones para realizar acciones específicas: alternar el motor del ventilador, alternar el motor de agua, controlar la intensidad de las luces LED o controlar la velocidad del ventilador. Si el comando no coincide con ninguno de los previstos, se imprime un mensaje indicando que el comando es desconocido.
cpp
Copy code
void toggleFanMotor() {
  digitalWrite(motorPin, !digitalRead(motorPin)); // Cambia el estado del pin del motor del ventilador (encendido o apagado)
  Serial.println("Motor del Ventilador Toggled"); // Imprime un mensaje indicando que se ha alternado el motor del ventilador
}

void toggleWaterPump() {
  digitalWrite(waterMotorPin, !digitalRead(waterMotorPin)); // Cambia el estado del pin del motor de agua (encendido o apagado)
  Serial.println("Motor de Agua Toggled"); // Imprime un mensaje indicando que se ha alternado el motor de agua
}

void controlLedIntensity(String command) {
  int intensity = command.substring(3).toInt(); // Obtiene la intensidad de las luces LED del comando recibido
  analogWrite(ledPin, map(intensity, 0, 100, 0, 255)); // Ajusta la intensidad de las luces LED utilizando PWM
  Serial.println("Intensidad de LED ajustada"); // Imprime un mensaje indicando que se ha ajustado la intensidad de las luces LED
}

void controlFanSpeed(String command) {
  int speed = command.substring(9).toInt(); // Obtiene la velocidad del ventilador del comando recibido
  analogWrite(motorPin, map(speed, 0, 100, 0, 255)); // Ajusta la velocidad del ventilador utilizando PWM
  Serial.println("Velocidad del Motor del Ventilador ajustada"); // Imprime un mensaje indicando que se ha ajustado la velocidad del ventilador
}
Estas son las funciones que se llaman según el comando recibido:
toggleFanMotor(): Cambia el estado del pin del motor del ventilador (encendido o apagado) y muestra un mensaje.
toggleWaterPump(): Cambia el estado del pin del motor de agua (encendido o apagado) y muestra un mensaje.
controlLedIntensity(String command): Obtiene la intensidad de las luces LED del comando recibido y la ajusta utilizando PWM, luego muestra un mensaje.
controlFanSpeed(String command): Obtiene la velocidad del ventilador del comando recibido y la ajusta utilizando PWM, luego muestra un mensaje.