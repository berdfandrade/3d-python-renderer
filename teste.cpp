#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

// Função para carregar o código-fonte do shader de um arquivo
std::string loadShaderSource(const char* filename) {
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

    // Verificar erros de compilação
    GLint success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success) {
        char infoLog[512];
        glGetShaderInfoLog(shader, sizeof(infoLog), nullptr, infoLog);
        std::cerr << "Erro na compilação do shader:\n" << infoLog << std::endl;
        return 0;
    }

    return shader;
}

// Função para criar um programa de shader e vincular os shaders
GLuint createShaderProgram(const char* vertexShaderSource, const char* fragmentShaderSource) {
    // Compilar shaders
    GLuint vertexShader = compileShader(GL_VERTEX_SHADER, vertexShaderSource);
    GLuint fragmentShader = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource);

    // Criar programa de shader
    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    // Verificar erros de vinculação
    GLint success;
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
    if (!success) {
        char infoLog[512];
        glGetProgramInfoLog(shaderProgram, sizeof(infoLog), nullptr, infoLog);
        std::cerr << "Erro na vinculação do programa de shader:\n" << infoLog << std::endl;
        return 0;
    }

    // Limpar recursos desnecessários após a vinculação
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    return shaderProgram;
}

int main() {
    // Inicializar GLFW
    if (!glfwInit()) {
        std::cerr << "Falha ao inicializar GLFW" << std::endl;
        return -1;
    }

    // Configurar GLFW
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // Criar janela
    GLFWwindow* window = glfwCreateWindow(800, 600, "Meu Programa OpenGL", nullptr, nullptr);
    if (!window) {
        std::cerr << "Falha ao criar janela GLFW" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    // Inicializar GLEW
    if (glewInit() != GLEW_OK) {
        std::cerr << "Falha ao inicializar GLEW" << std::endl;
        glfwTerminate();
        return -1;
    }

    // Definir a função de visualização de portas de exibição (viewport)
    glViewport(0, 0, 800, 600);

    // Carregar shaders
    std::string vertexShaderSource = loadShaderSource("caminho/do/seu/vertex_shader.glsl");
    std::string fragmentShaderSource = loadShaderSource("caminho/do/seu/fragment_shader.glsl");

    // Criar programa de shader
    GLuint shaderProgram = createShaderProgram(vertexShaderSource.c_str(), fragmentShaderSource.c_str());

    // Verificar se o programa de shader foi criado com sucesso
    if (!shaderProgram) {
        glfwTerminate();
        return -1;
    }

    // Loop principal
    while (!glfwWindowShouldClose(window)) {
        // Lógica de entrada, se necessário

        // Limpar a tela
        glClear(GL_COLOR_BUFFER_BIT);

        // Usar o programa de shader
        glUseProgram(shaderProgram);

        // Renderizar cubo ou outras operações de renderização

        // Trocar os buffers e verificar eventos GLFW
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // Limpar recursos e finalizar GLFW
    glDeleteProgram(shaderProgram);
    glfwTerminate();

    return 0;
}
