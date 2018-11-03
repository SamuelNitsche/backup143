import hashlib
import os
from pathlib import Path
from configparser import ConfigParser, DuplicateSectionError, NoOptionError

# Calculate folder path for ini files
hashpath = str(Path.home()) + os.sep + 'backup143'
# Create folder if not exists
if not os.path.exists(hashpath):
    os.mkdir(hashpath)


def filechanged(task, dir, file):
    # Return true if backup type is full
    if task['type'] == 'full':
        print('Type is full. Backing up file ' + file)
        return True

    config = ConfigParser()

    hashfile = os.path.join(hashpath, str(task['id']) + '.ini')
    hasher = hashlib.sha3_512()
    f = open(os.path.join(dir, file), 'rb')
    # Read file
    buf = f.read()
    # Calculate hash of file
    hasher.update(buf)
    # Create ini file for task if it does not exist
    if not os.path.exists(hashfile):
        f = open(hashfile, "w+")
        f.close()

    # Parse ini file
    config.read(hashfile)

    # Add new section if it does not exist
    try:
        config.add_section(dir)
    except DuplicateSectionError:
        pass

    haschanged = False
    try:
        # Get hash from file
        hash = config.get(dir, file)

        # Compare hash from file with new hash of file
        if not hash == hasher.hexdigest():
            print('Hash has changed')
            # Set new hash in file
            config.set(dir, file, hasher.hexdigest())
            haschanged = True
        else:
            print(file + ' has not changed')

    except NoOptionError:
        # If file is new set hash
        print('No value set. Setting current hash')
        config.set(dir, file, hasher.hexdigest())
        haschanged = True
    except Exception as e:
        print('Other error occurred')
        print(e)

    # Save new values to ini file
    with open(hashfile, 'w') as configfile:
        config.write(configfile)

    return haschanged
