import csv
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from monusac_data import image_and_annotation_generator


DOSSIER = Path(__file__).resolve().parent
ROOT = DOSSIER / "MoNuSAC_images_and_annotations"
COLUMNS = ["R_min", "G_min", "B_min", "R_max", "G_max", "B_max",
           "R_mean", "G_mean", "B_mean"]


def get_descriptor(region: np.ndarray) -> tuple:
    r = region[:, 0]
    g = region[:, 1]
    b = region[:, 2]

    descr = (r.min(), g.min(), b.min(),
             r.max(), g.max(), b.max(),
             r.mean(), g.mean(), b.mean())
    return tuple(float(v) for v in descr)


def get_descriptors_per_nuclei(im: np.ndarray, mask: np.ndarray) -> list:
    all_descriptors = []
    for idx in range(1, mask.max() + 1):
        mask_region = mask == idx
        if mask_region.sum() == 0:
            continue
        region = im[mask_region]
        all_descriptors.append(get_descriptor(region))
    return all_descriptors


def get_descriptor_background(im: np.ndarray, mask: np.ndarray) -> tuple:
    region = im[mask == 0]
    if len(region) == 0:
        return (float("nan"),) * 9
    return get_descriptor(region)


def save_to_csv(descriptors: list, path: Path):
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(COLUMNS)
        writer.writerows(descriptors)


def save_all_descriptors(path: Path):
    all_nuclei_descriptors = []
    all_background_descriptors = []

    for i, (im, mask) in enumerate(image_and_annotation_generator(path), start=1):
        all_nuclei_descriptors.extend(get_descriptors_per_nuclei(im, mask))
        all_background_descriptors.append(get_descriptor_background(im, mask))
        print(f"descripteurs : image {i}", flush=True)

    save_to_csv(all_nuclei_descriptors, DOSSIER / "nuclei.csv")
    save_to_csv(all_background_descriptors, DOSSIER / "background.csv")


def segment_nuclei(im: np.ndarray) -> np.ndarray:
    mask_r = im[:, :, 0] < 150
    mask_g = im[:, :, 1] < 110
    mask_b = im[:, :, 2] < 150
    return mask_r & mask_g & mask_b


def show_example(path: Path):
    im, mask = next(image_and_annotation_generator(path))
    prediction = segment_nuclei(im)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(im)
    axes[0].set_title("image")
    axes[1].imshow(mask > 0, cmap="gray")
    axes[1].set_title("annotations")
    axes[2].imshow(prediction, cmap="gray")
    axes[2].set_title("segmentation")
    for ax in axes:
        ax.axis("off")
    plt.tight_layout()
    plt.show()
    plt.close(fig)


def accuracy(prediction: np.ndarray, mask: np.ndarray) -> float:
    return float(np.mean(prediction == (mask > 0)))


def evaluate(path: Path):
    scores = []
    for im, mask in image_and_annotation_generator(path):
        prediction = segment_nuclei(im)
        scores.append(accuracy(prediction, mask))

    with (DOSSIER / "results.txt").open("w", encoding="utf-8") as fp:
        fp.write("seuils : R < 150, G < 110, B < 150\n")
        fp.write(f"nombre d images : {len(scores)}\n")
        fp.write(f"accuracy moyenne : {np.mean(scores):.4f}\n")
        fp.write(f"accuracy minimale : {min(scores):.4f}\n")
        fp.write(f"accuracy maximale : {max(scores):.4f}\n\n")
        for i, score in enumerate(scores, start=1):
            fp.write(f"image {i} : {score:.4f}\n")

    print(f"accuracy moyenne : {np.mean(scores):.4f}")


def main():
    evaluate(ROOT)
    show_example(ROOT)

if __name__ == "__main__":
    main()
