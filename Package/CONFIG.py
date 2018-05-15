import ops
import iopc

pkg_path = ""
output_dir = ""
arch = ""
output_platform_dir = ""
src_image_cfg = ""
dao_file = "dao.ini"
dao_script = "dao.py"

def set_global(args):
    global pkg_path
    global output_dir
    global arch
    global src_image_cfg
    global output_platform_dir

    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    arch = ops.getEnv("ARCH_ALT")
    src_image_cfg = ops.path_join(pkg_path, dao_file)
    output_platform_dir = ops.path_join(iopc.getOutputRootDir(), "platform")
    #dst_include_dir = ops.path_join("include",args["pkg_name"])

def MAIN_ENV(args):
    set_global(args)

    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.mkdir(output_platform_dir)
    ops.copyto(src_image_cfg, ops.path_join(output_platform_dir, dao_file))
    ops.copyto(ops.path_join(pkg_path, dao_script), output_dir)
    ops.copyto(ops.path_join(pkg_path, dao_file), output_dir)

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

    CMD=['python', dao_script, dao_file]
    ops.execCmd(CMD, output_dir, False)

    return False

def MAIN_INSTALL(args):
    set_global(args)

    #iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_lib_dir, "."), "usr/lib")
    ops.copyto(ops.path_join(output_dir, 'db_init.bin'), iopc.getOutputRootDir())
    #iopc.installBin(args["pkg_name"], ops.path_join(output_dir, "db_init.inc"), dst_include_dir)

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)
    return False

def MAIN(args):
    set_global(args)

