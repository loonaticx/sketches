```
<Scalar> format { format-definition }

    This defines the load format of the image file.  The
    format-definition is one of:

      RGBA, RGBM, RGBA12, RGBA8, RGBA4,
      RGB, RGB12, RGB8, RGB5, RGB332,
      LUMINANCE_ALPHA,
      RED, GREEN, BLUE, ALPHA, LUMINANCE

    The formats whose names end in digits specifically request a
    particular texel width.  RGB12 and RGBA12 specify 48-bit texels
    with or without alpha; RGB8 and RGBA8 specify 32-bit texels, and
    RGB5 and RGBA4 specify 16-bit texels.  RGB332 specifies 8-bit
    texels.

    The remaining formats are generic and specify only the semantic
    meaning of the channels.  The size of the texels is determined by
    the width of the components in the image file.  RGBA is the most
    general; RGB is the same, but without any alpha channel.  RGBM is
    like RGBA, except that it requests only one bit of alpha, if the
    graphics card can provide that, to leave more room for the RGB
    components, which is especially important for older 16-bit
    graphics cards (the "M" stands for "mask", as in a cutout).

    The number of components of the image file should match the format
    specified; if it does not, the egg loader will attempt to provide
    the closest match that does.
```