import glob
import os
import sys

from PyQt4.QtGui import QApplication, QTreeWidgetItem, QFileDialog, QIcon
from PyQt4.uic import loadUiType
from functools import partial

BackupUiBase, BUiQtBase = loadUiType("main.ui")

def get_dir_structure(path):

    struct = {}

    size = 0

    for entry in glob.glob(os.path.join(path, '*')):
        base = os.path.basename(entry)
        if os.path.isdir(entry):
            str_r, size_r = get_dir_structure(entry)
            struct[base] = ('dir', str_r, size_r)
            size += size_r
        elif os.path.isfile(entry):
            size_f = os.path.getsize(entry)
            size += size_f
            fp = os.path.join(path, entry)
            struct[base] = ('file', fp, size_f)

    return struct, size

def get_dir_difference(source_struct, destination_struct):

    diff = {}

    size = 0

    for name, data in source_struct.iteritems():

        if name not in destination_struct:
            diff[name] = data
            size += data[2]
            continue

        if data[0] == 'file':
            if data[2] != destination_struct[name][2]:
                print "file %s has different sizes: %d vs %d" % (name, data[2], destination_struct[name][2])
                print "file path is [%s] [%s]" % (data[1], destination_struct[name][1])
                diff[name] = data
                size += data[2]
            else:
                pass  # TODO check contents

        elif data[0] == 'dir':
            diff_r, size_r = get_dir_difference(data[1], destination_struct[name][1])

            size += size_r

            if len(diff_r) > 0:
                diff[name] = ('dir', diff_r, size_r)

    return diff, size

def copy_file_with_progress(src, dest, progress_func, buffer_size=65536):
    src_f = open(src, 'rb')
    dest_f = open(dest, 'wb')

    while True:
        buffer = src_f.read(buffer_size)

        if len(buffer) <= 0:
            break

        dest_f.write(buffer)

        progress_func(len(buffer))

    src_f.close()
    dest_f.close()

def copy_new_files(source_path, destination_path, difference, progress_func, options=None):
    if options is None:
        options = {}

    backup_overwritten = options.get('backup_overwritten', False)
    backup_suffix = options.get('backup_suffix', '~bt')

    queue = [(difference, '')]

    while len(queue) > 0:
        baseobj, basepath = queue.pop()
        for name, data in baseobj.iteritems():
            path = os.path.join(basepath, name)
            dest_path = os.path.join(destination_path, path)
            src_path = os.path.join(source_path, path)
            if data[0] == 'dir':
                if not os.path.isdir(dest_path):
                    print "creating directory [%s]" % (dest_path)
                    os.mkdir(dest_path)
                queue.append((data[1], path))
            elif data[0] == 'file':
                if os.path.isfile(dest_path):
                    if backup_overwritten:
                        backup_path = dest_path + backup_suffix
                        if os.path.isfile(backup_path):
                            print "warning, removing (backup?) file [%s]" % (backup_path)
                            os.remove(backup_path)

                        print "saving file [%s] to [%s]" % (dest_path, backup_path)
                        os.rename(dest_path, backup_path)

                    print "removing old file [%s]" % (dest_path)
                    os.remove(dest_path)

                print "copying file [%s] to [%s]" % (src_path, dest_path)
                copy_file_with_progress(src_path, dest_path, progress_func)

def format_size(size):
    if size < 2048:
        return '%d B' % (size)

    if size < 1024**2 * 2:
        return '%d kB' % (size / 1024)

    if size < 1024**3 * 2:
        return '%d MB' % (size / 1024**2)

    if size < 1024**4 * 2:
        return '%d GB' % (size / 1024**3)

    return '%d TB' % (size / 1024**4)

# noinspection PyAttributeOutsideInit
class BackupUi(BackupUiBase, BUiQtBase):

    def __init__(self):
        BUiQtBase.__init__(self)

        self.setupUi(self)
        
        self.source_view.setColumnCount(3)
        self.destination_view.setColumnCount(3)

        self.source_view.setHeaderItem(QTreeWidgetItem(['kind', 'path', 'size']))

        self.source_browse.clicked.connect(partial(self.browse_for_dir, self.source_browse))
        self.destination_browse.clicked.connect(partial(self.browse_for_dir, self.destination_browse))

        self.source_path.setText(r'd:\media')
        self.destination_path.setText(r'e:\media')
        # self.source_path.setText(r'd:\work\054_backup_tool\qtui\test_src')
        # self.destination_path.setText(r'd:\work\054_backup_tool\qtui\test_dest')

        self.scan_button.clicked.connect(self.scan_directories)
        self.copy_button.clicked.connect(self.copy_new_files)

        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(1000)
        self.progress_bar.hide()

        self.source_struct = None
        self.destination_struct = None
        self.difference = None

    def browse_for_dir(self, button):
        # noinspection PyCallByClass
        dir_path = QFileDialog.getExistingDirectory(self, "Select a directory")
        if button == self.source_browse:
            self.source_path.setText(dir_path)
        elif button == self.destination_browse:
            self.destination_path.setText(dir_path)
        else:
            print "other?"

    def scan_directories(self):
        source_dir = str(self.source_path.text())
        destination_dir = str(self.destination_path.text())

        if not os.path.isdir(source_dir):
            self.error_message("Source directory is invalid")
            return

        if not os.path.isdir(destination_dir):
            self.error_message("Destination directory is invalid")
            return

        self.source_struct, self.source_size = get_dir_structure(source_dir)
        self.destination_struct, self.destination_size = get_dir_structure(destination_dir)

        self.difference, self.difference_size = get_dir_difference(self.source_struct, self.destination_struct)

        self.source_size_label.setText("difference: %s" % (format_size(self.difference_size)))

        self.update_source_view()

    def update_source_view(self):
        if self.difference is None:
            return

        self.source_view.clear()

        queue = [(self.difference, self.source_view.addTopLevelItem)]

        while len(queue) > 0:
            baseobj, inserter = queue.pop()
            for name, data in baseobj.iteritems():
                if data[0] == 'dir':
                    child = QTreeWidgetItem(['', name, format_size(data[2])])
                    child.setIcon(0, QIcon('dir_icon.png'))
                    inserter(child)
                    queue.append((data[1], child.addChild))
                elif data[0] == 'file':
                    entry = QTreeWidgetItem(['', name, format_size(data[2])])
                    entry.setIcon(0, QIcon('file_icon.png'))
                    inserter(entry)

    def progress_cb(self, count):
        self.total_count += count

        self.progress_bar.setValue(1000 * self.total_count / self.difference_size)
        args = tuple(map(format_size, [self.total_count, self.difference_size]))
        self.info_label.setText('Copied %s of %s total' % args)

    def copy_new_files(self):
        source_dir = str(self.source_path.text())
        destination_dir = str(self.destination_path.text())

        self.total_count = 0

        self.progress_bar.setValue(0)
        self.progress_bar.show()

        copy_new_files(source_dir, destination_dir, self.difference, self.progress_cb)

    def error_message(self, message):
        self.info_label.setText(message)
        self.info_label.show()

app = QApplication(sys.argv)

main = BackupUi()
main.show()

app.exec_()
