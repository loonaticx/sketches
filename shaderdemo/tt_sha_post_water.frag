// Postprocess water overlay | Fragment
// drewcification 022221
#version 130

// These 3 are required by the filter manager to be present
uniform sampler2D color_texture;
uniform sampler2D depth_texture;
uniform sampler2D p3d_Texture0;


uniform float osg_FrameTime;

in vec2 texcoord;
out vec4 color;

void main() {

    //gl_FragColor = color.bgra;

	vec2 wc = texcoord;

	wc.x = ( 0.33 * wc.x) + 0.5;
	wc.y = (-0.33 * wc.y) + 0.5;

	vec2 newcoord = texcoord;
	//newcoord.x = clamp(newcoord.x + sin(60 * wc.y + 60 * wc.x + osg_FrameTime * 2) / 60, 0, 1);
	newcoord.y = clamp(newcoord.y + sin(60 * wc.y + 60 * wc.x + osg_FrameTime * 2) / 60, 0, 1);

	// vignette
	vec2 uv = gl_FragCoord.xy;
	uv *= 1.0 - uv.yx;
	float vignette = pow(uv.x*uv.y * 15.0, 0.5);

	// This lessens the wave effect as it reaches the edge of the screen
	// mainly used to hide where the scene would wrap
	newcoord = mix(texcoord.xy, newcoord.xy, vignette);

	color = texture(p3d_Texture0, newcoord);

	// Uncomment this for just a black border
	//color.rgb *= vignette;

	// Dark Blue border
	color.rgb = mix(vec3(0.0, 0.0, 0.2), color.rgb, vignette);

	// Tint the screen blue
	color.rg /= 3;

}
