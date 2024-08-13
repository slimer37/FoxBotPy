import os

ignorelist = set()

ignorefile = 'ignored_users.txt'

if os.path.exists(ignorefile):
    with open(ignorefile, 'r', newline='') as f:
        ignorelist = set(f.readlines())

print(f'Loaded {len(ignorelist)} ignored users.')
    

def add_user(id: str):
    if id in ignorelist: return False
    
    ignorelist.add(id)
    
    return True

def remove_user(id: str):
    if id not in ignorelist: return False
    
    ignorelist.remove(id)
    
    return True


def user_exists(id: str) -> bool:
    return id in ignorelist

def save():
    with open(ignorefile, 'w', newline='') as f:
        f.writelines(ignorelist)
    print('Saved database')