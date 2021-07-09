```
<Scalar> compression { compression-mode }

Defines an explicit control over the real-time compression mode
applied to the texture.  The various options are:

  DEFAULT OFF ON
  FXT1 DXT1 DXT2 DXT3 DXT4 DXT5

This controls the compression of the texture when it is loaded
into graphics memory, and has nothing to do with on-disk
compression such as JPEG.  If this option is omitted or "DEFAULT",
then the texture compression is controlled by the
compressed-textures config variable.  If it is "OFF", texture
compression is explicitly off for this texture regardless of the
setting of the config variable; if it is "ON", texture compression
is explicitly on, and a default compression algorithm supported by
the driver is selected.  If any of the other options, it names the
specific compression algorithm to be used.
```