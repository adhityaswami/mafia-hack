
import xml.etree.ElementTree as ET
from svg.path import parse_path
import numpy as np
from PIL import Image
import cv2


def parse_svg_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root


def rectangle_to_pixels(element):
    x, y, width, height = float(element.get('x', 0)), float(element.get('y', 0)), float(element.get('width')), float(element.get('height'))
    xs = np.arange(x, x + width, 1)
    ys = np.arange(y, y + height, 1)
    return [(x, y) for x in xs for y in ys]


def line_to_pixels(element):
    x1, y1, x2, y2 = float(element.get('x1')), float(element.get('y1')), float(element.get('x2')), float(element.get('y2'))
    length = int(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    xs = np.linspace(x1, x2, length)
    ys = np.linspace(y1, y2, length)
    return list(zip(xs, ys))


def polygon_to_pixels(element):
    points = [tuple(map(float, point.split(','))) for point in element.get('points').strip().split()]
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return list(zip(xs, ys))


def component_to_pixels(element, resolution):
    if element.tag.endswith('circle'):
        cx, cy, r = float(element.get('cx')), float(element.get('cy')), float(element.get('r'))
        xs = np.arange(cx - r, cx + r, 1)
        ys = np.arange(cy - r, cy + r, 1)
        return [(x, y) for x in xs for y in ys if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2]

    elif element.tag.endswith('ellipse'):
        cx, cy, rx, ry = float(element.get('cx')), float(element.get('cy')), float(element.get('rx')), float(element.get('ry'))
        xs = np.arange(cx - rx, cx + rx, 1)
        ys = np.arange(cy - ry, cy + ry, 1)
        return [(x, y) for x in xs for y in ys if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1]

    elif element.tag.endswith('path'):
        path_data = element.get('d')
        path = parse_path(path_data)
        pixels = []
        for sub_path in path:
            for pos in np.arange(0, 1, 1 / resolution):
                point = sub_path.point(pos)
                pixels.append((point.real, point.imag))
        return pixels

    elif element.tag.endswith('rect'):
        return rectangle_to_pixels(element)

    elif element.tag.endswith('line'):
        return line_to_pixels(element)

    elif element.tag.endswith('polygon'):
        return polygon_to_pixels(element)

    return []


def parse_components(root, resolution=1000):
    components = {}
    for child in root:
        if child.tag.endswith(('path', 'circle', 'ellipse', 'rect', 'line', 'polygon')):
            component_id = child.get('id')
            component_pixels = component_to_pixels(child, resolution)
            if component_pixels:
                components[component_id] = component_pixels
    return components


if __name__ == '__main__':
    svg_string = open('generation.svg').read().strip()  # or load from a file
    resolution = 480  # set the resolution for rasterizing the SVG components

    import io
    root = parse_svg_file(io.StringIO(svg_string))  # replace this line with `parse_svg_file("filename.svg")` if you have an SVG file
    components = parse_components(root, resolution=resolution)

    print(components)


# In[ ]:


components.keys()


# In[ ]:


len(components['cell_membrane'])


# In[ ]:


canvas = np.zeros((480, 480))

for x, y in components['cell_membrane']:
    canvas[int(y), int(x)] = 1.0


# In[ ]:


cv2.imshow(canvas)


# In[ ]:





# In[ ]:

