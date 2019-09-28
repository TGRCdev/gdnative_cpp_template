// Include all of your GDNative classes here
//------------------------------------------
// #include "src/gdexample.h"
//------------------------------------------

extern "C" void GDN_EXPORT godot_gdnative_init(godot_gdnative_init_options *o) {
    godot::Godot::gdnative_init(o);
}

extern "C" void GDN_EXPORT godot_gdnative_terminate(godot_gdnative_terminate_options *o) {
    godot::Godot::gdnative_terminate(o);
}

extern "C" void GDN_EXPORT godot_nativescript_init(void *handle) {
    godot::Godot::nativescript_init(handle);

    // Register all of your GDNative classes here
    //--------------------------------------------
    // godot::register_class<godot::GDExample>();
    //--------------------------------------------
}