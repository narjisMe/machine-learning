"""Read data from the MoNuSAC dataset.

@author Adrien Foucart

Dataset contains images (using .tif format version) and annotations (XML)
"""

import pathlib
import sys
import xml.etree.ElementTree as elt
from collections.abc import Generator

import numpy as np
from matplotlib import pyplot as plt
from skimage.io import imread
from skimage import draw as skdraw

type Coordinate = tuple[int, int]


def find_celltype(element: elt.Element) -> str:
    attrs = element.find("Attributes")
    if attrs is None:
        return "unknown"
    for attr in attrs.findall("Attribute"):
        if "Name" in attr.attrib:
            return attr.attrib["Name"]
    return "unknown"


def find_regions(element: elt.Element) -> list[list[Coordinate]]:
    region_coordinates = []
    regions = element.find("Regions")
    if regions is None:
        return []
    for region in regions.findall("Region"):
        vertices = region.find("Vertices")
        if vertices is None:
            continue
        coords = []
        for vertex in vertices.findall("Vertex"):
            try:
                coords.append((int(vertex.attrib["X"]), int(vertex.attrib["Y"])))
            except ValueError:
                coords.append(
                    (int(float(vertex.attrib["X"])), int(float(vertex.attrib["Y"])))
                )
        region_coordinates.append(coords)
    return region_coordinates


def get_nuclei_from_xml(xml_file: pathlib.Path) -> list[tuple[str, list[Coordinate]]]:
    """Get all nuclei annotations from the XML file.

    Returns as a list of tuples with the cell type as a str, and a list of vertex coordinates.
    """
    annotations = []
    tree = elt.parse(xml_file)
    root = tree.getroot()
    for annotation in root:
        celltype = find_celltype(annotation)
        try:
            regions = find_regions(annotation)
        except ValueError:
            print(f"Couldn't process: {xml_file.name}:{celltype}")
            continue
        for region in regions:
            annotations.append((celltype, region))

    return annotations


def xml_and_image_file_generator(
    path: pathlib.Path,
) -> Generator[tuple[pathlib.Path, pathlib.Path], None, None]:
    for xml in path.glob("*.xml"):
        impath = xml.parent / f"{xml.stem}.tif"
        if not impath.is_file():
            continue
        yield xml, impath


def make_mask_from_vertices(
    nuclei: list[list[Coordinate]], imshape: tuple[int, int]
) -> np.ndarray:
    mask = np.zeros(imshape, dtype="int")
    for idx, region in enumerate(nuclei, start=1):
        rr, cc = skdraw.polygon([y for _, y in region], [x for x, _ in region], imshape)
        mask[rr, cc] = idx
    return mask


def image_and_annotation_generator(
    root: pathlib.Path, filter_celltype: str | None = None
) -> Generator[tuple[np.ndarray, np.ndarray], None, None]:
    for patient in root.iterdir():
        if not patient.is_dir():
            continue
        for xmlpath, impath in xml_and_image_file_generator(patient):
            nuclei = get_nuclei_from_xml(xmlpath)
            im = imread(impath)
            if filter_celltype:
                nuclei = [
                    nucleus
                    for nucleus in nuclei
                    if nucleus[0].lower() == filter_celltype.lower()
                ]
            mask = make_mask_from_vertices([coords for _, coords in nuclei], im.shape[:2])
            yield im, mask


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: no path provided.")
        sys.exit(0)

    path = pathlib.Path(sys.argv[1])
    for im, nuclei in image_and_annotation_generator(path):
        if len(nuclei) == 0:
            continue
        fig, axes = plt.subplots(1, 2)
        axes[0].imshow(im)
        axes[1].imshow(nuclei, cmap='gray')
        fig.tight_layout()
        plt.show()
        break
