import subprocess
import optparse
import re



def get_arguments():
    parser=optparse.OptionParser()
    parser.add_option('-i','--interface', dest="interface", help="Interface to change the Mac Address")
    parser.add_option('-m','--new_mac', dest="new_mac_addr", help="New Mac Address")
    parser.add_option('-l','--list_interface',action="store_true",dest="interfaces", help="List all Interfaces Available")
    option,args = parser.parse_args()
    return option

def change_mac(device, new_mac_addr):
    if not device:
        parser.error("[+] Please specify an Inteface or use -h or --help for more Information")
    elif not new_mac_addr:
        parser.error("[+] Please specify a MAC address or use -h or --help for more Information")
    print("[+] Changing MAC address for {} to {}".format(device,new_mac_addr))
    subprocess.run(['ifconfig', device , 'down'])
    subprocess.run(['ifconfig', device , 'hw', 'ether', new_mac_addr])
    subprocess.run(['ifconfig', device , 'up'])

def get_current_mac(interface):
    mac_address_re= re.compile('(\w\w:){5}\w\w')
    ifconfig_result = subprocess.run(["ifconfig",interface], check=True,stdout=subprocess.PIPE,universal_newlines=True).stdout
    mac_addr_extract = re.search(mac_address_re, ifconfig_result)
    if mac_addr_extract:
        return mac_addr_extract[0]
    else:
        return "Can't Locate MAC address"

def get_all_devices():
    intrface_re= re.compile('[\w]+:\ ')
    ifconfig_result = subprocess.run(["ifconfig"], check=True,stdout=subprocess.PIPE,universal_newlines=True).stdout
    intr_extract = re.findall(intrface_re, ifconfig_result) 
    if intr_extract:
        print("Following interfaces are connected to Your Device")
        for i in range(len(intr_extract)):
            print("  [+] ",intr_extract[i].strip(": "))
    else:
        print("Can't read Your Device")
    

    

options = get_arguments()
if options.interfaces:
    get_all_devices()
elif options.interface or options.new_mac_addr:
    old_mac_address = get_current_mac(options.interface)
    change_mac(options.interface, options.new_mac_addr)
    new_mac_address = get_current_mac(options.interface)
    if old_mac_address!=new_mac_address:
        print('[+]MAC address Has Changed Successfully from {} to {} of {}'.format(old_mac_address, new_mac_address, options.interface))
    else:
        print("Some Problem in Changing MAC address")
else:
    print("[+] Invalid Arguments please use -h or --help for more information")
