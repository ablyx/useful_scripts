import os
import sys

# use at your own risk.
# This is not very well written. I think there is an endless loop in the check skip?

FOLDERS_OF_INTEREST = ["lib","bin", "sbin", "usr"]
SKIP_FOLDERS = ["/lib/modules", ]
def is_elf(file_path):
    try:
        f = open(file_path, 'rb')
        magic_bytes = f.read(4)
        f.close()
    except:
        return False
    return magic_bytes == b"\x7fELF"

def search_folder(search_str, folder):
    if folder in SKIP_FOLDERS:
        return
    try:
        for f in os.listdir(folder):
            p = os.path.join(folder, f)
            if os.path.isfile(p):
                file_path = p
                if not is_elf(file_path):
                    continue
                # need to capture input here
                raw_out = os.popen(f"ldd {file_path}").read()
                if search_str in raw_out:
                    # print(file_path)
                    pass
            elif os.path.isdir(p):
                check_skip = folder == "/"
                if check_skip:
                    skip = True
                    for i in FOLDERS_OF_INTEREST:
                        if i in p:
                            skip = False
                            break
                    if skip:
                        continue
                print(p)
                search_folder(search_str, p)
            else:
                # probably should use logging instead of print
                # print(f"{p} is not file or dir")
                pass
    except PermissionError:
        # print(f"Permission error for {folder}")
        pass

if __name__ == "__main__":
    search_str = sys.argv[1]
    search_folder(search_str, "/")
