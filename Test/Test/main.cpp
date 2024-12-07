#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <sstream>

#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif 

char* readFileToString(const char* filename) {
    std::ifstream file(filename, std::ios::in | std::ios::binary);
    if (!file.is_open()) {
        perror("File reading Error!");
        return nullptr;
    }

    std::ostringstream contentStream;
    contentStream << file.rdbuf();
    std::string content = contentStream.str();
    char* result = new char[content.size() + 1];
    std::copy(content.begin(), content.end(), result);
    result[content.size()] = '\0';
    return result;
}

int main(int argc, char* argv[]) {
    const char* Path = "C:\\Users\\skyla\\Desktop\\Yolo_FoodDeteced-main\\yolo 모델 활용 잔반 처리 인식.py";

    // 파일 경로 설정
    char* Python_code = readFileToString(Path);
    if (Python_code == nullptr) {
        return 1;
    }

    Py_Initialize();
    if (PyRun_SimpleString(Python_code) != 0) {
        std::cerr << "Python Error!\n";
    }
    Py_Finalize();

    delete[] Python_code;
    return 0;
}
