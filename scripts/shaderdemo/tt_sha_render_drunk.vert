// Render drunk vert
// drewcification 010721
#version 130

in vec4 p3d_Vertex;
in vec4 p3d_Color;
in vec2 p3d_MultiTexCoord0;
uniform mat4 p3d_ModelViewProjectionMatrix;

uniform float osg_FrameTime;

out vec4 vColor;
out vec2 texcoord;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;

  // Wobble the screen
  gl_Position.x += osg_FrameTime * gl_Position.x/10;
  gl_Position.y += osg_FrameTime * gl_Position.y/10;
  //gl_Position.z += tan(osg_FrameTime) * gl_Position.z/10;

  vColor = p3d_Color;
  texcoord = p3d_MultiTexCoord0;
}
