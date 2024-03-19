cmake_minimum_required(VERSION 3.26)

project(MyApp LANGUAGES C CXX)
enable_testing()

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
find_package(GTest REQUIRED)

add_executable(my_app my_app.cpp)
target_link_libraries(my_app PRIVATE ZLIB::ZLIB PNG::PNG)

add_library(my_library STATIC my_library.cpp )
target_include_directories(my_library
     PUBLIC
          $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
          $<INSTALL_INTERFACE:include>
)
target_link_libraries(my_library PRIVATE ZLIB::ZLIB)

add_executable(my_library_test my_library_test.cpp)
target_link_libraries(my_library_test PRIVATE my_library GTest::gtest_main)
add_test(NAME my_library_test COMMAND my_library_test)

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

set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT my_app)