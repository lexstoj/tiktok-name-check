import sys
import requests
from colorama import init,Fore
import string
import random
from bs4 import BeautifulSoup
import itertools

print('''
  _______ _____ _  _________ ____  _  __  _   _          __  __ ______    _____ _    _ ______ _____ _  ________ _____  
 |__   __|_   _| |/ |__   __/ __ \| |/ / | \ | |   /\   |  \/  |  ____|  / ____| |  | |  ____/ ____| |/ |  ____|  __ \ 
    | |    | | | ' /   | | | |  | | ' /  |  \| |  /  \  | \  / | |__    | |    | |__| | |__ | |    | ' /| |__  | |__) |
    | |    | | |  <    | | | |  | |  <   | . ` | / /\ \ | |\/| |  __|   | |    |  __  |  __|| |    |  < |  __| |  _  / 
    | |   _| |_| . \   | | | |__| | . \  | |\  |/ ____ \| |  | | |____  | |____| |  | | |___| |____| . \| |____| | \ \ 
    |_|  |_____|_|\_\  |_|  \____/|_|\_\ |_| \_/_/    \_|_|  |_|______|  \_____|_|  |_|______\_____|_|\_|______|_|  \_\
                                Known bugs:
                                    [-] --ignore-invalid sometimes still shows invalid names. why
''')

init(convert=True) #Fuck you colorama.

print('Setting headers...', end='')
headers = {
    'User-Agent' : 'Mozilla: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)' #Avoid 429: Too Many Requests, fuck you too instagram.
} 
print('Done')

ignore = False
save = False
rheader = False

def checkuser(name) -> None:
    global ignore
    global save
    accounts = []
    checking = requests.get(f'https://www.tiktok.com/@{name}?', headers = headers)
    soup = BeautifulSoup(checking.content, 'html.parser')
    try:
        if name in soup.find(class_ = 'jsx-2997938848 share-title'):
            if ignore is False:
                print(Fore.RED + f'[X] Name "{name}" is not valid.')
    except TypeError as e:
        if soup.find(class_ = 'jsx-2997938848 share-title verified') is not None or soup.find(class_ = 'jsx-2997938848 share-title ftc') is not None:
            print(Fore.RED + f'[X] Name "{name}" is not valid.')
        else:    
            print(Fore.GREEN + f'[O] Name "{name}" is valid.')
            accounts.append(name)
            if save is True:
                with open('valid_user.txt', 'w') as f:
                    f.write(str(accounts))
                    f.close()

    
def checkmultiple(lettercount, genType) -> None:
    global ignore
    global save
    global headers
    global rheader
    accounts = []
    names = []
    while True:
        name = ''
        if genType == 'random':
            for _ in range(lettercount):
                name += random.choice(string.ascii_lowercase + string.digits)
            checking = requests.get(f'https://www.tiktok.com/@{name}?', headers = headers)
            soup = BeautifulSoup(checking.content, 'html.parser')
            try:
                if name in soup.find(class_ = 'jsx-2997938848 share-title'):
                    if ignore is False:
                        print(Fore.RED + f'[X] Name "{name}" is not valid.')
            except TypeError as e:
                if soup.find(class_ = 'jsx-2997938848 share-title verified') is not None or soup.find(class_ = 'jsx-2997938848 share-title ftc') is not None:
                    print(Fore.RED + f'[X] Name "{name}" is not valid.')
                else:    
                    print(Fore.GREEN + f'[O] Name "{name}" is valid.')
                    accounts.append(name)
                    if save is True:
                        with open('valid_user.txt', 'w') as f:
                            f.write(str(accounts))
                            f.close()
            if rheader:
                headers = {
                    f'User-Agent' : 'Mozilla: Mozilla/{random.randint(1,9)}.0 (Windows NT {random.randint(1,9)}.1; Win{random.choice([32,64])}; x{random.choice([32,64])}; rv:{random.randint(9,99)}.0)'
                }

        elif genType == 'alphabetical':
            print('Generating the names in alphabetical order...')
            if lettercount <= 4:
                for elem in itertools.product(string.ascii_lowercase, repeat=lettercount):
                    for i in elem:
                        name += i
                    names.append(name)
                    name = ''
                for _name in names:
                    checking = requests.get(f'https://www.tiktok.com/@{_name}?', headers = headers)
                    soup = BeautifulSoup(checking.content, 'html.parser')
                    try:
                        if _name in soup.find(class_ = 'jsx-2997938848 share-title'):
                            if ignore is False:
                                print(Fore.RED + f'[X] Name "{_name}" is not valid.')
                    except TypeError as e:
                        if soup.find(class_ = 'jsx-2997938848 share-title verified') is not None or soup.find(class_ = 'jsx-2997938848 share-title ftc') is not None:
                            print(Fore.RED + f'[X] Name "{_name}" is not valid.')
                        else:    
                            print(Fore.GREEN + f'[O] Name "{_name}" is valid.')
                            accounts.append(_name)
                            if save is True:
                                with open('valid_user.txt', 'w') as f:
                                    f.write(str(accounts))
                                    f.close()
            else:
                print("We don't need out of memory exceptions.. Pick a smaller number")
                exit(-1)
        


try:
    print('Checking sys args...')
    if '--save-to-file' in sys.argv:
        save = True
        print('Enabled save to file')
    if '--ignore-invalid' in sys.argv:
        ignore = True
        print('Enabled invalid names ignoration')
    if '--random-header' in sys.argv:
        rheader = True
        print('Enabled header randomization')
    if sys.argv[1] == '--checkOne':
        checkuser(sys.argv[2])
    elif sys.argv[1] == '--checkMultiple':
        if not '--generationType' in sys.argv:
            print('Specify the generation type. "random" or "alphabetical" ')
            exit(-1)
        if '--generationType' in sys.argv:
            gentype = sys.argv.index('--generationType')
            checkmultiple(int(sys.argv[2]), sys.argv[gentype + 1])
except KeyboardInterrupt:
    print(Fore.BLUE + 'Tool created by connordechart on github. Quitting...')
    exit(-3)
except Exception as e:
    print(f''' 
{e}
Use this in cmd.
Usage: python check.py <method> <name/lettercount> *, <optional args>
Example: python check.py --checkOne .dechart
Example: python check.py --checkMultiple 4 --generationType alphabetical/random
Optional args:
    --ignore-invalid - ignores invalid names
    --save-to-file - save all valid names to a .txt file
    --random-header - random headers, reduces the chance of getting rate limited
    ''')                   


if __name__ == '__main__': 
    pass
