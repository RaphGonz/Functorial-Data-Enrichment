# /app/pose/pose_skeleton_only.py

import argparse
import os

import numpy as np # type: ignore
from ultralytics import YOLO # type: ignore
from PIL import Image, ImageDraw # type: ignore
#non résolu mais le seront dans le conteneur docker

# Connexions de squelette (indices COCO 17 points, 0-based)
SKELETON_EDGES = [
    (5, 7), (7, 9),       # bras gauche
    (6, 8), (8, 10),      # bras droit
    (11, 13), (13, 15),   # jambe gauche
    (12, 14), (14, 16),   # jambe droite
    (5, 6),               # épaules
    (11, 12),             # hanches
    (5, 11), (6, 12),     # tronc
]


def draw_skeletons_on_blank(kpts_xy: np.ndarray, size: tuple[int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = 3
    line_width = 2

    for person in kpts_xy:
        for (i, j) in SKELETON_EDGES:
            if i >= person.shape[0] or j >= person.shape[0]:
                continue
            x1, y1 = person[i]
            x2, y2 = person[j]
            if (x1 == 0 and y1 == 0) or (x2 == 0 and y2 == 0):
                continue
            draw.line((x1, y1, x2, y2), width=line_width)

        for x, y in person:
            if x == 0 and y == 0:
                continue
            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                outline=(255, 255, 255),
                width=1,
            )

    return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Chemin de l'image d'entrée")
    parser.add_argument("--output", type=str, required=True, help="Chemin de l'image de sortie (squelettes)")
    parser.add_argument("--model", type=str, default="yolov8n-pose.pt", help="Chemin ou nom du modèle YOLOv8 pose")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    outdir = os.path.dirname(output_path)
    if outdir:
        os.makedirs(outdir, exist_ok=True)

    model = YOLO(args.model)

    with Image.open(input_path) as im:
        im = im.convert("RGB")
        w, h = im.size

    results = model(input_path)[0]

    if results.keypoints is None:
        blank = Image.new("RGB", (w, h), (0, 0, 0))
        blank.save(output_path)
        return

    kpts_xy = results.keypoints.xy.cpu().numpy()

    out_img = draw_skeletons_on_blank(kpts_xy, (w, h))
    out_img.save(output_path)


if __name__ == "__main__":
    main()
