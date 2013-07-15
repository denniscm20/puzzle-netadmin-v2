from django.db import models
from core.models import Auditable
from django.utils.translation import ugettext as _
import subprocess

class Nmap (Auditable):
    
    def scan_network (self, network):
        p = subprocess.Popen(["nmap", "sP", network], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        if not error:
            ip_list = []
            pivot = 'Nmap scan report for '
            array_output = output.split('\n')
            for line in array_output:
                if pivot in line:
                    ip = line[len(pivot):]
                    ip_list.append(ip)
            return ip_list
        raise Error

    def scan_host (self, host):
        p = subprocess.Popen(["nmap", "PN", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        if not error:
            service_list = []
            pivot = 'open '
            array_output = output.split('\n')
            for line in array_output:
                if pivot in line:
                    port, protocol = line.split(' ')[0].split('/', 1)
                    ip_list.append((port, protocol))
            return service_list
        raise Error
