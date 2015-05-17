import os

class FileTree(object):

    def __init__(self):
        pass

class Comparer(object):

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def update_source(self):
        for root, dirs, files in os.walk(self.source):
            rel = os.path.relpath(root, self.source)

    def update(self):
        # for root, dirs, files in os.walk(self.source):
        #     rel = os.path.relpath(root, self.source)
        #
        #     for d in dirs:
        #         dest_d = os.path.join(dest, rel, d)
        #         if not os.path.isdir(dest_d):
        #             new.append(('dir', os.path.join(rel, d)))
        #     for f in files:
        #         src_f = os.path.join(source, rel, f)
        #         dest_f = os.path.join(dest, rel, f)
        #         if not os.path.isfile(dest_f):
        #             new.append(('file', os.path.join(rel, f), os.path.getsize(src_f)))
        pass


