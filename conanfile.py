from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMakeToolchain

class MyApp(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    def requirements(self):
        self.requires("zlib/[>=1.3]", options={"shared": True})
        self.requires("libpng/[>1.6.40]", options={"shared": True})

    def generate(self):
        tc = CMakeToolchain(self)
        host_deps = [dep for dep in reversed(self.dependencies.host.topological_sort.values())]
        if self.settings.os == "Windows":
            bin_dirs = [p.replace('\\','/') for dep in host_deps for p in dep.cpp_info.aggregated_components().bindirs]
            tc.variables["CONAN_RUNTIME_LIB_DIRS"] = ";".join(bin_dirs)
        elif self.settings.os in ["Linux", "Macos"]:
            lib_dirs = [p for dep in host_deps for p in dep.cpp_info.aggregated_components().libdirs]
            tc.variables["CONAN_RUNTIME_LIB_DIRS"] = ";".join(lib_dirs)
        tc.generate()

    def layout(self):
        cmake_layout(self)