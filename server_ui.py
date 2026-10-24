import curses
import serial
import time
import sys
import psutil
import os
import socket

# --- CONFIGURATION ---
PORT = '/dev/ttyUSB0' 
BAUD_RATE = 9600

menu_items = [
    "1. View CPU & RAM Status",
    "2. View Network Traffic",
    "3. Restart Server",
    "4. Exit Dashboard"
]

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1 (Offline)'
    finally:
        s.close()
    return ip

def draw_menu(stdscr, current_row, message=""):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    title = " LENOVO V145 HARDWARE DASHBOARD "
    stdscr.addstr(2, width//2 - len(title)//2, title, curses.A_BOLD | curses.A_UNDERLINE)
    
    for idx, item in enumerate(menu_items):
        x = width//2 - len(item)//2
        y = height//2 - len(menu_items)//2 + idx
        
        if idx == current_row:
            stdscr.addstr(y, x, item, curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(y, x, item)
            
    if message:
        stdscr.addstr(height-3, width//2 - len(message)//2, message, curses.A_STANDOUT)
        
    stdscr.refresh()

def show_stats_screen(stdscr, ser):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    while True:
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory()
        
        stdscr.clear()
        title = " LIVE SYSTEM STATS "
        stdscr.addstr(2, width//2 - len(title)//2, title, curses.A_BOLD)
        
        cpu_str = f"CPU Usage: {cpu}%"
        stdscr.addstr(5, width//2 - len(cpu_str)//2, cpu_str)
        
        ram_str = f"RAM Usage: {ram.percent}% ({ram.used // (1024**2)}MB / {ram.total // (1024**2)}MB)"
        stdscr.addstr(7, width//2 - len(ram_str)//2, ram_str)
        
        footer = "[ Press STANDARD LEFT CLICK to return ]"
        stdscr.addstr(height-3, width//2 - len(footer)//2, footer, curses.color_pair(1))
        
        stdscr.refresh()
        
        if ser.in_waiting > 0:
            try:
                raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
                if "Standard Left Click" in raw_data:
                    break 
            except:
                pass

def show_network_screen(stdscr, ser):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    ip_addr = get_local_ip()
    net_io = psutil.net_io_counters()
    last_recv = net_io.bytes_recv
    last_sent = net_io.bytes_sent
    
    while True:
        stdscr.clear()
        title = " LIVE NETWORK TRAFFIC "
        stdscr.addstr(2, width//2 - len(title)//2, title, curses.A_BOLD)
        
        ip_str = f"Server IP: {ip_addr}"
        stdscr.addstr(4, width//2 - len(ip_str)//2, ip_str)
        
        net_io = psutil.net_io_counters()
        recv_mb = net_io.bytes_recv / (1024*1024)
        sent_mb = net_io.bytes_sent / (1024*1024)
        
        recv_speed = ((net_io.bytes_recv - last_recv) / 1024) * 2 
        sent_speed = ((net_io.bytes_sent - last_sent) / 1024) * 2
        
        last_recv = net_io.bytes_recv
        last_sent = net_io.bytes_sent
        
        recv_str = f"Download: {recv_mb:.1f} MB Total | Speed: {recv_speed:.1f} KB/s"
        sent_str = f"Upload: {sent_mb:.1f} MB Total | Speed: {sent_speed:.1f} KB/s"
        
        stdscr.addstr(6, width//2 - len(recv_str)//2, recv_str)
        stdscr.addstr(7, width//2 - len(sent_str)//2, sent_str)
        
        footer = "[ Press STANDARD LEFT CLICK to return ]"
        stdscr.addstr(height-3, width//2 - len(footer)//2, footer, curses.color_pair(1))
        stdscr.refresh()
        
        start_time = time.time()
        exit_screen = False
        while time.time() - start_time < 0.5:
            if ser.in_waiting > 0:
                try:
                    raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if "Standard Left Click" in raw_data:
                        exit_screen = True
                        break 
                except:
                    pass
            time.sleep(0.05)
            
        if exit_screen:
            break

def confirm_reboot_screen(stdscr, ser):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    warn = " WARNING: REBOOT SERVER? "
    stdscr.addstr(height//2 - 2, width//2 - len(warn)//2, warn, curses.A_BOLD | curses.A_STANDOUT)
    
    opt1 = "[ MIDDLE CLICK = Confirm Reboot ]"
    opt2 = "[ LEFT CLICK = Cancel & Return ]"
    
    stdscr.addstr(height//2, width//2 - len(opt1)//2, opt1)
    stdscr.addstr(height//2 + 1, width//2 - len(opt2)//2, opt2)
    stdscr.refresh()
    
    while True:
        if ser.in_waiting > 0:
            try:
                raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
                if "Standard Left Click" in raw_data:
                    return False 
                elif "EXECUTE" in raw_data:
                    return True 
            except:
                pass
        time.sleep(0.05)

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    current_row = 0
    message = "Hardware Bridge Connected. Awaiting Input..."
    
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1) 
        time.sleep(2)
    except Exception as e:
        stdscr.addstr(0, 0, f"ERROR: Could not open {PORT}.")
        stdscr.refresh()
        time.sleep(3)
        return False

    draw_menu(stdscr, current_row, message)

    while True:
        try:
            if ser.in_waiting > 0:
                raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if "Scrolled DOWN" in raw_data:
                    current_row = (current_row + 1) % len(menu_items)
                    message = "" 
                    
                elif "Scrolled UP" in raw_data:
                    current_row = (current_row - 1 + len(menu_items)) % len(menu_items)
                    message = ""
                    
                elif "EXECUTE" in raw_data:
                    if current_row == 0: 
                        show_stats_screen(stdscr, ser)
                        message = ""
                    elif current_row == 1: 
                        show_network_screen(stdscr, ser)
                        message = ""
                    elif current_row == 2: 
                        reboot = confirm_reboot_screen(stdscr, ser)
                        if reboot:
                            return True 
                        else:
                            message = "Reboot Cancelled."
                    elif current_row == 3: 
                        return False 
                    else:
                        message = f"EXECUTING: {menu_items[current_row]}"
                
                draw_menu(stdscr, current_row, message)
                
        except (serial.SerialException, OSError):
            message = "WARNING: USB Connection unstable!"
            draw_menu(stdscr, current_row, message)
            time.sleep(0.5) 

if __name__ == "__main__":
    trigger_reboot = curses.wrapper(main)
    
    if trigger_reboot:
        print("Hardware UI requested reboot. Bypassing inhibitors...")
        os.system("sudo systemctl reboot -i")
