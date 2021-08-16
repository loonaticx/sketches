//GLSL
#version 130
uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
out vec4 uv;

void main()
    {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex; 
    uv = gl_Position*0.5+0.5;    
    }
