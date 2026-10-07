import numpy as np
from skimage.io import imread
from matplotlib import pyplot as plt


def print_image_information(im: np.ndarray) -> None:
    height, width = im.shape[:2]
    print(f"Image shape: {height}x{width}px")

    if len(im.shape) > 2:
        print(f"Number of channels: {im.shape[2]}")
    else:
        print("Grayscale image")

    print(f"Min/max values: {im.min()}, {im.max()}")


def display_region(im: np.ndarray, x: int, y: int,
                   width: int, height: int) -> None:
    region = im[y:y+height, x:x+width]
    plt.figure()
    plt.imshow(region)
    plt.show()


def get_histogram(im: np.ndarray) -> list[int]:
    hist = [0 for _ in range(256)]

    for v in range(256):
        n_pixels = (im == v).sum()
        hist[v] = n_pixels

    return hist


def display_rgb_histograms(im: np.ndarray) -> None:
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    hist_r = get_histogram(r)
    hist_g = get_histogram(g)
    hist_b = get_histogram(b)

    plt.figure()
    plt.bar(range(256), hist_r, color='r', alpha=0.6)
    plt.bar(range(256), hist_g, color='g', alpha=0.6)
    plt.bar(range(256), hist_b, color='b', alpha=0.6)

    plt.show()


def display_image_and_mask(im: np.ndarray, mask: np.ndarray) -> None:
    plt.figure()
    plt.imshow(im)
    plt.figure()
    plt.imshow(mask)
    plt.show()


def main():
    im = imread("./data/cat_wall.jpg")

    print_image_information(im)
    display_region(
        im,
        x=150,
        y=700,
        width=250,
        height=im.shape[0] - 700
    )

    display_rgb_histograms(im)
    mask = im[..., 0] > 230

    display_image_and_mask(im, mask)


if __name__ == "__main__":
    main()