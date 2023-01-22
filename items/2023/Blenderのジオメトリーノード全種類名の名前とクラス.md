title: Blenderのジオメトリーノード全種類名の名前とクラス
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/1bf451085f55bde21224
created_at: 2023-01-22 20:29:04+09:00
updated_at: 2023-01-22 23:40:35+09:00
body:

## ジオメトリーノード全種類の名前とクラス

ジオメトリーノードの名前からそのクラスを知りたかったので、全種類のデフォルトの名前とそのクラスの一覧を作成しました。

## 作成方法

ノードのクラスはシェーダーやコンポジットなどでも使われていますが、全て`bpy.types.Node`の派生クラスです。
そこで、`bpy.types.Node`の全派生クラスを実際にジオメトリーノードに作成して成功したものを抽出しました。

後で辞書として使いたいので、JSONで書き出しています。短い名前のときに、前から検索して別のノードと間違えないように逆順にしています。

```python:make_all_nodes.py
import bpy

bpy.ops.mesh.primitive_plane_add()  # dummy object
mds = bpy.context.object.modifiers.new("GeometryNodes", "NODES")
mds.node_group = node_group = bpy.data.node_groups.new("Geometry Nodes", "GeometryNodeTree")
node_group.inputs.new("NodeSocketGeometry", "Geometry")
node_group.outputs.new("NodeSocketGeometry", "Geometry")
clss = []
for name in dir(bpy.types):
    cls = getattr(bpy.types, name)
    if isinstance(cls, type) and issubclass(cls, bpy.types.Node):
        try:
            node_group.nodes.new(cls.bl_rna.identifier)
            clss.append((cls.bl_rna.name, cls.bl_rna.identifier))
        except RuntimeError:
            pass
with open("all_geometry_node.json", "w") as fp:
    fp.write("{")
    for i, (name, idname) in enumerate(sorted(clss, reverse=True)):
        fp.write(f'{"," * (i > 0)}\n    "{name}": "{idname}"')
    fp.write("\n}\n")
```

上記を`make_all_nodes.py`としたときに、下記のように実行します。

```bash:bash
blender -b -P make_all_nodes.py
```

`blender`コマンドについては、「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」を参考にしてください。

## 結果

194クラスありました。

