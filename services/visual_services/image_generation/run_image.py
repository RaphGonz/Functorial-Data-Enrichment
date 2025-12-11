import argparse
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os
import numpy as np
import sys
from models.network_swinir import SwinIR as SwinIRNet  # after sys.path append


# ------------------------------------------------------------
# LOAD SD-TURBO VIA AUTOPIPELINE (GPU, FP16)
# ------------------------------------------------------------
pipe = StableDiffusionPipeline.from_single_file(
    "/models/sd15/sd15.ckpt",
    torch_dtype=torch.float16
).to("cuda")


# ------------------------------------------------------------
# LOAD SWINIR
# ------------------------------------------------------------
sys.path.append("/app/SwinIR")

_swinir_checkpoint = "/models/swinir/real_x4.pth"

_swinir = SwinIRNet(
    upscale=4,
    in_chans=3,
    img_size=64,
    window_size=8,
    img_range=1.0,
    depths=[6, 6, 6, 6, 6, 6],
    embed_dim=240,
    num_heads=[6, 6, 6, 6, 6, 6],
    mlp_ratio=2,
    upsampler="nearest+conv",
    resi_connection="1conv",
)

state = torch.load(_swinir_checkpoint, map_location="cuda")
_swinir.load_state_dict(state["params"], strict=True)
_swinir = _swinir.to("cuda").eval()


# ------------------------------------------------------------
# UPSCALE FUNCTION
# ------------------------------------------------------------
def upscale_swinir(img: Image.Image) -> Image.Image:
    arr = np.array(img).astype(np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))  # HWC -> CHW
    tensor = torch.from_numpy(arr).unsqueeze(0).cuda()

    with torch.no_grad():
        out = _swinir(tensor)

    out = out.squeeze().cpu().numpy()
    out = np.transpose(out, (1, 2, 0))  # CHW -> HWC
    out = (np.clip(out, 0, 1) * 255).astype(np.uint8)

    return Image.fromarray(out)


# ------------------------------------------------------------
# GENERATE WITH SD
# ------------------------------------------------------------
def generate(prompt: str) -> Image.Image:
    out = pipe(
        prompt=prompt,
        num_inference_steps=25,   # 20–30 pour SD 1.x
        guidance_scale=7.5,       # CFG standard SD 1.5
    )
    return out.images[0]

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str)
    parser.add_argument("--outdir", type=str, required=True)
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    input_path = args.input_path
    
    with open(input_path, "r") as f:
        prompt = f.read().rstrip("\n")
    

    # 1) Generate image 512px (SD-Turbo)
    img_512 = generate(prompt)

    # 2) Upscale 4× (SwinIR)
    img_up = upscale_swinir(img_512)

    outpath = os.path.join(args.outdir, "base_image.png")
    img_up.save(outpath)

    print(outpath)


if __name__ == "__main__":
    main()
