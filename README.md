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