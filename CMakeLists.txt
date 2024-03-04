cmake_minimum_required(VERSION 3.26)

project(MyApp LANGUAGES C CXX)

include(GNUInstallDirs)

file(RELATIVE_PATH relative_lib_dir
     ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}
     ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}
)

if(APPLE)
    set(rpath_base @executable_path)
else()
    set(rpath_base $ORIGIN)
endif()

set(CMAKE_INSTALL_RPATH ${rpath_base} ${rpath_base}/${relative_lib_dir})

find_package(ZLIB REQUIRED)
find_package(PNG REQUIRED)

add_executable(my_app my_app.cpp)
target_link_libraries(my_app PRIVATE ZLIB::ZLIB PNG::PNG)


install(TARGETS my_app
    DESTINATION ${CMAKE_INSTALL_BINDIR}
    RUNTIME_DEPENDENCY_SET my_app_deps
)

install(RUNTIME_DEPENDENCY_SET my_app_deps
    PRE_EXCLUDE_REGEXES
        [[api-ms-win-.*]]
        [[ext-ms-.*]]
        [[kernel32\.dll]]
        [[libc\.so\..*]] [[libgcc_s\.so\..*]] [[libm\.so\..*]] [[libstdc\+\+\.so\..*]]
    POST_EXCLUDE_REGEXES
        [[.*/system32/.*\.dll]]
        [[^/lib.*]]
        [[^/usr/lib.*]]
    DIRECTORIES ${CONAN_RUNTIME_LIB_DIRS}
)
