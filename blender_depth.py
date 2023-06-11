import bpy
import cv2
import numpy as np

def get_depth():
    """Obtains depth map from Blender render.
    :return: The depth map of the rendered camera view as a numpy array of size (H,W).
    """
    z = bpy.data.images['Viewer Node']
    w, h = z.size
    dmap = np.array(z.pixels[:], dtype=np.float32) # convert to numpy array
    dmap = np.reshape(dmap, (h, w, 4))[:,:,0]
    dmap = np.rot90(dmap, k=2)
    dmap = np.fliplr(dmap)
    return dmap

def dmap2norm(dmap):
    """Computes surface normals from a depth map.
    :param dmap: A grayscale depth map image as a numpy array of size (H,W).
    :return: The corresponding surface normals map as numpy array of size (H,W,3).
    """
    zx = cv2.Sobel(dmap, cv2.CV_64F, 1, 0, ksize=5)
    zy = cv2.Sobel(dmap, cv2.CV_64F, 0, 1, ksize=5)

    # convert to unit vectors
    normals = np.dstack((-zx, -zy, np.ones_like(dmap)))
    length = np.linalg.norm(normals, axis=2)
    normals[:, :, :] /= length

    # offset and rescale values to be in 0-1
    normals += 1
    normals /= 2
    return normals[:, :, ::-1].astype(np.float32)

bpy.context.scene.render.filepath = "rgb.png"
bpy.ops.render.render(False, animation=False, write_still=True)
dmap = get_depth()
nmap = dmap2norm(dmap)
np.savez_compressed("d.npz", dmap=dmap, nmap=nmap)
