#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

// Função para carregar o código-fonte do shader de um arquivo 

std::string loadShaderSource(const char* filename){
    std::ifstream file(filename);
    std::stringstream buffer; 
    buffer << file.rdbuf(); 
    return buffer.str();
}

// Função para compilar um shader

GLuint compileShader(GLenum shaderType, const char* source) {
    GLuint shader = glCreateShader(shaderType);
    glShaderSource(shader, 1, &source, nullptr);
    glCompileShader(shader);

    // Verificar errors de compilação
    GLint sucess;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &sucess);
    if(!sucess){
        char infoLog[512];
        glGetShaderInfoLog(shader, sizeof(infoLog), nullptr, infoLog);
        std::cerr << "Erro na compilação do shader:\n" << infoLog << std::endl;
        return 0;
    }

    return shader; 

}