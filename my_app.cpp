#include <iostream>
#include <cstring>
#include <png.h>
#include <zlib.h>

int main(int argc, char** argv) {
    char buffer_in [32] = {"Conan Package Manager"};
    char buffer_out [32] = {0};

    z_stream defstream;
    defstream.zalloc = Z_NULL;
    defstream.zfree = Z_NULL;
    defstream.opaque = Z_NULL;
    defstream.avail_in = (uInt) strlen(buffer_in);
    defstream.next_in = (Bytef *) buffer_in;
    defstream.avail_out = (uInt) sizeof(buffer_out);
    defstream.next_out = (Bytef *) buffer_out;

    deflateInit(&defstream, Z_BEST_COMPRESSION);
    deflate(&defstream, Z_FINISH);
    deflateEnd(&defstream);

    std::cout << "Compressed size is: " << strlen(buffer_in) << "\n";
    std::cout << "Compressed string is: " << buffer_in << "\n";
    std::cout << "Compressed size is: " << strlen(buffer_out) << "\n";
    std::cout << "ZLIB_VERSION is: " << zlibVersion() << "\n";

    png_structp png_ptr;
    png_infop info_ptr;

    std::cout << "Libpng is: " << PNG_LIBPNG_VER_STRING << "\n";

    // fprintf(stderr, "   Compiled with libpng %s; using libpng %s.\n", PNG_LIBPNG_VER_STRING, png_libpng_ver);
    png_ptr = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    info_ptr = png_create_info_struct(png_ptr);

    return EXIT_SUCCESS;
}