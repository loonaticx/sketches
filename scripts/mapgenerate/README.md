
# Sphere Maps
todo: write how this works

        # First, make an offscreen buffer to convert the cube map to a
        # sphere map.  We make it first so we can guarantee the
        # rendering order for the cube map.
        toSphere = source.makeTextureBuffer(namePrefix, size, size,
                                            Texture(), 1)
# Cube Maps
