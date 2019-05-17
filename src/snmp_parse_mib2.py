#!/usr/bin/env python3
#
# Collect snmp interface counters from router
#

from __future__ import print_function
import subprocess, re, time, sys

snmp_router_ip = ''
snmp_community = ''
snmp_version = '2c'
snmp_walk_oid = '.1.3.6.1.2.1.31.1.1.1'
snmp_options = '-O qs -r 2 -t 1'
snmp_command = '/usr/bin/snmpbulkwalk'

if len(sys.argv) < 2:
    print('USAGE: ', sys.argv[0], ' <ip> <snmp_community>')
    exit(1)

(snmp_router_ip, snmp_community) = (sys.argv[1], sys.argv[2])
data = dict()

cmd = ' ' . join([snmp_command, '-v', snmp_version, '-c', snmp_community, snmp_options, snmp_router_ip, snmp_walk_oid])

cmd_pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(cmd_out, cmd_err) = cmd_pipe.communicate()
cmd_status = cmd_pipe.wait()

if cmd_status:
    print(cmd_err.decode('utf-8'))
    exit(cmd_status)

text = cmd_out.decode('utf-8')
regex = re.compile('^([^\.]+)\.(\d+)\s*(.*)')

for line in cmd_out.decode('utf-8').split('\n'):
    re_match = regex.match(line)
    if not re_match:
        continue

    (var_name, var_index, var_value) = re_match.groups()

    if var_index not in data:
        data[var_index] = {}

    data[var_index][var_name] = var_value

timestamp = time.ctime()
for interface in data.values():
    print(timestamp, ' ',  ','.join([k + ' = ' + interface[k] for k in interface.keys()]))

exit(0)
