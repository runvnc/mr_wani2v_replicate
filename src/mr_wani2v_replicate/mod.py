import os
import asyncio
import replicate
import traceback
import base64
from io import BytesIO
from PIL import Image
from nanoid import generate as nanoid_generate
from lib.providers.services import service
from typing import Optional, Union


def write_video(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def pillow_image_to_base64_url(image: Image.Image, format: str = "JPEG") -> str:
    """Convert a Pillow image to a base64 data URL.
    
    Args:
        image (Image.Image): The Pillow image object.
        format (str, optional): The image format. Defaults to "JPEG".
    
    Returns:
        str: Base64 data URL for the image.
    """
    buffered = BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    mime_type = f"image/{format.lower()}"
    return f"data:{mime_type};base64,{img_str}"


@service()
async def image_to_video(image: Union[str, Image.Image], prompt: str = "A woman is talking", context: Optional[dict] = None) -> str:
    """Convert an input image to a video using the wavespeedai/wan-2.1-i2v-480p model.
    
    Parameters:
        image (Union[str, Image.Image]): Either a URL string or a Pillow Image object.
        prompt (str, optional): The prompt for the video generation. Defaults to 'A woman is talking'.
        context (Optional[dict], optional): The context data.
    
    Returns:
        str: Relative path to the generated video file (e.g., "imgs/[random-id].mp4").
    
    Raises:
        Exception: Propagates any exceptions encountered after printing the traceback.
    """
    replicate_api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not replicate_api_token:
        raise Exception("REPLICATE_API_TOKEN not set in environment")
    
    replicate.api_token = replicate_api_token
    
    # Convert Pillow Image to base64 data URL if needed
    image_input = image
    if isinstance(image, Image.Image):
        image_input = pillow_image_to_base64_url(image)
    
    input_data = {
        "image": image_input,
        "prompt": prompt,
        "max_area": "832x480",
        "fast_mode": "Off",
        "num_frames": 81,
        "sample_shift": 2,
        "sample_steps": 40,
        "frames_per_second": 24,
        "sample_guide_scale": 4
    }
    
    try:
        output = await asyncio.to_thread(replicate.run, "wavespeedai/wan-2.1-i2v-480p", input=input_data)
        video_data = await asyncio.to_thread(output.read)
        
        imgs_dir = os.path.join(os.getcwd(), "imgs")
        if not os.path.exists(imgs_dir):
            os.makedirs(imgs_dir)
        
        random_filename = nanoid_generate(size=10) + ".mp4"
        output_path = os.path.join("imgs", random_filename)
        await asyncio.to_thread(lambda: write_video(output_path, video_data))
        return output_path
    except Exception as e:
        traceback.print_exc()
        raise e
