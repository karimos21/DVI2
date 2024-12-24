import numpy as np

def decode_obj(filepath):
    vertices = []
    normals = []
    texcoords = []
    faces = []

    dtype = [('vertices', 'i4', (3,)), ('texcoords', 'i4', (3,)), ('normals', 'i4', (3,))]

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('v '):
                vertices.append(np.array(line.split()[1:], dtype=float))
            elif line.startswith('vn '):
                normals.append(np.array(line.split()[1:], dtype=float))
            elif line.startswith('vt '):
                texcoords.append(np.array(line.split()[1:], dtype=float))
            elif line.startswith('f '):
                face_data = []
                for item in line.split()[1:]:
                    indices = item.split('/')
                    v_idx = int(indices[0]) - 1
                    vt_idx = int(indices[1]) - 1 if len(indices) > 1 and indices[1] else -1
                    vn_idx = int(indices[2]) - 1 if len(indices) > 2 and indices[2] else -1
                    face_data.append((v_idx, vt_idx, vn_idx))
                faces.append(np.array(face_data, dtype=dtype))

    return np.array(vertices), np.array(normals), np.array(texcoords), np.array(faces)

vertices, normals, texcoords, faces = decode_obj("obj1.obj")

# Accéder aux données:
print(vertices[0]) # Premier sommet
print(faces[0]['vertices']) # Indices des sommets de la première face