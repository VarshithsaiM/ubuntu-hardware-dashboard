import serial
import time

# --- CONFIGURATION ---
# Change this to match the exact port from your Arduino IDE
PORT = '/dev/ttyUSB0' 
BAUD_RATE = 9600

try:
    # 1. Establish connection to the Arduino
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Successfully connected to Arduino on {PORT}")
    
    # Give the Arduino 2 seconds to reboot (happens automatically on serial connect)
    time.sleep(2) 
    print("Listening for hardware inputs... (Press Ctrl+C to exit)\n")
    
    # 2. Infinite loop to read incoming data
    while True:
        if ser.in_waiting > 0:
            # Read the line, decode the bytes to a string, and remove invisible newline characters
            raw_data = ser.readline().decode('utf-8').strip()
            
            if raw_data:
                print(f"[RAW IN] {raw_data}")
                
                # 3. Parse the specific commands from your Arduino code
                if "Scrolled DOWN" in raw_data:
                    print("--> ACTION: Moving dashboard selection DOWN")
                    
                elif "Scrolled UP" in raw_data:
                    print("--> ACTION: Moving dashboard selection UP")
                    
                elif "EXECUTE" in raw_data:
                    print("--> ACTION: Running server command for this menu item!")
                    
                elif "Standard Left Click" in raw_data:
                    print("--> ACTION: Back / Cancel")
                    
                elif "Standard Right Click" in raw_data:
                    print("--> ACTION: Auxiliary Menu")

except serial.SerialException as e:
    print(f"CRITICAL ERROR: Could not connect to {PORT}.")
    print("Check that the Arduino is plugged in, the port name is correct, and the Arduino IDE Serial Monitor is CLOSED.")
except KeyboardInterrupt:
    print("\nExiting script. Closing serial connection.")
    if 'ser' in locals() and ser.is_open:
        ser.close()
