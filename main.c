#include <Python.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <filename.py>\n", argv[0]);
        return 1;
    }

    const char *filename = argv[1];

    FILE *fp = fopen(filename, "r");
    if (!fp) {
        printf("Failed to open %s\n", filename);
        return 1;
    }

    Py_Initialize();

    PyRun_SimpleFile(fp, filename);
    fclose(fp);

    Py_Finalize();

    printf("\nPress Enter to exit...");
    getchar();

    return 0;
}
