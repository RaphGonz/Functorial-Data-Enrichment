# /app/detectron2_repo/run_object_detection.py

import argparse
import json
import os

import cv2 # type: ignore
import numpy as np # type: ignore
from PIL import Image # type: ignore

from detectron2.config import get_cfg # type: ignore
from detectron2.engine import DefaultPredictor # type: ignore
from detectron2 import model_zoo # type: ignore
from detectron2.data import MetadataCatalog # type: ignore


DEFAULT_WEIGHTS_PATH = os.environ.get(
    "DETECTRON2_WEIGHTS",
    "/app/models/mask_rcnn_R_50_FPN_3x.pkl",  # à adapter si besoin
)


def load_predictor(weights_path: str, score_thresh: float = 0.5):
    if not os.path.isfile(weights_path):
        raise FileNotFoundError(f"Weights file not found: {weights_path}")

    cfg = get_cfg()
    cfg.merge_from_file(
        model_zoo.get_config_file(
            "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
        )
    )
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = score_thresh
    cfg.MODEL.WEIGHTS = weights_path

    predictor = DefaultPredictor(cfg)
    return predictor, cfg


def bbox_to_int_clipped(box, width: int, height: int):
    x1, y1, x2, y2 = box
    x1 = max(0, min(width - 1, int(np.floor(x1))))
    y1 = max(0, min(height - 1, int(np.floor(y1))))
    x2 = max(0, min(width, int(np.ceil(x2))))
    y2 = max(0, min(height, int(np.ceil(y2))))
    return x1, y1, x2, y2


def save_mask_and_crop(
    image_bgr: np.ndarray,
    mask_bool: np.ndarray,
    outdir: str,
    obj_id: int,
):
    os.makedirs(outdir, exist_ok=True)

    h, w = mask_bool.shape
    mask_uint8 = (mask_bool.astype(np.uint8) * 255)

    # noms de fichiers
    mask_filename = f"obj_{obj_id:03d}_mask.png"
    crop_filename = f"obj_{obj_id:03d}.png"

    mask_path = os.path.join(outdir, mask_filename)
    crop_path = os.path.join(outdir, crop_filename)

    # sauvegarde du mask en niveaux de gris
    cv2.imwrite(mask_path, mask_uint8)

    # image RGBA recadrée (fond transparent)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    rgba = np.dstack([image_rgb, mask_uint8])

    # bbox serrée basée sur le masque
    ys, xs = np.where(mask_bool)
    if ys.size == 0 or xs.size == 0:
        # pas de pixels -> on sauve quand même une image vide minimale
        crop_rgba = np.zeros((1, 1, 4), dtype=np.uint8)
    else:
        y_min, y_max = ys.min(), ys.max()
        x_min, x_max = xs.min(), xs.max()  # inclusif
        crop_rgba = rgba[y_min : y_max + 1, x_min : x_max + 1]

    Image.fromarray(crop_rgba, mode="RGBA").save(crop_path)

    return mask_path, crop_path


def run_inference(input_path: str, outdir: str, weights_path: str):
    image_bgr = cv2.imread(input_path)
    if image_bgr is None:
        raise ValueError(f"Cannot read image: {input_path}")

    h, w = image_bgr.shape[:2]

    predictor, cfg = load_predictor(weights_path)
    outputs = predictor(image_bgr)

    instances = outputs["instances"].to("cpu")
    num_instances = len(instances)

    # pas de détection -> JSON vide
    if num_instances == 0:
        return []

    boxes = instances.pred_boxes.tensor.numpy()           # (N, 4)
    scores = instances.scores.numpy()                     # (N,)
    classes = instances.pred_classes.numpy()              # (N,)
    masks = instances.pred_masks.numpy()                  # (N, H, W) bool

    metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
    class_names = list(getattr(metadata, "thing_classes", []))

    objects = []

    for i in range(num_instances):
        box = boxes[i]
        score = float(scores[i])
        cls_id = int(classes[i])
        mask_bool = masks[i]

        x1, y1, x2, y2 = bbox_to_int_clipped(box, w, h)

        if 0 <= cls_id < len(class_names):
            label = class_names[cls_id]
        else:
            label = str(cls_id)

        mask_path, crop_path = save_mask_and_crop(
            image_bgr=image_bgr,
            mask_bool=mask_bool,
            outdir=outdir,
            obj_id=i,
        )

        obj = {
            "id": f"obj_{i:03d}",
            "label": label,
            "bbox": [x1, y1, x2, y2],
            "score": score,
            "segmentation": {
                "mask_path": mask_path,
                "cropped_image_path": crop_path,
                "confidence": score,
                "method": "detectron2_mask_rcnn_R_50_FPN_3x",
            },
            # "size_estimation": null,
            # "material_estimation": null,
        }

        objects.append(obj)

    return objects


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Chemin de l'image d'entrée",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        required=True,
        help="Dossier de sortie (contiendra objects.json et les PNG)",
    )
    parser.add_argument(
        "--weights",
        type=str,
        default=DEFAULT_WEIGHTS_PATH,
        help="Chemin des poids Detectron2 (Mask R-CNN R50 FPN)",
    )
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    objects = run_inference(args.input, args.outdir, args.weights)

    output_json = os.path.join(args.outdir, "objects.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(objects, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
