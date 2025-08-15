# Tower: Pont Arduino vers OSC

Ce projet fournit un pont entre un récepteur LoRa basé sur Arduino et un client OSC (Open Sound Control), permettant de déclencher des événements OSC à partir d'un appui sur un bouton physique d'un dispositif Arduino à distance.

## Vue d'ensemble

- **Arduino Émetteur**: Lorsqu'un bouton est pressé, envoie un message LoRa et allume une LED.
- **Arduino Récepteur**: Écoute les messages LoRa, allume une barre de LED et imprime `TOWER_ON` sur le port série quand un message est reçu.
- **Pont Python (`main.py`)**: Écoute la sortie série de l'Arduino récepteur et émet un message OSC (`/light/tower on`) vers un serveur OSC local.

## Exigences Logicielles

- Python 3.10+
- [pyserial](https://pypi.org/project/pyserial/)
- [python-osc](https://pypi.org/project/python-osc/)

Installer les dépendances :

```bash
# Utiliser uv (recommandé)
uv sync

# Ou utiliser pip
pip install -r requirements.txt
```

## Installation et Configuration

### 1. Configuration Arduino

1. **Téléverser le code émetteur** sur votre premier Arduino :
   ```bash
   # Ouvrir arduino/emitter_tower.ino dans Arduino IDE
   # Sélectionner votre carte et port, puis téléverser
   ```

2. **Téléverser le code récepteur** sur votre deuxième Arduino :
   ```bash
   # Ouvrir arduino/receiver_tower.ino dans Arduino IDE
   # Sélectionner votre carte et port, puis téléverser
   ```

### 2. Connexions Matérielles

**Arduino Émetteur :**
- Connecter le bouton double Grove à D2
- Connecter la LED Grove enchaînable à D7
- Connecter le module Grove LoRa à UART (broches TX/RX)

**Arduino Récepteur :**
- Connecter la barre de LED Grove à D7
- Connecter le module Grove LoRa à UART (broches TX/RX)

### 3. Configuration du Pont Python

Le pont Python détecte automatiquement le port série de votre Arduino, donc aucune configuration manuelle n'est nécessaire.

## Utilisation

### Démarrer le Pont

1. **Connecter votre Arduino récepteur** à votre ordinateur via USB
2. **Exécuter le pont Python** :
   ```bash
   python main.py
   ```

3. **Démarrer votre serveur OSC** (ex: dans votre logiciel de contrôle d'éclairage) sur le port 8000

### Tester le Système

1. **Appuyer sur le bouton** de l'Arduino émetteur
2. **Observer l'Arduino récepteur** - la barre de LED devrait s'allumer
3. **Vérifier la console Python** - vous devriez voir "OSC event sent: /light/tower on"
4. **Vérifier votre serveur OSC** reçoit le message `/light/tower on`

## Fonctionnalités

- **Détection Dynamique de Port** : Trouve automatiquement les ports série Arduino sur différents systèmes d'exploitation
- **Multi-Plateforme** : Fonctionne sur macOS, Linux et Windows
- **Gestion d'Erreurs** : Gestion gracieuse des problèmes de connexion et déconnexions
- **Communication en Temps Réel** : Transmission de messages OSC à faible latence
- **Retour Matériel** : Indicateurs LED visuels sur les deux dispositifs Arduino

---

# Tower: Arduino to OSC Bridge

This project provides a bridge between an Arduino-based LoRa receiver and an OSC (Open Sound Control) client, allowing you to trigger OSC events from a physical button press on an Arduino device.

## Overview

- **Arduino Emitter**: When a button is pressed, sends a LoRa message and lights up an LED.
- **Arduino Receiver**: Listens for LoRa messages, lights up an LED bar, and prints `TOWER_ON` to serial when a message is received.
- **Python Bridge (`main.py`)**: Listens to the Arduino receiver's serial output and emits an OSC message (`/light/tower on`) to a local OSC server.

## Hardware Requirements

- 2x Arduino-compatible boards
- Grove LoRa modules (UART)
- Grove Chainable LED (for emitter)
- Grove LED Bar (for receiver)
- Grove Dual Button (for emitter)
- Grove cables and connectors

## Software Requirements

- Python 3.10+
- [pyserial](https://pypi.org/project/pyserial/)
- [python-osc](https://pypi.org/project/python-osc/)

Install dependencies:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Installation & Setup

### 1. Arduino Setup

1. **Upload the emitter code** to your first Arduino:
   ```bash
   # Open arduino/emitter_tower.ino in Arduino IDE
   # Select your board and port, then upload
   ```

2. **Upload the receiver code** to your second Arduino:
   ```bash
   # Open arduino/receiver_tower.ino in Arduino IDE
   # Select your board and port, then upload
   ```

### 2. Hardware Connections

**Emitter Arduino:**
- Connect Grove Dual Button to D2
- Connect Grove Chainable LED to D7
- Connect Grove LoRa module to UART (TX/RX pins)

**Receiver Arduino:**
- Connect Grove LED Bar to D7
- Connect Grove LoRa module to UART (TX/RX pins)

### 3. Python Bridge Setup

The Python bridge automatically detects your Arduino's serial port, so no manual configuration is needed.

## Usage

### Starting the Bridge

1. **Connect your receiver Arduino** to your computer via USB
2. **Run the Python bridge**:
   ```bash
   python main.py
   ```

3. **Start your OSC server** (e.g., in your lighting control software) on port 8000

### Testing the System

1. **Press the button** on the emitter Arduino
2. **Watch the receiver Arduino** - the LED bar should light up
3. **Check the Python console** - you should see "OSC event sent: /light/tower on"
4. **Verify your OSC server** receives the `/light/tower on` message

## Features

- **Dynamic Port Detection**: Automatically finds Arduino serial ports across different operating systems
- **Cross-Platform**: Works on macOS, Linux, and Windows
- **Error Handling**: Graceful handling of connection issues and disconnections
- **Real-time Communication**: Low-latency OSC message transmission
- **Hardware Feedback**: Visual LED indicators on both Arduino devices

## Troubleshooting

### Arduino Not Detected

If the Python script can't find your Arduino:

1. **Check USB connection** - try a different USB cable or port
2. **Verify Arduino drivers** are installed for your operating system
3. **Check Arduino IDE** - make sure you can upload code to the board
4. **Restart the script** - sometimes port detection needs a fresh start

### Serial Communication Issues

- **Permission errors**: On Linux/macOS, you might need to add your user to the `dialout` group
- **Port in use**: Make sure no other application is using the Arduino port
- **Wrong baud rate**: The code uses 9600 baud - ensure your Arduino code matches

### OSC Connection Issues

- **Check OSC server**: Ensure your OSC server is running on `127.0.0.1:8000`
- **Firewall settings**: Make sure port 8000 is not blocked
- **Network configuration**: Verify localhost/loopback interface is working

## Project Structure

```
tower/
├── arduino/
│   ├── emitter_tower.ino    # Arduino code for button/LoRa transmitter
│   └── receiver_tower.ino   # Arduino code for LoRa receiver/LED bar
├── main.py                  # Python bridge (Arduino → OSC)
├── pyproject.toml          # Project dependencies
├── uv.lock                 # Locked dependency versions
└── README.md              # This file
```

## OSC Message Format

The bridge sends the following OSC message when a LoRa signal is received:

- **Address**: `/light/tower`
- **Value**: `"on"`
- **Protocol**: UDP
- **Destination**: `127.0.0.1:8000`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the Arduino serial monitor for debugging information
- Ensure all hardware connections are secure