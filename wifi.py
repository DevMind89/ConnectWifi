import pywifi
import time
import tkinter as tk
import tkinter.simpledialog

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

def scan_networks():
    iface.scan()
    time.sleep(2)
    scan_results = iface.scan_results()
    if scan_results != "":
        network_list.delete(1, tk.END) 
        displayed_ssids = set()
        for result in scan_results:
            if result.ssid != "" and result.ssid not in displayed_ssids:
                network_list.insert(tk.END, f"SSID: {result.ssid}, BSSID: {result.bssid}, Signal: {result.signal}")
                network_list.insert(tk.END, "________________________________________________________________________") 
    else:
        tkinter.messagebox.showinfo("Info", "Not networks available.")         


def choose_network():
    network = network_list.curselection()
    if network:
        result = network_list.get(network[0])
        ssid_index = result.find("SSID: ") + len("SSID: ")
        comma_index = result.find(", BSSID:")
        ssid = result[ssid_index:comma_index]
        enter_password(ssid)
        
def enter_password(ssid):  
    while True:
        spaces = "\t\t\t\t\t"
        password = tkinter.simpledialog.askstring(f"{ssid}", f"Enter the WiFi password: {spaces}", show='*')
        if password is None:
            return False
        elif password:
            if connect_network(ssid, password):
                break 
            else:
                tkinter.messagebox.showinfo("Info", "Incorrect password. Please try again.")
            
    return True

        
def connect_network(ssdi, password):
    profile = pywifi.Profile()
    profile.ssid = ssdi
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
    profile.key = password
        
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(5) 
    
    if iface.status() == pywifi.const.IFACE_CONNECTED:
        root.destroy()
        return True
    else:
        return False
   

root = tk.Tk()
root.title("WiFi")
root.geometry("600x400")
root.resizable(False, False)

network_list = tk.Listbox(root, width=95, height=20)
network_list.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

scan_button = tk.Button(root, text="Scan Networks", command=scan_networks)
scan_button.grid(row=1, column=0, padx=10, pady=10)

choose_button = tk.Button(root, text="Choose", command=choose_network)
choose_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
