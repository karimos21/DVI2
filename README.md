# DVI2

### Vertex Clustering

    Purpose: 
        Reduces the number of vertices in a mesh by clustering them into a specified number of clusters.
    Method:
        Clustering: Uses KMeans clustering to group the vertices into target_count clusters.
        New Vertices: The cluster centers become the new vertices of the mesh.
        Vertex Mapping: Maps old vertices to their respective cluster centers.
        New Faces: Reconstructs faces using the new vertex indices.

### Edge Collapse

    Purpose: 
        Reduces the number of vertices in a mesh by iteratively collapsing the edges.
    Method:
        Priority Queue: Uses a priority queue to keep edges sorted by their collapse cost.
        Edge Collapse: Iteratively collapses edges with the lowest cost until the number of vertices is reduced to target_count.
        Vertex Mapping: Updates vertex positions and maps collapsed vertices to their new positions.
        New Faces: Re-indexes faces to use the new vertex indices and removes degenerate faces (faces with fewer than 3 vertices).
