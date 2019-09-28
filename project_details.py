#------------------------------------------------------------------------------
# Edit stuff below for your project

# Directories where all of your source files are contained
# These aren't recursively searched, so you need to define child dirs too
# i.e. ["src", "src/foo", "thirdparty/bar/src"]
src_paths = ["src"] # Just the directories, individual files will be found within

# Include paths, for directories containing headers
# i.e. ["thirdparty/foo/include"]
inc_paths = []

# Module name, used for Godot module build, and GDNative output formatting
# Set this to the name of your module
module_name = "gdexample"

# GDNative library file name
# Valid substitutions:
# NAME = module name
# PLATFORM = target platform
# BITS = target bits, or android architecture if building for android
# TARGET = build type
gdnative_output = "bin/{NAME}.{PLATFORM}.{BITS}"

# Path to your godot-cpp folder.
# https://github.com/GodotNativeTools/godot-cpp
godot_cpp_path = "thirdparty/godot-cpp"
#------------------------------------------------------------------------------