```json:all_geometry_node.json
{
    "White Noise Texture": "ShaderNodeTexWhiteNoise",
    "Wave Texture": "ShaderNodeTexWave",
    "Voronoi Texture": "ShaderNodeTexVoronoi",
    "Volume to Mesh": "GeometryNodeVolumeToMesh",
    "Volume Cube": "GeometryNodeVolumeCube",
    "Viewer": "GeometryNodeViewer",
    "Vertex of Corner": "GeometryNodeVertexOfCorner",
    "Vertex Neighbors": "GeometryNodeInputMeshVertexNeighbors",
    "Vector Rotate": "ShaderNodeVectorRotate",
    "Vector Math": "ShaderNodeVectorMath",
    "Vector Curves": "ShaderNodeVectorCurve",
    "Vector": "FunctionNodeInputVector",
    "Value to String": "FunctionNodeValueToString",
    "Value": "ShaderNodeValue",
    "UV Unwrap": "GeometryNodeUVUnwrap",
    "UV Sphere": "GeometryNodeMeshUVSphere",
    "Trim Curve": "GeometryNodeTrimCurve",
    "Triangulate": "GeometryNodeTriangulate",
    "Translate Instances": "GeometryNodeTranslateInstances",
    "Transform": "GeometryNodeTransform",
    "Switch": "GeometryNodeSwitch",
    "Subdivision Surface": "GeometryNodeSubdivisionSurface",
    "Subdivide Mesh": "GeometryNodeSubdivideMesh",
    "Subdivide Curve": "GeometryNodeSubdivideCurve",
    "String to Curves": "GeometryNodeStringToCurves",
    "String Length": "FunctionNodeStringLength",
    "String": "FunctionNodeInputString",
    "Store Named Attribute": "GeometryNodeStoreNamedAttribute",
    "Star": "GeometryNodeCurveStar",
    "Split Edges": "GeometryNodeSplitEdges",
    "Spline Resolution": "GeometryNodeInputSplineResolution",
    "Spline Parameter": "GeometryNodeSplineParameter",
    "Spline Length": "GeometryNodeSplineLength",
    "Special Characters": "FunctionNodeInputSpecialCharacters",
    "Slice String": "FunctionNodeSliceString",
    "Shortest Edge Paths": "GeometryNodeInputShortestEdgePaths",
    "Set Spline Type": "GeometryNodeCurveSplineType",
    "Set Spline Resolution": "GeometryNodeSetSplineResolution",
    "Set Spline Cyclic": "GeometryNodeSetSplineCyclic",
    "Set Shade Smooth": "GeometryNodeSetShadeSmooth",
    "Set Position": "GeometryNodeSetPosition",
    "Set Point Radius": "GeometryNodeSetPointRadius",
    "Set Material Index": "GeometryNodeSetMaterialIndex",
    "Set Material": "GeometryNodeSetMaterial",
    "Set ID": "GeometryNodeSetID",
    "Set Handle Type": "GeometryNodeCurveSetHandles",
    "Set Handle Positions": "GeometryNodeSetCurveHandlePositions",
    "Set Curve Tilt": "GeometryNodeSetCurveTilt",
    "Set Curve Radius": "GeometryNodeSetCurveRadius",
    "Set Curve Normal": "GeometryNodeSetCurveNormal",
    "Separate XYZ": "ShaderNodeSeparateXYZ",
    "Separate RGB": "ShaderNodeSeparateRGB",
    "Separate Geometry": "GeometryNodeSeparateGeometry",
    "Separate Components": "GeometryNodeSeparateComponents",
    "Separate Color": "FunctionNodeSeparateColor",
    "Self Object": "GeometryNodeSelfObject",
    "Scene Time": "GeometryNodeInputSceneTime",
    "Scale Instances": "GeometryNodeScaleInstances",
    "Scale Elements": "GeometryNodeScaleElements",
    "Sample UV Surface": "GeometryNodeSampleUVSurface",
    "Sample Nearest Surface": "GeometryNodeSampleNearestSurface",
    "Sample Nearest": "GeometryNodeSampleNearest",
    "Sample Index": "GeometryNodeSampleIndex",
    "Sample Curve": "GeometryNodeSampleCurve",
    "Rotate Instances": "GeometryNodeRotateInstances",
    "Rotate Euler": "FunctionNodeRotateEuler",
    "Reverse Curve": "GeometryNodeReverseCurve",
    "Resample Curve": "GeometryNodeResampleCurve",
    "Reroute": "NodeReroute",
    "Replace String": "FunctionNodeReplaceString",
    "Replace Material": "GeometryNodeReplaceMaterial",
    "Remove Named Attribute": "GeometryNodeRemoveAttribute",
    "Realize Instances": "GeometryNodeRealizeInstances",
    "Raycast": "GeometryNodeRaycast",
    "Random Value": "FunctionNodeRandomValue",
    "Radius": "GeometryNodeInputRadius",
    "RGB Curves": "ShaderNodeRGBCurve",
    "Quadrilateral": "GeometryNodeCurvePrimitiveQuadrilateral",
    "Quadratic Bezier": "GeometryNodeCurveQuadraticBezier",
    "Position": "GeometryNodeInputPosition",
    "Points to Volume": "GeometryNodePointsToVolume",
    "Points to Vertices": "GeometryNodePointsToVertices",
    "Points of Curve": "GeometryNodePointsOfCurve",
    "Points": "GeometryNodePoints",
    "Pack UV Islands": "GeometryNodeUVPackIslands",
    "Offset Point in Curve": "GeometryNodeOffsetPointInCurve",
    "Offset Corner in Face": "GeometryNodeOffsetCornerInFace",
    "Object Info": "GeometryNodeObjectInfo",
    "Normal": "GeometryNodeInputNormal",
    "Noise Texture": "ShaderNodeTexNoise",
    "Named Attribute": "GeometryNodeInputNamedAttribute",
    "Musgrave Texture": "ShaderNodeTexMusgrave",
    "MixRGB": "ShaderNodeMixRGB",
    "Mix": "ShaderNodeMix",
    "Mesh to Volume": "GeometryNodeMeshToVolume",
    "Mesh to Points": "GeometryNodeMeshToPoints",
    "Mesh to Curve": "GeometryNodeMeshToCurve",
    "Mesh Line": "GeometryNodeMeshLine",
    "Mesh Island": "GeometryNodeInputMeshIsland",
    "Mesh Circle": "GeometryNodeMeshCircle",
    "Mesh Boolean": "GeometryNodeMeshBoolean",
    "Merge by Distance": "GeometryNodeMergeByDistance",
    "Math": "ShaderNodeMath",
    "Material Selection": "GeometryNodeMaterialSelection",
    "Material Index": "GeometryNodeInputMaterialIndex",
    "Material": "GeometryNodeInputMaterial",
    "Map Range": "ShaderNodeMapRange",
    "Magic Texture": "ShaderNodeTexMagic",
    "Join Strings": "GeometryNodeStringJoin",
    "Join Geometry": "GeometryNodeJoinGeometry",
    "Is Viewport": "GeometryNodeIsViewport",
    "Is Spline Cyclic": "GeometryNodeInputSplineCyclic",
    "Is Shade Smooth": "GeometryNodeInputShadeSmooth",
    "Is Face Planar": "GeometryNodeInputMeshFaceIsPlanar",
    "Interpolate Domain": "GeometryNodeFieldOnDomain",
    "Integer": "FunctionNodeInputInt",
    "Instances to Points": "GeometryNodeInstancesToPoints",
    "Instance on Points": "GeometryNodeInstanceOnPoints",
    "Instance Scale": "GeometryNodeInputInstanceScale",
    "Instance Rotation": "GeometryNodeInputInstanceRotation",
    "Index": "GeometryNodeInputIndex",
    "Image Texture": "GeometryNodeImageTexture",
    "Ico Sphere": "GeometryNodeMeshIcoSphere",
    "ID": "GeometryNodeInputID",
    "Handle Type Selection": "GeometryNodeCurveHandleTypeSelection",
    "Group Output": "NodeGroupOutput",
    "Group Input": "NodeGroupInput",
    "Group": "GeometryNodeGroup",
    "Grid": "GeometryNodeMeshGrid",
    "Gradient Texture": "ShaderNodeTexGradient",
    "Geometry to Instance": "GeometryNodeGeometryToInstance",
    "Geometry Proximity": "GeometryNodeProximity",
    "Frame": "NodeFrame",
    "Float to Integer": "FunctionNodeFloatToInt",
    "Float Curve": "ShaderNodeFloatCurve",
    "Flip Faces": "GeometryNodeFlipFaces",
    "Fillet Curve": "GeometryNodeFilletCurve",
    "Fill Curve": "GeometryNodeFillCurve",
    "Field at Index": "GeometryNodeFieldAtIndex",
    "Face of Corner": "GeometryNodeFaceOfCorner",
    "Face Set Boundaries": "GeometryNodeMeshFaceSetBoundaries",
    "Face Neighbors": "GeometryNodeInputMeshFaceNeighbors",
    "Face Area": "GeometryNodeInputMeshFaceArea",
    "Extrude Mesh": "GeometryNodeExtrudeMesh",
    "Endpoint Selection": "GeometryNodeCurveEndpointSelection",
    "Edges of Vertex": "GeometryNodeEdgesOfVertex",
    "Edges of Corner": "GeometryNodeEdgesOfCorner",
    "Edge Vertices": "GeometryNodeInputMeshEdgeVertices",
    "Edge Paths to Selection": "GeometryNodeEdgePathsToSelection",
    "Edge Paths to Curves": "GeometryNodeEdgePathsToCurves",
    "Edge Neighbors": "GeometryNodeInputMeshEdgeNeighbors",
    "Edge Angle": "GeometryNodeInputMeshEdgeAngle",
    "Duplicate Elements": "GeometryNodeDuplicateElements",
    "Dual Mesh": "GeometryNodeDualMesh",
    "Domain Size": "GeometryNodeAttributeDomainSize",
    "Distribute Points on Faces": "GeometryNodeDistributePointsOnFaces",
    "Distribute Points in Volume": "GeometryNodeDistributePointsInVolume",
    "Delete Geometry": "GeometryNodeDeleteGeometry",
    "Deform Curves on Surface": "GeometryNodeDeformCurvesOnSurface",
    "Cylinder": "GeometryNodeMeshCylinder",
    "Curve to Points": "GeometryNodeCurveToPoints",
    "Curve to Mesh": "GeometryNodeCurveToMesh",
    "Curve of Point": "GeometryNodeCurveOfPoint",
    "Curve Tilt": "GeometryNodeInputCurveTilt",
    "Curve Tangent": "GeometryNodeInputTangent",
    "Curve Spiral": "GeometryNodeCurveSpiral",
    "Curve Line": "GeometryNodeCurvePrimitiveLine",
    "Curve Length": "GeometryNodeCurveLength",
    "Curve Handle Positions": "GeometryNodeInputCurveHandlePositions",
    "Curve Circle": "GeometryNodeCurvePrimitiveCircle",
    "Cube": "GeometryNodeMeshCube",
    "Corners of Vertex": "GeometryNodeCornersOfVertex",
    "Corners of Face": "GeometryNodeCornersOfFace",
    "Convex Hull": "GeometryNodeConvexHull",
    "Cone": "GeometryNodeMeshCone",
    "Compare": "FunctionNodeCompare",
    "Combine XYZ": "ShaderNodeCombineXYZ",
    "Combine RGB": "ShaderNodeCombineRGB",
    "Combine Color": "FunctionNodeCombineColor",
    "ColorRamp": "ShaderNodeValToRGB",
    "Color": "FunctionNodeInputColor",
    "Collection Info": "GeometryNodeCollectionInfo",
    "Clamp": "ShaderNodeClamp",
    "Checker Texture": "ShaderNodeTexChecker",
    "Capture Attribute": "GeometryNodeCaptureAttribute",
    "Brick Texture": "ShaderNodeTexBrick",
    "Bounding Box": "GeometryNodeBoundBox",
    "Boolean Math": "FunctionNodeBooleanMath",
    "Boolean": "FunctionNodeInputBool",
    "Bezier Segment": "GeometryNodeCurvePrimitiveBezierSegment",
    "Attribute Statistic": "GeometryNodeAttributeStatistic",
    "Arc": "GeometryNodeCurveArc",
    "Align Euler to Vector": "FunctionNodeAlignEulerToVector",
    "Accumulate Field": "GeometryNodeAccumulateField"
}
```

以上

