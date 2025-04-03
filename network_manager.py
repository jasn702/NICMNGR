import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import subprocess
import re
from typing import Dict, List, Optional

class NetworkManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Adapter Manager")
        self.root.geometry("475x500")
        
        # Configure entry style for better contrast
        style = ttk.Style()
        style.map('TEntry',
            fieldbackground=[('disabled', 'white'),
                           ('readonly', 'white'),
                           ('active', 'white'),
                           ('!disabled', 'white')])
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create adapter listbox
        self.adapter_frame = ttk.LabelFrame(self.main_frame, text="Network Adapters", padding="5")
        self.adapter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.adapter_listbox = tk.Listbox(self.adapter_frame, width=50, height=10)
        self.adapter_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.adapter_listbox.bind('<<ListboxSelect>>', self.on_adapter_select)
        
        # Scrollbar for adapter listbox
        adapter_scrollbar = ttk.Scrollbar(self.adapter_frame, orient=tk.VERTICAL, command=self.adapter_listbox.yview)
        adapter_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.adapter_listbox.configure(yscrollcommand=adapter_scrollbar.set)
        
        # Create info frame
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Adapter Information", padding="5")
        self.info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # IP configuration
        ttk.Label(self.info_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.ip_var = tk.StringVar()
        self.ip_entry = ttk.Entry(self.info_frame, textvariable=self.ip_var)
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.ip_entry.configure(background="white")
        
        ttk.Label(self.info_frame, text="Subnet Mask:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.subnet_var = tk.StringVar()
        self.subnet_entry = ttk.Entry(self.info_frame, textvariable=self.subnet_var)
        self.subnet_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        self.subnet_entry.configure(background="white")
        
        ttk.Label(self.info_frame, text="Gateway:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.gateway_var = tk.StringVar()
        self.gateway_entry = ttk.Entry(self.info_frame, textvariable=self.gateway_var)
        self.gateway_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        self.gateway_entry.configure(background="white")
        
        # Buttons frame
        self.button_frame = ttk.Frame(self.main_frame, padding="5")
        self.button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.dhcp_var = tk.BooleanVar(value=True)
        self.dhcp_check = ttk.Checkbutton(self.button_frame, text="Use DHCP", 
                                         variable=self.dhcp_var, command=self.toggle_dhcp)
        self.dhcp_check.grid(row=0, column=0, padx=5)
        
        ttk.Button(self.button_frame, text="Apply Changes", 
                  command=self.apply_changes).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="Refresh", 
                  command=self.refresh_adapters).grid(row=0, column=2, padx=5)
        ttk.Button(self.button_frame, text="Exit", 
                  command=self.root.destroy).grid(row=0, column=3, padx=5)
        
        # Initialize
        self.current_adapter = None
        self.refresh_adapters()
        self.toggle_dhcp()
        
    def refresh_adapters(self):
        """Refresh the list of network adapters"""
        self.adapter_listbox.delete(0, tk.END)
        for interface, addresses in psutil.net_if_addrs().items():
            self.adapter_listbox.insert(tk.END, interface)
    
    def toggle_dhcp(self):
        """Toggle between DHCP and static IP configuration"""
        state = "disabled" if self.dhcp_var.get() else "normal"
        self.ip_entry.configure(state=state)
        self.subnet_entry.configure(state=state)
        self.gateway_entry.configure(state=state)
    
    def on_adapter_select(self, event):
        """Handle adapter selection"""
        selection = self.adapter_listbox.curselection()
        if not selection:
            return
        
        self.current_adapter = self.adapter_listbox.get(selection[0])
        addresses = psutil.net_if_addrs()[self.current_adapter]
        
        # Find IPv4 address
        ipv4_info = next((addr for addr in addresses if addr.family == 2), None)
        if ipv4_info:
            self.ip_var.set(ipv4_info.address)
            self.subnet_var.set(ipv4_info.netmask)
            # Gateway information needs to be retrieved differently
            self.get_gateway_info()
    
    def get_gateway_info(self):
        """Get gateway information for the selected adapter"""
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            output = result.stdout
            
            # Find the section for current adapter
            adapter_section = re.split(r'\r?\n\r?\n', output)
            for section in adapter_section:
                if self.current_adapter in section:
                    gateway_match = re.search(r'Default Gateway.*: ([\d.]+)', section)
                    if gateway_match:
                        self.gateway_var.set(gateway_match.group(1))
                    else:
                        self.gateway_var.set("")
                    break
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get gateway information: {str(e)}")
    
    def apply_changes(self):
        """Apply network configuration changes"""
        if not self.current_adapter:
            messagebox.showerror("Error", "Please select an adapter first")
            return
        
        try:
            if self.dhcp_var.get():
                self.set_dhcp()
            else:
                self.set_static_ip()
            
            messagebox.showinfo("Success", "Network configuration updated successfully")
            self.refresh_adapters()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply changes: {str(e)}")
    
    def set_dhcp(self):
        """Set adapter to use DHCP"""
        commands = [
            f'netsh interface ip set address "{self.current_adapter}" dhcp',
            f'netsh interface ip set dns "{self.current_adapter}" dhcp'
        ]
        
        for cmd in commands:
            subprocess.run(cmd, shell=True, check=True)
    
    def set_static_ip(self):
        """Set static IP configuration"""
        if not all([self.ip_var.get(), self.subnet_var.get(), self.gateway_var.get()]):
            raise ValueError("All IP configuration fields must be filled")
        
        command = (f'netsh interface ip set address "{self.current_adapter}" '
                  f'static {self.ip_var.get()} {self.subnet_var.get()} {self.gateway_var.get()} 1')
        
        subprocess.run(command, shell=True, check=True)

def main():
    root = tk.Tk()
    app = NetworkManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 