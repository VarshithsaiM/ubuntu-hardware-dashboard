# ubuntu-hardware-dashboard

Turned a gutted wireless mouse and a spare Arduino Nano into a literal hardware remote control for a headless Ubuntu server. Features live CPU/Network monitoring and a hard-reboot override—all controlled by satisfying, tactile mouse clicks

# Ubuntu Hardware Server Dashboard

A custom physical control panel built for an Ubuntu headless server/laptop (specifically a Lenovo V145). This project uses repurposed mouse microswitches and an Arduino Nano to create a tactile hardware interface that communicates with a Python `curses` Terminal UI. 

It allows you to monitor live system metrics and perform hardware-level reboots without needing an external keyboard or SSH connection.

## Features
*   **Tactile Hardware Navigation:** Repurposed microswitches for Up, Down, Execute (Double-Click), and Back (Single-Click).
*   **Live System Metrics:** Real-time CPU and RAM monitoring via `psutil`.
*   **Live Network Traffic:** Real-time upload/download speeds and IP address mapping.
*   **Hardware Reboot Override:** Bypasses Ubuntu desktop systemd inhibitors to force a clean reboot.
*   **Crash-Proof Serial Bridge:** Python backend automatically ignores momentary USB disconnects or hardware bounces.

## Hardware Harvesting & Assembly
This project recycles an old wireless mouse shell to act as the ergonomic enclosure for the dashboard appliance. 

1. **Gutting the Enclosure:** The internal PCB of a standard wireless mouse was removed. The internal plastic standoffs and the cylindrical battery compartment walls were clipped out using wire snips to create a flat internal cavity large enough to house a 45mm Arduino Nano.
2. **Switch Placement:** Three standard microswitches were harvested and repurposed. They were hot-glued to the base plate of the mouse shell, specifically aligned so the existing cross-shaped plastic plungers of the mouse's left and right clickers would actuate them.
3. **Scroll Wheel Mod:** The middle microswitch was mounted directly beneath the rectangular gap left by the original scroll wheel, with a small plastic spacer glued to the top for easy actuation.
4. **Cable Routing:** A small U-shaped notch was melted into the front lip of the mouse shell to allow the Arduino's mini-USB cable to exit cleanly to the server.

### Wiring Guide (Daisy-Chain Ground)
| Microswitch | Switch Pin (NO) | Arduino Pin |
| :--- | :--- | :--- |
| **Left Switch** | Normally Open | `D5` |
| **Right Switch** | Normally Open | `D4` |
| **Middle Switch** | Normally Open | `D6` |
| **All Switches** | Common (COM) | `GND` |

## Software Installation

**1. Install Python Dependencies**
Ensure you have Python 3 installed on your Ubuntu machine, then install the required libraries:
```bash
sudo apt update
sudo apt install python3-psutil python3-serial
pip install -r requirements.txt
