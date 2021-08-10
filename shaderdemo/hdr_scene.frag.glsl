#version 330

in vec2 texcoord;
uniform sampler2D p3d_Texture0;

out vec4 color;

void main()
{
	color = texture(p3d_Texture0, texcoord);
}
