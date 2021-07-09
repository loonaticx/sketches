```
#   This attribute indicates that the child nodes of this group
#   represent a series of animation frames that should be
#   consecutively displayed.  In the absence of an "fps" scalar for
#   the group (see below), the egg loader creates a SwitchNode, and it
#   the responsibility of the show code to perform the switching.  If
#   an fps scalar is defined and is nonzero, the egg loader creates a
#   SequenceNode instead, which automatically cycles through its
#   children.
egg-object-type-switch          <Switch> { 1 }

egg-object-type-seq2            <Switch> { 1 } <Scalar>  fps { 2 }
egg-object-type-seq4            <Switch> { 1 } <Scalar>  fps { 4 }
egg-object-type-seq6            <Switch> { 1 } <Scalar>  fps { 6 }
egg-object-type-seq8            <Switch> { 1 } <Scalar> fps { 8 }
egg-object-type-seq10           <Switch> { 1 } <Scalar> fps { 10 }
egg-object-type-seq12           <Switch> { 1 } <Scalar> fps { 12 }
egg-object-type-seq24           <Switch> { 1 } <Scalar> fps { 24 }

```

----------------------------

# SAMPLE EGG FILE

```
<Texture> 1 {
  texture.png
  ...
}

<Texture> 2 {
  texture-dim.png
  ...
}

<Group> seqPlane {
  <Switch> { 1 }
  <Scalar> fps { 1 }
  <Group> plane1 {
    <VertexPool> planeShape1.verts { ... }
    <Polygon> {
      <Normal> { 0 0 1 }
      <TRef> { 1 }
      <VertexRef> { 0 2 3 1 <Ref> { planeShape1.verts } }
    }
  }
  <Group> plane2 {
    <VertexPool> planeShape2.verts { ... }
    <Polygon> {
      <Normal> { 0 0 1 }
      <TRef> { 2 }
      <VertexRef> { 0 2 3 1 <Ref> { planeShape2.verts } }
    }
  }
}
```

Two identical meshes in the same exact location, both with different TRefs. They should swap with one another one time per second.

*Also refer to egg-seq-3d for another example.*
