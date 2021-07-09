```
<Scalar> wrap { repeat-definition }
<Scalar> wrapu { repeat-definition }
<Scalar> wrapv { repeat-definition }
<Scalar> wrapw { repeat-definition }

This defines the behavior of the texture image outside of the
normal (u,v) range 0.0 - 1.0.  It is "REPEAT" to repeat the
texture to infinity, "CLAMP" not to.  The wrapping behavior may be
specified independently for each axis via "wrapu" and "wrapv", or
it may be specified for both simultaneously via "wrap".

Although less often used, for 3-d textures wrapw may also be
specified, and it behaves similarly to wrapu and wrapv.

There are other legal values in addtional to REPEAT and CLAMP.
The full list is:

  CLAMP
  REPEAT
  MIRROR
  MIRROR_ONCE
  BORDER_COLOR
```

https://docs.panda3d.org/1.10/python/programming/texturing/texture-wrap-modes
