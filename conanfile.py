from conan import ConanFile
from conan.tools.files import save
from conan.tools.cmake import cmake_layout, CMakeToolchain
import os
class MyApp(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    def configure(self):
        self.options["zlib"].shared = True
        self.options["libpng"].shared = True

    def requirements(self):
        self.requires("zlib/[>=1.3]", options={"shared": True})
        self.requires("libpng/[>1.6.40]", options={"shared": True})
        self.requires("gtest/1.14.0")

    def generate(self):
        tc = CMakeToolchain(self)
        host_deps = [dep for dep in reversed(self.dependencies.host.topological_sort.values())]
        if self.settings.os == "Windows":
            bin_dirs = [p.replace('\\','/') for dep in host_deps for p in dep.cpp_info.aggregated_components().bindirs]
            tc.variables["CONAN_RUNTIME_LIB_DIRS"] = ";".join(bin_dirs)
        elif self.settings.os in ["Linux", "Macos"]:
            lib_dirs = [p for dep in host_deps for p in dep.cpp_info.aggregated_components().libdirs]
            tc.variables["CONAN_RUNTIME_LIB_DIRS"] = ";".join(lib_dirs)

        if self.settings.os == "Windows":
            # For CMake 3.29: set CMAKE_TEST_LAUNCHER that activates conanrun.bat 
            # before calling the test executable. This should help resolve DLLs in the Conan cache
            # without copying them
            runner_bat = os.path.join(self.generators_folder, "test_runner.bat")
            save(self, runner_bat, '@echo off\ncall "%~dp0/conanrun.bat"\n%*\n')
            runner_bat = runner_bat.replace("\\", "/")
            tc.variables["CMAKE_TEST_LAUNCHER"] = runner_bat
        
        tc.generate()

    def layout(self):
        cmake_layout(self)
