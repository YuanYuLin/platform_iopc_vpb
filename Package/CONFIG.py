import ops
import iopc

pkg_path = ""
output_dir = ""
arch = ""
output_platform_dir = ""
#dao_file = "dao.ini"
dao_files = ["dao"]

def set_global(args):
    global pkg_path
    global output_dir
    global arch
    global output_platform_dir
    global install_platform_dao
    global dao_script

    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    arch = ops.getEnv("ARCH_ALT")
    output_platform_dir = ops.path_join(iopc.getOutputRootDir(), "platform")
    dao_script = ops.path_join(output_platform_dir, "dao.py")

    install_platform_dao = False
    if ops.getEnv("INSTALL_PLATFORM_DAO") == 'y' :
        install_platform_dao = True

def MAIN_ENV(args):
    set_global(args)

    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.mkdir(output_platform_dir)
    for ini in dao_files:
        dao_file = ops.path_join(pkg_path, ini + ".ini")
        ops.copyto(dao_file, output_platform_dir)
        ops.copyto(dao_file, output_dir)

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(output_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)
    return False

def MAIN_BUILD(args):
    set_global(args)

    if install_platform_dao == True :
        for ini in dao_files:
            dao_file = ops.path_join(output_platform_dir, ini + ".ini")
            dao_bin = ops.path_join(output_platform_dir, ini + ".bin")
            CMD=['python', dao_script, dao_file, dao_bin]
            print CMD
            ops.execCmd(CMD, output_dir, False)

    return False

def MAIN_INSTALL(args):
    set_global(args)

    if install_platform_dao == True :
        #iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_lib_dir, "."), "usr/lib")
        #ops.copyto(ops.path_join(output_dir, 'db_init.bin'), iopc.getOutputRootDir())
        #ops.copyto(ops.path_join(output_dir, 'img_header.bin'), iopc.getOutputRootDir())
        iopc.installBin(args["pkg_name"], ops.path_join(output_dir, "db_init.inc"), 'include/platform')

    return False

def MAIN_SDKENV(args):
    set_global(args)
    return False

def MAIN_SDKENV(args):
    set_global(args)

    cflags = ""
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), 'usr/include/platform')
    iopc.add_includes(cflags)

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)
    return False

def MAIN(args):
    set_global(args)

