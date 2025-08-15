import serial
import serial.tools.list_ports
from pythonosc import udp_client
import time

def find_arduino_port():
    """
    Dynamically find Arduino serial port across different operating systems.
    Returns the first Arduino port found, or None if no Arduino is detected.
    """
    # Get all available serial ports
    ports = serial.tools.list_ports.comports()
    
    # Common Arduino identifiers
    arduino_identifiers = [
        'Arduino',
        'arduino',
        'CH340',  # Common Arduino clone chip
        'CP210x',  # Silicon Labs USB-to-UART bridge
        'FTDI',   # FTDI USB-to-UART bridge
        'USB Serial Device',
        'USB2.0-Serial'
    ]
    
    for port in ports:
        # Check if any Arduino identifier is in the port description or manufacturer
        port_info = f"{port.description} {port.manufacturer or ''} {port.product or ''}"
        
        for identifier in arduino_identifiers:
            if identifier.lower() in port_info.lower():
                print(f"Found Arduino on port: {port.device}")
                print(f"Port info: {port.description}")
                return port.device
    
    # If no Arduino-specific port found, try common port names
    common_ports = [
        '/dev/ttyUSB0',  # Linux
        '/dev/ttyACM0',  # Linux (Arduino Uno)
        '/dev/tty.usbserial-*',  # macOS
        '/dev/tty.usbmodem*',    # macOS (Arduino Uno)
        'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10'  # Windows
    ]
    
    for port_name in common_ports:
        try:
            # Test if port exists and is accessible
            test_ser = serial.Serial(port_name, 9600, timeout=0.1)
            test_ser.close()
            print(f"Found accessible port: {port_name}")
            return port_name
        except (serial.SerialException, OSError):
            continue
    
    return None

def main():
    arduino_port = find_arduino_port()
    
    if arduino_port is None:
        print("Error: No Arduino port found!")
        print("Please make sure your Arduino is connected and try again.")
        return
    
    try:
        # Set up Arduino serial port
        ser = serial.Serial(arduino_port, 9600, timeout=1)
        print(f"Successfully connected to Arduino on {arduino_port}")
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")
        return

    # Set up OSC UDP client
    osc_client = udp_client.SimpleUDPClient("127.0.0.1", 8000)

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line == "TOWER_ON":
                # Emit OSC event to light controller
                osc_client.send_message("/light/tower", "on")
                print("OSC event sent: /light/tower on")
            time.sleep(0.5)
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            break
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
    
    ser.close()

if __name__ == "__main__":
    main()
