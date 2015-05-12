import os, sys

def print_help():
    print """
Usage: %s source_dir dest_dir

    """ % (sys.argv[0])

if len(sys.argv) < 3:
    print_help()
    sys.exit()

source = sys.argv[1]
dest = sys.argv[2]

new = []

for root, dirs, files in os.walk(source):
    rel = os.path.relpath(root, source)
    
    for d in dirs:
        dest_d = os.path.join(dest, rel, d)
        if not os.path.isdir(dest_d):
            new.append(('dir', os.path.join(rel, d)))
    for f in files:
        src_f = os.path.join(source, rel, f)
        dest_f = os.path.join(dest, rel, f)
        if not os.path.isfile(dest_f):
            new.append(('file', os.path.join(rel, f), os.path.getsize(src_f)))
            
dirs = 0
files = 0
size = 0
for e in new:
    if e[0] == 'dir':
        dirs += 1
    elif e[0] == 'file':
        files += 1
        size += e[2]

print "%d new dirs, %d new files - %dB in size" % (dirs, files, size)
