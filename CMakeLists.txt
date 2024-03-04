cmake_minimum_required(VERSION 3.26)

project(MyApp LANGUAGES C CXX)

find_package(ZLIB REQUIRED)

add_executable(my_app my_app.cpp)
target_link_libraries(my_app PRIVATE ZLIB::ZLIB)


install(TARGETS my_app
    DESTINATION ${CMAKE_INSTALL_BINDIR}
    RUNTIME_DEPENDENCY_SET my_app_deps
)

install(RUNTIME_DEPENDENCY_SET my_app_deps
    PRE_EXCLUDE_REGEXES
        [[api-ms-win-.*]]
        [[ext-ms-.*]]
        [[kernel32\.dll]]
    POST_EXCLUDE_REGEXES
        [[.*/system32/.*\.dll]]
    DIRECTORIES ${CONAN_DLL_BIN_DIRS}
)