import hashlib
import os
from pathlib import Path
from configparser import ConfigParser, DuplicateSectionError, NoOptionError

# Calculate folder path for ini files
inipath = str(Path.home()) + os.sep + 'backup143'
# Create folder if not exists
if not os.path.exists(inipath):
    os.mkdir(inipath)


def filechanged(task, dir, file, date, lastini):
    haschanged = False

    # Return true if backup type is full
    if task['type'] == 'full':
        print('Type is full. Backing up file ' + file)
        return True

    oldini = ConfigParser()
    newini = ConfigParser()

    # Get directory for backup ini files
    taskinidir = os.path.join(inipath, str(task['id']))

    # Create directory for backup ini files if not exists
    if not os.path.exists(taskinidir):
        os.mkdir(taskinidir)

    # Get path from hashfile of old ini
    lastinidate = str(lastini).replace(' ', '_').replace(':', '-')
    oldhashfile = taskinidir + os.sep + lastinidate + '.ini'
    print('Old ini file: ' + oldhashfile)

    newhashfile = taskinidir + os.sep + date + '.ini'
    print('New ini file: ' + newhashfile)

    hasher = hashlib.sha3_512()

    f = open(os.path.join(dir, file), 'rb')

    # Read file
    buf = f.read()

    # Calculate hash of file
    hasher.update(buf)

    # Create ini file for task if it does not exist
    if not os.path.exists(newhashfile):
        f = open(newhashfile, "w+")
        f.close()

    # Parse ini file
    newini.read(newhashfile)

    if os.path.exists(oldhashfile):
        oldini.read(oldhashfile)
    else:
        print('Old hash file does not exist. Creating new one with current values')
        if not newini.has_section(dir):
            newini.add_section(dir)

        newini.set(dir, file, hasher.hexdigest())

        haschanged = True

        # Save new values to ini file
        with open(newhashfile, 'w') as configfile:
            newini.write(configfile)

        return haschanged

    # Add new section if it does not exist
    if not newini.has_section(dir):
        newini.add_section(dir)

    if oldini.has_section(dir):
        if oldini.has_option(dir, file):
            # Get hash from file
            hash = oldini.get(dir, file)

            # Compare hash from file with new hash of file
            if not hash == hasher.hexdigest():
                print('Hash has changed')
                # Set new hash in file
                newini.set(dir, file, hasher.hexdigest())
                haschanged = True
            else:
                print(file + ' has not changed')
                newini.set(dir, file, hasher.hexdigest())

        else:
            newini.set(dir, file, hasher.hexdigest())
            haschanged = True

    else:
        newini.set(dir, file, hasher.hexdigest())
        haschanged = True

    # Save new values to ini file
    with open(newhashfile, 'w') as configfile:
        newini.write(configfile)

    return haschanged
