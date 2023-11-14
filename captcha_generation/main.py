import torch
import random
import os
from PIL import Image
from diffusers import (
    DiffusionPipeline,
    AutoencoderKL,
    ControlNetModel,
    StableDiffusionControlNetPipeline,
    StableDiffusionControlNetImg2ImgPipeline,
    DPMSolverMultistepScheduler,
    EulerDiscreteScheduler
)

BASE_MODEL = "SG161222/Realistic_Vision_V5.1_noVAE"
CONTROLNET_MODEL = "monster-labs/control_v1p_sd15_qrcode_monster"
IMAGE_DIR = r"C:\Users\Jooney Han\Desktop\KSEF2023\images"
OUTPUT_DIR = r"C:\Users\Jooney Han\Desktop\KSEF2023"  

vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float16)
controlnet = ControlNetModel.from_pretrained(CONTROLNET_MODEL, torch_dtype=torch.float16)
main_pipe = StableDiffusionControlNetPipeline.from_pretrained(
    BASE_MODEL,
    controlnet=controlnet,
    vae=vae,
    safety_checker=None,
    torch_dtype=torch.float16,
).to("cuda")

image_pipe = StableDiffusionControlNetImg2ImgPipeline(**main_pipe.components)

SAMPLER_MAP = {
    "DPM++ Karras SDE": lambda config: DPMSolverMultistepScheduler.from_config(config, use_karras=True, algorithm_type="sde-dpmsolver++"),
    "Euler": lambda config: EulerDiscreteScheduler.from_config(config),
}

def center_crop_resize(img, output_size=(512, 512)):
    width, height = img.size
    new_dimension = min(width, height)
    left = (width - new_dimension)/2
    top = (height - new_dimension)/2
    right = (width + new_dimension)/2
    bottom = (height + new_dimension)/2
    img = img.crop((left, top, right, bottom))
    img = img.resize(output_size)
    return img

def upscale(samples, upscale_method, scale_by):
    width = round(samples.shape[3] * scale_by)
    height = round(samples.shape[2] * scale_by)
    return torch.nn.functional.interpolate(samples, size=(height, width), mode=upscale_method)

def convert_image_to_pil(image_path):
    with open(image_path, 'rb') as f:
        image = Image.open(f)
        image = image.convert("RGB")
    return image

def run_inference(control_image_path, prompt, negative_prompt, guidance_scale=8.0, controlnet_conditioning_scale=1.0,
                  control_guidance_start=0.0, control_guidance_end=1.0, upscaler_strength=0.5, seed=-1, sampler="Euler"):
    
    control_image = convert_image_to_pil(control_image_path)
    control_image_small = center_crop_resize(control_image)
    control_image_large = center_crop_resize(control_image, (1024, 1024))
    
    my_seed = random.randint(0, 2**32 - 1) if seed == -1 else seed
    generator = torch.Generator(device="cuda").manual_seed(my_seed)
    
    main_pipe.scheduler = SAMPLER_MAP[sampler](main_pipe.scheduler.config)
    
    out = main_pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=control_image_small,
        guidance_scale=float(guidance_scale),
        controlnet_conditioning_scale=float(controlnet_conditioning_scale),
        generator=generator,
        control_guidance_start=float(control_guidance_start),
        control_guidance_end=float(control_guidance_end),
        num_inference_steps=15
    )
    
    output_image = out["images"][0]
    output_image = output_image.convert("RGB") 

    output_image = output_image.resize((output_image.width * 2, output_image.height * 2), Image.NEAREST)

    output_image_path = os.path.join(OUTPUT_DIR, 'output_image')
    output_image.save(output_image_path + random.randint(0, 1000).__str__() + ".png")
    print(f"Inference complete. Image saved to: {output_image_path}")

if __name__ == "__main__":
    control_image_path = os.path.join(IMAGE_DIR, 'ill.jpg')
    prompt = "Medieval village scene with busy streets and a castle in the distance"
    negative_prompt = "low quality, blurry"
    guidance_scale = 7.5  
    controlnet_conditioning_scale = 3

    for x in range(10):
        run_inference(
            control_image_path=control_image_path,
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            controlnet_conditioning_scale=controlnet_conditioning_scale
        )