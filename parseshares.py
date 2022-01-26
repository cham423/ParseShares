#! /usr/bin/env python3
import argparse
import uuid

parser = argparse.ArgumentParser(description='Parse SharpShares Output')
parser.add_argument('-f',dest='file', action='store', required=True, help='path to sharpshares output in a file')
parser.add_argument('-outfiles',dest='outfiles', action='store_true',help='write paths to output files (auto-generated names)')
parser.add_argument('-p',dest='printpaths', action='store_true', help='print share paths in \\\\host\\share format')
parser.add_argument('-l',dest='printlist', action='store_true', help='list shares in prioritized, human readable format (on by default)')
parser.add_argument('-iloveprinters',dest='printers', action='store_true', help='show print$ shares')

parser.set_defaults(printlist=True)
args = parser.parse_args()

# file for infile
file = args.file

# files for outfiles
fileSig = str(uuid.uuid4())[:8]
daFile = 'parsed_da_{}'.format(fileSig)
adminFile = 'parsed_admin_{}'.format(fileSig)
listableFile = 'parsed_listable_{}'.format(fileSig)
dcFile = 'parsed_dc_{}'.format(fileSig)
sccmFile = 'parsed_sccm_{}'.format(fileSig)

# define shares to look for
printerShares = ['print$', 'prnproc$']
adminShares = ['C$','ADMIN$']
dcShares = ['NETLOGON', 'SYSVOL']
sccmShares = ['REMINST', 'SCCMContentLib$', 'SMSPKGD$', 'SMSSIG$']

# create empty results lists
daHosts = []
adminHosts = []
dcHosts = []
sccmHosts = []
listableHosts = []

# main loop
with open(file,'r') as file:
        for line in file:
            shares = []
            admin = False
            dc = False
            sccm = False
            if 'Shares for' in line:
                host = line.split(' ')[2].replace(':','').rstrip('\n')
            if 'Listable Shares' in line:
                shareList = next(file).rstrip('\n').split('\t')
                for share in shareList:
                    if share != '':
                        if args.printers:
                            shares.append(share)
                        elif share not in printerShares:
                            shares.append(share)
                if len(shares) > 0:
                    for test in adminShares:
                        if test in shares:
                            admin = True
                    for test in dcShares:
                        if test in shares:
                            dc = True
                    for test in sccmShares:
                        if test in shares:
                            sccm = True
                    if admin and dc:
                        daHosts.append({'host':host, 'shares':shares})
                        #print('!!! YOU HAVE DA on {} with shares {}'.format(host,shares))
                    elif admin:
                        adminHosts.append({'host':host, 'shares':shares})
                        #print('!!! Potential Local Admin on {} with shares {}'.format(host,shares))
                    elif dc:
                        dcHosts.append({'host':host, 'shares':shares})
                        #print('DC Found: {} with shares {}'.format(host,shares))
                    elif sccm:
                        sccmHosts.append({'host':host, 'shares':shares})
                        #print('SCCM Found: {} with shares {}'.format(host,shares))
                    else:
                        listableHosts.append({'host':host, 'shares':shares})
                        #print('listable shares for {} were {}'.format(host,shares))
# final print results
if args.printlist:
    print("--- DA Hosts ---")
    for host in daHosts:
        print(host)
    print("--- Admin Hosts ---")
    for host in adminHosts:
        print(host)
    print("--- Listable Hosts ---")
    for host in listableHosts:
        print(host)
    print("--- DC Hosts ---")
    for host in dcHosts:
        print(host)
    print("--- SCCM Hosts ---")
    for host in sccmHosts:
        print(host)

# print paths
if args.printpaths:
    print("--- DA Share Paths ---")
    for host in daHosts:
        for share in host['shares']:
            print('\\\\{}\\{}'.format(host['host'],share))
    print("--- Admin Share Paths ---")
    for host in adminHosts:
        for share in host['shares']:
            print('\\\\{}\\{}'.format(host['host'],share))
    print("--- Listable Share Paths ---")
    for host in listableHosts:
        for share in host['shares']:
            print('\\\\{}\\{}'.format(host['host'],share))
    print("--- DC Share Paths ---")
    for host in dcHosts:
        for share in host['shares']:
            print('\\\\{}\\{}'.format(host['host'],share))
    print("--- SCCM Share Paths ---")
    for host in sccmHosts:
        for share in host['shares']:
            print('\\\\{}\\{}'.format(host['host'],share))
if args.outfiles:
    if len(daHosts) > 0:
        with open(daFile,'w') as file:
            for host in daHosts:
                for share in host['shares']:
                    file.write('\\\\{}\\{}\n'.format(host['host'],share))
        file.close()
    if len(adminHosts) > 0:
        with open(adminFile,'w') as file:
            for host in adminHosts:
                for share in host['shares']:
                    file.write('\\\\{}\\{}\n'.format(host['host'],share))
        file.close()
    if len(listableHosts) > 0:
        with open(listableFile,'w') as file:
            for host in adminHosts:
                for share in host['shares']:
                    file.write('\\\\{}\\{}\n'.format(host['host'],share))
        file.close()
    if len(dcHosts) > 0:
        with open(dcFile,'w') as file:
            for host in dcHosts:
                for share in host['shares']:
                    file.write('\\\\{}\\{}\n'.format(host['host'],share))
        file.close()
    if len(sccmHosts) > 0:
        with open(sccmFile,'w') as file:
            for host in sccmHosts:
                for share in host['shares']:
                    file.write('\\\\{}\\{}\n'.format(host['host'],share))
        file.close()