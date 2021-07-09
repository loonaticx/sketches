# Nodepath Flattening

## Why should we flatten nodes?
- Remove redundant geometry

# Case Study
---

## INPUT EGG
- Filesize is 7,785 KB

```
966 total nodes (including 0 instances); 0 LODNodes.
4 transforms; 0% of nodes have some render attribute.
946 Geoms, with 833 GeomVertexDatas and 4 GeomVertexFormats, appear on 806 GeomNodes.
15188 vertices, 15188 normals, 12742 colors, 15188 texture coordinates.
0 normals are too long, 2 are too short.  Average normal length is 0.999868
GeomVertexData arrays occupy 892 KiB memory.
GeomPrimitive arrays occupy 40.4 KiB memory.
1363 GeomVertexArrayDatas are redundant, wasting 85K.
533 GeomPrimitive arrays are redundant, wasting 31K.
8507 triangles:
  7496 of these are on 3327 tristrips (2.25308 average tris per strip).
  1011 of these are independent triangles.
39 textures, estimated minimum 75.1 MiB texture memory required.
```

## NORMAL BAM
- Filesize is 1,177 KB

```
966 total nodes (including 0 instances); 0 LODNodes.
4 transforms; 0% of nodes have some render attribute.
946 Geoms, with 833 GeomVertexDatas and 4 GeomVertexFormats, appear on 806 GeomNodes.
15188 vertices, 15188 normals, 12742 colors, 15188 texture coordinates.
0 normals are too long, 2 are too short.  Average normal length is 0.999868
GeomVertexData arrays occupy 892 KiB memory.
GeomPrimitive arrays occupy 40.4 KiB memory.
1363 GeomVertexArrayDatas are redundant, wasting 85K.
533 GeomPrimitive arrays are redundant, wasting 31K.
8507 triangles:
  7496 of these are on 3327 tristrips (2.25308 average tris per strip).
  1011 of these are independent triangles.
39 textures, estimated minimum 75.1 MiB texture memory required.
```

## LIGHT
- Filesize is 1,176 KB

```
966 total nodes (including 0 instances); 0 LODNodes.
1 transforms; 0% of nodes have some render attribute.
946 Geoms, with 833 GeomVertexDatas and 4 GeomVertexFormats, appear on 806 GeomNodes.
15188 vertices, 15188 normals, 12742 colors, 15188 texture coordinates.
0 normals are too long, 2 are too short.  Average normal length is 0.999868
GeomVertexData arrays occupy 892 KiB memory.
GeomPrimitive arrays occupy 40.4 KiB memory.
1363 GeomVertexArrayDatas are redundant, wasting 85K.
533 GeomPrimitive arrays are redundant, wasting 31K.
8507 triangles:
  7496 of these are on 3327 tristrips (2.25308 average tris per strip).
  1011 of these are independent triangles.
39 textures, estimated minimum 75.1 MiB texture memory required.
```
## MEDIUM
- Filesize is 1,176 KB
- NO CHANGE

```
966 total nodes (including 0 instances); 0 LODNodes.
1 transforms; 0% of nodes have some render attribute.
946 Geoms, with 833 GeomVertexDatas and 4 GeomVertexFormats, appear on 806 GeomNodes.
15188 vertices, 15188 normals, 12742 colors, 15188 texture coordinates.
0 normals are too long, 2 are too short.  Average normal length is 0.999868
GeomVertexData arrays occupy 892 KiB memory.
GeomPrimitive arrays occupy 40.4 KiB memory.
1363 GeomVertexArrayDatas are redundant, wasting 85K.
533 GeomPrimitive arrays are redundant, wasting 31K.
8507 triangles:
  7496 of these are on 3327 tristrips (2.25308 average tris per strip).
  1011 of these are independent triangles.
39 textures, estimated minimum 75.1 MiB texture memory required.
```

## STRONG
- Filesize is 1,066 KB

```
61 total nodes (including 0 instances); 0 LODNodes.
1 transforms; 0% of nodes have some render attribute.
63 Geoms, with 12 GeomVertexDatas and 4 GeomVertexFormats, appear on 11 GeomNodes.
29264 vertices, 29264 normals, 29152 colors, 29264 texture coordinates.
0 normals are too long, 4 are too short.  Average normal length is 0.999863
GeomVertexData arrays occupy 1.72e+03 KiB memory.
GeomPrimitive arrays occupy 48.4 KiB memory.
14076 vertices are unreferenced by any GeomPrimitives.
6 GeomVertexArrayDatas are redundant, wasting 322K.
2 GeomPrimitive arrays are redundant, wasting 1K.
8507 triangles:
  4706 of these are on 2193 tristrips (2.14592 average tris per strip).
  3801 of these are independent triangles.
39 textures, estimated minimum 75.1 MiB texture memory required.
```