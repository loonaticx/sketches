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

All of the child nodes within a seq-defined group node will take turns being displayed.

*Also refer to egg-seq-2d for another example.*