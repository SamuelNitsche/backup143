import filecmp

# Returns true if files are same
def file_changed(old, new):
    return not filecmp.cmp(old, new)