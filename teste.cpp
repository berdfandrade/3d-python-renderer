#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

// Função para carregar o código-fonte do shader de um arquivo

std::string loadShaderSource(const char *filename)
{
    std::ifstream file(filename);
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

// Função para compilar um shader

GLuint compileShader(GLenum shaderType, const char *source)
{
    GLuint shader = glCreateShader(shaderType);
    glShaderSource(shader, 1, &source, nullptr);
    glCompileShader(shader);

    // Verificar errors de compilação
    GLint sucess;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &sucess);
    if (!sucess)
    {
        char infoLog[512];
        glGetShaderInfoLog(shader, sizeof(infoLog), nullptr, infoLog);
        std::cerr << "Erro na compilação do shader:\n"
                  << infoLog << std::endl;
        return 0;
    }

    return shader;
}

// Função para criar um programa da shader e vincular os shaders

GLuint createShaderProgram(const char *vertexShaderSource, const char *fragmentShaderSource)
{
    // Compilar os shader

    /*
        Colocando as funções que escrevemos em
        cima e colocando um parametro que vai ser
        lido depois
    */

    GLuint vertexShader = compileShader(GL_VERTEX_SHADER, vertexShaderSource);
    GLuint fragmentShader = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource);

    // Criar um programa de shader

    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    // Verifica erros de vinculação
    GLint sucess;
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &sucess);
    if (!sucess)
    {
        char infoLog[512];
        glGetProgramInfoLog(shaderProgram, sizeof(infoLog), nullptr, infoLog);
        std::cerr << "Erro na vinculação do programa de shader:\n"
                  << infoLog << std::endl;
        return 0;
    }

    // Limpar recursos desnecessãrios após a vinculação
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    return shaderProgram;
}
