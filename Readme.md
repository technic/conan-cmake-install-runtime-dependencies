# Linux

```
conan install . --build=missing
cmake . --preset=conan-release
cmake --build . --preset=conan-release

mkdir build/Release/install
cmake --install build/Release --prefix=$(pwd)/build/Release/install
```

On Linux:
- The installed executable should have `$ORIGIN/../lib` as part of its `RUNPATH` (or `RPATH`) entries
- The required `.so` files have been copied into the install directory:

```
./build/Release/install
|-- bin
|   `-- my_app
`-- lib
    |-- libpng16.so.16 -> libpng16.so.16.43.0
    |-- libpng16.so.16.43.0
    |-- libz.so.1 -> libz.so.1.3.1
    `-- libz.so.1.3.1
```


# Windows

```
# Install dependencies
conan install --build=missing

# Configure CMake and build project
cmake . --preset=conan-default
cmake --build . --preset=conan-release

# Install and bundle runtime dependencies
mkdir install
cmake --install build --prefix=install
```