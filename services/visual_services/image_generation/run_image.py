import argparse
import os

import torch
import numpy as np
from PIL import Image

from diffusers import StableDiffusionPipeline

from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet


# -------------------------------------------------------------
# Stable Diffusion generation
# -------------------------------------------------------------
def generate(pipe, prompt: str) -> Image.Image:
    out = pipe(
        prompt=prompt,
        num_inference_steps=10,
        guidance_scale=7.5,
    )
    return out.images[0]


# -------------------------------------------------------------
# Real-ESRGAN upscale (official API)
# -------------------------------------------------------------
def upscale_realesrgan(upsampler: RealESRGANer, img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    img_np = np.array(img)  # RGB uint8 HWC

    # RGB -> BGR
    img_bgr = img_np[:, :, ::-1]

    with torch.no_grad():
        output_bgr, _ = upsampler.enhance(img_bgr, outscale=4)

    # BGR -> RGB
    output_rgb = output_bgr[:, :, ::-1]

    return Image.fromarray(output_rgb, mode="RGB")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, required=True)
    parser.add_argument("--outdir", type=str, required=True)
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    # ---------------------------------------------------------
    # Load prompt
    # ---------------------------------------------------------
    with open(args.input_path, "r") as f:
        prompt = f.read().rstrip("\n")

    # ---------------------------------------------------------
    # Load Stable Diffusion
    # ---------------------------------------------------------
    print("Loading Stable Diffusion...")
    pipe = StableDiffusionPipeline.from_single_file(
        "/app/models/sd15/v1-5-pruned-emaonly.safetensors",
        torch_dtype=torch.float32,
        safety_checker=None,
    ).to("cuda")

    # ---------------------------------------------------------
    # Load Real-ESRGAN (x4plus)
    # ---------------------------------------------------------
    print("Loading Real-ESRGAN...")

    model = RRDBNet(
        num_in_ch=3,
        num_out_ch=3,
        num_feat=64,
        num_block=23,
        num_grow_ch=32,
        scale=4,
    )

    upsampler = RealESRGANer(
        scale=2,
        model_path="/app/models/realesrgan/RealESRGAN_x4plus.pth",
        model=model,
        tile=0,            # mettre >0 si OOM GPU
        tile_pad=10,
        pre_pad=0,
        half=False,        # True si tu veux FP16
        device="cuda",
    )

    print("Models loaded.")

    # ---------------------------------------------------------
    # Generate + Upscale
    # ---------------------------------------------------------
    print("Generating image...")
    img_512 = generate(pipe, prompt)

    print("Upscaling image...")
    img_up = upscale_realesrgan(upsampler, img_512)

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------
    outpath = os.path.join(args.outdir, "base_image.png")
    img_up.save(outpath)

    print("Saved:", outpath)


if __name__ == "__main__":
    main()
