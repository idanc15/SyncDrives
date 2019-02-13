
from os import listdir, makedirs, remove
from os.path import isfile, join, exists
from os import walk
import sys
from shutil import copyfile

#TODO: sync with google drive


def banner():
    print "      _________                     ________        .__                     "
    print " /   _____/__.__. ____   ____   \______ \_______|__|__  __ ____   ______"
    print " \_____  <   |  |/    \_/ ___\   |    |  \_  __ \  \  \/ // __ \ /  ___/"
    print " /        \___  |   |  \  \___   |    `   \  | \/  |\   /\  ___/ \___ \ "
    print "/_______  / ____|___|  /\___  > /_______  /__|  |__| \_/  \___  >____  >"
    print "        \/\/         \/     \/          \/                    \/     \/ "
    print "[*] RAID 1 - Mirroring between two HDD"
    print "[*] Usage: python main.py /path/a/ /path/b/"


def args_check():
    if len(sys.argv) < 3:
        print "[x] Error: cmd arguments"
        banner()
        exit(1)


def list_drive(path_to_drive):
    dirs = []
    files = []
    output_list = []

    for root, directories, filenames in walk(path_to_drive):
        for directory in directories:
            dirs.append(join(root, directory))
            #print join(root, directory)
        for filename in filenames:
            #print join(root,filename)
            files.append(join(root, filename))
    try:
        output_list.append(dirs)
        output_list.append(files)

    except:
        print "[x] Error while appending lists"

    return output_list


def list_diff(source,dst,source_path,dst_path):
    source = remove_base_dir_l(source, source_path) # Clean the source paths
    dst = remove_base_dir_l(dst, dst_path) # Clean the dst paths
    return list(set(source) - set(dst))

def remove_base_dir(item,base_path):
    return item.replace(base_path,'')


def copy_files(source_path,dst_path,list):
    count = len(list)
    for item in list:
        print item
        # Store the path without the base
        tmp = remove_base_dir(item,source_path)
        # Split the rest of the path
        filename = tmp.split("/")
        path = tmp.replace(filename[-1],'')
        # Create dir if not exist
        if not exists(dst_path+path):
            makedirs(dst_path+path)
        # Copy the file from source to dst
        copyfile(item, dst_path+tmp)
        #print "[+] " + item + " Copied successfuly"
        count = count -1
        print "[+] Copying file " + str(count) + " out of " +str(len(list)) 

def remove_files(file_array,dst_path,source_path):
    count = len(file_array)
    for item in file_array:
        tmp = remove_base_dir(item,dst_path)
        if not exists(source_path+tmp):
            remove(item)
            count = count - 1
            print "[+] Deleting file " + str(count) + " out of " + str(len(file_array))


def main():
    #Find uniqe files
    need_to_copy = len(list_diff(source_list[1], dst_list[1], path_to_drive_a, path_to_drive_b))
    need_to_delete = len(list_diff(dst_list[1], source_list[1], path_to_drive_b, path_to_drive_a))
    print "[+] " + str(need_to_copy) + " files will be copied"
    print "[+] " + str(need_to_delete) + " files will be deleted"
    
    # if there is a diff then copy/delete - recursive
    if need_to_copy > 0:
        # Copy missing files
        copy_files(path_to_drive_a,path_to_drive_b,list_diff(source_list[1], dst_list[1], path_to_drive_a, path_to_drive_b))
    elif need_to_delete > 0:
        # Delete unwanted files from dst
        remove_files(list_diff(dst_list[1], source_list[1], path_to_drive_a, path_to_drive_b),path_to_drive_b,path_to_drive_a)
    else:
        print "[+] No action is needed. Exiting"
        exit(0)

if __name__ == "__main__":
    # verify the cmd args
    args_check()

    #Set path variables
    path_to_drive_a = sys.argv[1]
    path_to_drive_b = sys.argv[2]

    # Create lists
    print "[+] Mapping Drives..."
    source_list = list_drive(path_to_drive_a)
    dst_list = list_drive(path_to_drive_b)

    main()


