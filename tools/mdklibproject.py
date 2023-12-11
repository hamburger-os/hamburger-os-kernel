import os
import shutil
import string

def ReadFileType(path,file_type): 
    filenames = os.listdir(path) 
    filenames1 = []
    for filename in filenames:
        if os.path.splitext(filename)[1] == file_type:
            filenames1.append(filename)
    return filenames1

def MDK45ProjectByLib(target, link_modules):

    if os.path.isfile(target) is False:
        print ('Warning: The file [project.uvprojx] not found!')
        return

    file_data = []
    line_num = 0
    start_line = 0
    end_line = 0

    target_file = open(target, 'r')
    lines = target_file.readlines()
    target_file.close()

    for line in lines:
        line_num = line_num + 1
        if '<Groups>' in line:
            start_line = line_num
        elif '</Groups>' in line:
            end_line = line_num
            break

    start_line = start_line + 1
    end_line = end_line - 1

    file_data = lines[0:start_line]
    lib_list = ['<GroupName>lib</GroupName>\n',
                '<Files>\n',
                '<File>\n',
                '<FileName>rt-thread.lib</FileName>\n',
                '<FileType>4</FileType>\n',
                '<FilePath>.\lib\\rt-thread.lib</FilePath>\n',
                '<FileOption>\n',
                '<CommonProperty>\n',
                '<UseCPPCompiler>2</UseCPPCompiler>\n',
                '<RVCTCodeConst>0</RVCTCodeConst>\n',
                '<RVCTZI>0</RVCTZI>\n',
                '<RVCTOtherData>0</RVCTOtherData>\n',
                '<ModuleSelection>1</ModuleSelection>\n',
                '<IncludeInBuild>2</IncludeInBuild>\n',
                '<AlwaysBuild>2</AlwaysBuild>\n',
                '<GenerateAssemblyFile>2</GenerateAssemblyFile>\n',
                '<AssembleAssemblyFile>2</AssembleAssemblyFile>\n',
                '<PublicsOnly>2</PublicsOnly>\n',
                '<StopOnExitCode>11</StopOnExitCode>\n',
                '<CustomArgument></CustomArgument>\n',
                '<IncludeLibraryModules>main.o|1|0|0|0,fs_test.o|1|0|0|0</IncludeLibraryModules>\n',
                '<ComprImg>1</ComprImg>\n',
                '</CommonProperty>\n',
                '<FileArmAds/>\n',
                '</FileOption>\n',
                '</File>\n',
                '</Files>\n']

    modules = '<IncludeLibraryModules>'
    for m in link_modules:
        modules = modules + m +'|1|0|0|0,'
    modules = modules[:-1] + '</IncludeLibraryModules>\n'
    # print(modules)
    lib_list[20] = modules

    file_data = file_data + lib_list
    file_data = file_data + lines[end_line-1:]

    new_file = open(target, 'w')

    new_file.writelines(file_data)

    new_file.close()

def MDKLibProject(objects):
    if os.path.isfile('project.uvprojx'):
        shutil.copy('project.uvprojx', 'swos2_lib')
    if os.path.isfile('project.uvoptx'):
        shutil.copy('project.uvoptx', 'swos2_lib')

    modules = ReadFileType('build/keil_lib/Obj', '.o')
    MDK45ProjectByLib('swos2_lib/project.uvprojx', modules)
