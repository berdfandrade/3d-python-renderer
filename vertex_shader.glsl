// Vertex Shader
#version 330 core

layout (location = 0) in vec3 in_position;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec4 fragColor;

void main()
{
    // Transformação dos vértices
    gl_Position = projection * view * model * vec4(in_position, 1.0);
    fragColor = vec4(1.0, 0.5, 0.2, 1.0);  // Cor fixa para cada vértice
}