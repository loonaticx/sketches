/*
  (C) 2021 David Lettier
  lettier.com
*/

#version 150
uniform vec4 p3d_TexAlphaOnly;
uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
uniform vec2 enabled;
//uniform vec2 render2d;
in vec4 vColor;
out vec4 fragColor;

void main() {
  float redOffset   =  0.009;
  float greenOffset =  0.006;
  float blueOffset  = -0.006;

  vec2 texSize  = textureSize(p3d_Texture0, 0).xy;
  vec2 texCoord = gl_FragCoord.xy / texSize;

  vec2 direction = texCoord;

  vec4 texColor = texture(p3d_Texture0, texCoord) + p3d_TexAlphaOnly;
  fragColor = p3d_ColorScale * texColor * vColor;
  fragColor = vec4(fragColor.rgba);

  if (enabled.x != 1) { return; }

/*
  if (render2d.x == 1) {
    	if (fragColor.a < 0.1) {
        discard;
    }
  }
*/

  fragColor.r = texture(p3d_Texture0, texCoord + (direction * vec2(redOffset  ))).r;
  fragColor.g = texture(p3d_Texture0, texCoord + (direction * vec2(greenOffset))).g;
  fragColor.b = texture(p3d_Texture0, texCoord + (direction * vec2(blueOffset ))).b;
  //fragColor.a = texture(p3d_Texture0, texCoord).a;

}