import os
import sys
import string
import shutil

def MDKLIBCreatDir(all_path):
    swos2_lib_path = "swos2_lib/lib"
    head_path = []
    dir_type = ''

    if not os.path.exists(swos2_lib_path):
        os.makedirs(swos2_lib_path)
    else:
        print(swos2_lib_path + " already exists")

    current_path = os.path.abspath(os.getcwd())
    parent_path = os.path.dirname(current_path)
    if not os.path.exists('../mkrootfs.bat'):
        dir_name = os.path.basename(current_path)
    else:
        dir_name = os.path.basename(parent_path)

    for path in all_path:
        path = path.replace('\\', '/')
        index = path.find(dir_name)
        # print("index = %d", index)
        if index >= 0:
            index = index + len(dir_name) + 1
            head_path.append("swos2_lib/" + path[index:])
        else:
            head_path.append("swos2_lib/" + path)

    for path in head_path:
        # print(path)
        if not os.path.exists(path):
            os.makedirs(path)

    return head_path

def SFileToDFile(source_file, file_class, dest_file):
    for filenames in os.listdir(source_file):
        file_path = os.path.join(source_file, filenames)
        if os.path.isfile(file_path):
            if file_path.endswith(file_class):
                # print('copy %s'% file_path + ' To ' + dest_file)
                shutil.copy2(file_path, dest_file)

def MDKLibMVCPPH(all_path):
    full_head_path = []
    head_path = []
    lose_path = ['rt-thread\\components\\drivers\\include\\drivers',
                'rt-thread\\components\\drivers\\include\\ipc',
                'rt-thread\\components\\libc\\compilers\\common\\include\\sys',
                'rt-thread\\components\\libc\\compilers\\common\\extension\\sys',]

    full_head_path = all_path

    for path in lose_path:
        if any(path in s for s in all_path):
            print(path + " already exists")
        else:
            full_head_path.append(path)

    head_path = MDKLIBCreatDir(full_head_path)

    if head_path == "dir error":
        return "dir error"

    for src_path, dest_path in zip(full_head_path, head_path):
        # print(src_path, ':', dest_path)
        SFileToDFile(src_path, '.h', dest_path)

    # make linker_scripts dir
    linker_dir = 'swos2_lib/board/linker_scripts'
    if not os.path.exists(linker_dir):
        os.makedirs(linker_dir)
    # copy link.icf link.lds link.sct file
    shutil.copy2('board/linker_scripts/link.icf', 'swos2_lib/board/linker_scripts')
    shutil.copy2('board/linker_scripts/link.lds', 'swos2_lib/board/linker_scripts')
    shutil.copy2('board/linker_scripts/link.sct', 'swos2_lib/board/linker_scripts')
