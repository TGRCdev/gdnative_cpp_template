# All the variables needed to build are within project_details.py
# You shouldn't need to edit this unless you have a specific setup

from project_details import *
import os
import platform

# Detect platform
platform_names = {
    "Linux":"linux",
    "Darwin":"osx",
    "Windows":"windows"
}
host_platform = platform_names.get(platform.system(), "")

# Detect host bits
host_bits = "64" if platform.machine().endswith('64') else "32"

opts = Variables([], ARGUMENTS)
opts.Add(PathVariable("godot_cpp", "The path to your godot-cpp folder", godot_cpp_path, PathVariable.PathIsDir))
opts.Add(EnumVariable("platform", "The target platform to compile for", host_platform, ["windows", "linux", "osx", "android"], ignorecase=2))
opts.Add(EnumVariable("bits", "The target bits to compile for", host_bits, ["32", "64"]))
opts.Add(EnumVariable("target", "The type of compilation to run", "debug", ["release", "debug"], ignorecase=2))
opts.Add(EnumVariable("android_arch", "The target Android architecture (android builds only)", "armv7", ["armv7", "arm64v8", "x86", "x86_64"], ignorecase=2))
opts.Add("ndk_platform", "The target Android API level (android builds only)", 18 if ARGUMENTS.get("android_platform") in ["armv7", "x86"] else 21)
opts.Add(PathVariable("ANDROID_NDK_ROOT", "The path to your Android NDK installation (android builds only). By default, pulls from environment variables.", os.environ.get("ANDROID_NDK_ROOT", ""), PathVariable.PathAccept))

env = Environment()
opts.Update(env)
Help(opts.GenerateHelpText(env))

# Workaround for MinGW. See:
# http://www.scons.org/wiki/LongCmdLinesOnWin32
if (os.name=="nt"):
    import subprocess
    
    def mySubProcess(cmdline,env):
        #print "SPAWNED : " + cmdline
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, startupinfo=startupinfo, shell = False, env = env)
        data, err = proc.communicate()
        rv = proc.wait()
        if rv:
            print("=====")
            print(err.decode("utf-8"))
            print("=====")
        return rv
        
    def mySpawn(sh, escape, cmd, args, env):
                        
        newargs = ' '.join(args[1:])
        cmdline = cmd + " " + newargs
        
        rv=0
        if len(cmdline) > 32000 and cmd.endswith("ar") :
            cmdline = cmd + " " + args[1] + " " + args[2] + " "
            for i in range(3,len(args)) :
                rv = mySubProcess( cmdline + args[i], env )
                if rv :
                    break    
        else:                
            rv = mySubProcess( cmdline, env )
            
        return rv

# Platform specifics
if env['platform'] == 'windows':
    if env['bits'] == '32':
        env = Environment(TARGET_ARCH='x86')
    else:
        env = Environment(TARGET_ARCH='x86_64')
    opts.Update(env);

    env.Append(LINKFLAGS=['/WX'])
    if env['target'] == 'debug':
        env.Append(CCFLAGS=['/Z7', '/Od', '/EHsc', '/D_DEBUG', '/MDd'])
    elif env['target'] == 'release':
        env.Append(CCFLAGS=['/O2', '/EHsc', '/DNDEBUG', '/MD'])

elif env['platform'] == 'linux':
    if env['target'] == 'debug': env.Append(CCFLAGS=["-g", "-Og"])
    else: env.Append(CCFLAGS=['-O3'], LINKFLAGS=['-s'])
    
    if env['bits'] == '32': env.Append(CCFLAGS=['-m32'])
    else: env.Append(CCFLAGS=['-m64'])

elif env['platform'] == 'osx':
    if env['target'] == 'debug': env.Append(CCFLAGS=['-g', '-Og'])
    else: env.Append(CCFLAGS=['-O2'], LINKFLAGS=['-Wl,-s'])

elif env['platform'] == 'android':
    if host_platform == "windows":
        env = env.Clone(tools=['mingw'])
        env["SPAWN"] = mySpawn

    # Check for NDK
    if env['ANDROID_NDK_ROOT'] == "":
        print("ERR: Could not find your Android NDK installation. Please set ANDROID_NDK_ROOT to a path to your Android NDK installation.")
        Exit(1)
    
    # Validate API level
    if (int(env['ndk_platform']) < 21) and env['android_arch'] in ['arm64v8', 'x86_64']:
        print("ERR: 64-bit Android architectures require an API level of at least 21.")
        Exit(1)
    
    # Get NDK toolchain
    toolchain = env['ANDROID_NDK_ROOT'] + "/toolchains/llvm/prebuilt/"
    if host_platform == "windows":
        toolchain += "windows"
        if host_bits == "64":
            toolchain += "-x86_64"
    elif host_platform == "linux":
        toolchain += "linux-x86_64"
    elif host_platform == "osx":
        toolchain += "darwin-x86_64"
    toolchain += "/bin/"

    arch_to_tool = {"armv7": "arm-linux-androideabi", "arm64v8": "aarch64-linux-android", "x86": "i686-linux-android", "x86_64": "x86_64-linux-android"}
    arch_to_clang = {"armv7": "armv7a-linux-androideabi", "arm64v8": "aarch64-linux-android", "x86": "i686-linux-android", "x86_64": "x86_64-linux-android"}

    cmd = ""
    if host_platform == "windows":
        cmd = ".cmd"

    env["CC"] = toolchain + arch_to_clang[env['android_arch']] + str(env['ndk_platform']) + "-clang" + cmd
    env["CXX"] = toolchain + arch_to_clang[env['android_arch']] + str(env['ndk_platform']) + "-clang++" + cmd
    env["LINK"] = env["CXX"]
    env["STRIP"] = toolchain + arch_to_tool[env['android_arch']] + "-strip"
    env["SHLIBPREFIX"] = "lib"
    env["SHLIBSUFFIX"] = ".so"

    def find_ixes_wrapper(self, paths, prefix, suffix): # Prevents bad linker flags
        if prefix == 'LIBPREFIX' and suffix == 'LIBSUFFIX':
            return False
        else:
            return self.old_ixes(paths, prefix, suffix)
    
    from types import MethodType
    env.old_ixes = env.FindIxes
    env.FindIxes = MethodType(find_ixes_wrapper, env)

    if env['target'] == 'debug': env.Append(CCFLAGS=['-g', '-Og'])
    else: env.Append(CCFLAGS=['-O2'], LINKFLAGS=['-Wl,-s'])

env.Append(CPPDEFINES=["GDNATIVE"])

# Get sources and includes
source_files = ["gdlibrary.cpp"]
for path in src_paths:
    source_files += Glob(path + "/*.cpp")
    source_files += Glob(path + "/*.c")
env.Append(CPPPATH=inc_paths)

# Get godot-cpp libs and includes
godot_cpp_inc = [
    env['godot_cpp'] + "/include/core",
    env['godot_cpp'] + "/include/gen",
    env['godot_cpp'] + "/include",
    env['godot_cpp'] + "/godot_headers"
]
env.Append(CPPPATH=godot_cpp_inc, LIBPATH=[env['godot_cpp'] + "/bin"], LIBS=["libgodot-cpp.{}.{}.{}".format(host_platform, env['target'], env['bits'])])

format_dict = {"NAME":module_name,"BITS":env['bits'] if env['platform'] != 'android' else env['android_arch'], "TARGET":env['target'], "PLATFORM":env['platform']}
env.SharedLibrary(gdnative_output.format(**format_dict) + env['SHLIBSUFFIX'], source=source_files)