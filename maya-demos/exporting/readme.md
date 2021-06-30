# Export Process
Questions:
- What attributes are lost when our model is converted to an egg file?

Results:
- When converting maya2egg, all vertices have become detatched which generates more UV shells

## blue.mb
Default, all coincident (shared edges) verts are merged.
25 Verts
50 Edges
25 Faces
50 Tris
52 UVs
All faces are quads

## blue.egg
3 total nodes (including 0 instances); 0 LODNodes.
0 transforms; 0% of nodes have some render attribute.
1 Geoms, with 1 GeomVertexDatas and 1 GeomVertexFormats, appear on 1 GeomNodes.
100 vertices, 100 normals, 0 colors, 100 texture coordinates.
GeomVertexData arrays occupy 5.57 KiB memory.
GeomPrimitive arrays occupy 0.289 KiB memory.
50 triangles:
  50 of these are on 25 tristrips (2 average tris per strip).
  0 of these are independent triangles.
0 textures, estimated minimum 0 KiB texture memory required.

## Importing blue.egg into Maya
100 Verts
125 Edges
50 Faces
50 Tris
124 UVs
Some faces that were originally quads converted into tris (thus 2 faces now) have been split to their own unique UV shell. However, there are some tri faces that aren't on the same shell as its neighbor tri face.

## red.mb
All coincident verts are separated and all faces/edges are detatched.
100 Verts
100 Edges
25 Faces
50 Tris
100 UVs
All faces are quads

## red.egg
3 total nodes (including 0 instances); 0 LODNodes.
0 transforms; 0% of nodes have some render attribute.
1 Geoms, with 1 GeomVertexDatas and 1 GeomVertexFormats, appear on 1 GeomNodes.
100 vertices, 100 normals, 0 colors, 100 texture coordinates.
GeomVertexData arrays occupy 5.57 KiB memory.
GeomPrimitive arrays occupy 0.289 KiB memory.
50 triangles:
  50 of these are on 25 tristrips (2 average tris per strip).
  0 of these are independent triangles.
0 textures, estimated minimum 0 KiB texture memory required.