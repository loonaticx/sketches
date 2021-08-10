#version 330

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec4 texcoord;

out vec2 l_coordTap0;
out vec2 l_coordTap1;
out vec2 l_coordTap2;
out vec2 l_coordTap3;

uniform vec2 tapOffsets[4];

void main()
{
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    
    l_coordTap0 = texcoord.xy + tapOffsets[0];
    l_coordTap1 = texcoord.xy + tapOffsets[1];
    l_coordTap2 = texcoord.xy + tapOffsets[2];
    l_coordTap3 = texcoord.xy + tapOffsets[3];
}
