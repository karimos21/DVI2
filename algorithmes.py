import numpy as np
import heapq
from sklearn.cluster import KMeans

def load_obj(filepath):
    vertices = []
    faces = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip().split()
                if line:
                    if line[0] == 'v':
                        try:
                            vertices.append(np.array([float(x) for x in line[1:]]))
                        except ValueError:
                            print(f"Warning: Skipping invalid vertex line: {line}")  
                    elif line[0] == 'f':
                        try:
                           face = [int(x.split('/')[0]) - 1 for x in line[1:]]
                           faces.append(face)
                        except (ValueError, IndexError):
                           print(f"Warning: Skipping invalid face line: {line}") 
        return np.array(vertices), np.array(faces)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None, None

class Mesh:
    def __init__(self, vertices, faces): 
        self.vertices = vertices
        self.faces = faces

    def decimate(self, method, target_count):  
        
        if method == "vertex_clustering":
            return self._vertex_clustering(target_count)
        elif method == "edge_collapse":
            return self._edge_collapse(target_count)
        else:
            raise ValueError(f"Invalid decimation method: {method}")


    def _vertex_clustering(self, target_count):
        if target_count is None or target_count <= 0 or target_count >= len(self.vertices) :
           raise ValueError("Invalid target_count for vertex clustering")

        kmeans = KMeans(n_clusters=target_count, random_state=0).fit(self.vertices)
        new_vertices = kmeans.cluster_centers_

        # Map old vertices to new vertices
        vertex_map = {i: kmeans.labels_[i] for i in range(len(self.vertices))}

        new_faces = []
        for face in self.faces:
           new_face = [vertex_map[vertex_index] for vertex_index in face]
           new_faces.append(new_face)


        return Mesh(new_vertices, np.array(new_faces))

    def save_obj(self, filepath):
        """Saves the mesh to an OBJ file."""
        try:
            with open(filepath, 'w') as f:
                for vertex in self.vertices:
                    f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
                for face in self.faces:  # Corrected face saving
                    f.write(f"f {' '.join(map(str, face + 1))}\n")  # +1 to convert back to 1-based indexing for OBJ

        except Exception as e:
            print(f"Error saving OBJ file: {e}")



    def _edge_collapse(self, target_count):

      print(f"Original number of vertices: {len(self.vertices)}")  # Print original vertex count
      
      priority_queue = []
      for edge in edges:  
          cost = calculate_collapse_cost(edge, self.vertices, self.faces) 
          heapq.heappush(priority_queue, (cost, edge))

      collapsed_vertices = set()
      vertex_map = {i: i for i in range(len(self.vertices))}


      for _ in range(len(self.vertices) - target_count): 
        if priority_queue:
            cost, (v1, v2) = heapq.heappop(priority_queue)

            if v1 not in collapsed_vertices and v2 not in collapsed_vertices:
                new_vertex = (self.vertices[v1] + self.vertices[v2]) / 2 


                self.vertices[v1] = new_vertex
                collapsed_vertices.add(v2)
                vertex_map[v2] = v1
        else:
            break  



      # ... (Face re-indexing and creation of new mesh).
      new_vertices = self.vertices[list(set(range(len(self.vertices))) - collapsed_vertices)]

      new_faces = []
      for face in self.faces:
          new_face = []

          for v in face:
              new_v = vertex_map[v]

              if new_v not in new_face: 
                new_face.append(new_v)
          if len(new_face) >= 3:  
            new_faces.append(new_face)

      return Mesh(new_vertices, np.array(new_faces))





# Example usage:
vertices, faces = load_obj("obj1.obj")


if vertices is not None and faces is not None:

    print(f"Original vertices:\n{vertices}")  

    try:
        reduced_mesh_edge = mesh.decimate(method="edge_collapse", target_count=500)
        if reduced_mesh_edge:
            reduced_mesh_edge.save_obj("reduced_mesh.obj") # Save reduced mesh
            print(f"Reduced mesh saved to reduced_mesh.obj")


    except ValueError as e:
      print(f"Error during edge collapse: {e}")