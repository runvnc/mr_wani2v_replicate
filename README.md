# MindRoot Wan2.1 Image-to-Video Plugin

A MindRoot plugin that converts static images to videos using the Replicate API and wavespeedai's wan-2.1-i2v-480p model.

## Features

- Convert any image URL to a short animated video
- Control the animation with text prompts
- Integration with MindRoot plugin system

## Requirements

- Python 3.8+
- Replicate API access (get a token at https://replicate.com)
- MindRoot framework

## Installation

1. Set the REPLICATE_API_TOKEN environment variable:
   ```bash
   export REPLICATE_API_TOKEN="your_replicate_api_token"
   ```

2. Install the plugin:
   ```bash
   cd /xfiles/plugins_ah/mr_wani2v_replicate
   pip install -e .
   ```

3. The plugin will be automatically discovered by MindRoot after installation.

## Usage

### As a Service

In another plugin, you can use the image_to_video service:

```python
from lib.providers.services import get_service

async def my_function():
    image_to_video = await get_service("image_to_video")
    video_path = await image_to_video(
        image="https://example.com/image.jpg",
        prompt="A woman is talking"
    )
    # video_path will be something like "imgs/Ab3Cde9fGh.mp4"
```

## API Reference

### image_to_video

```python
async def image_to_video(image: str, prompt: str = "A woman is talking", context: Optional[dict] = None) -> str:
```

**Parameters:**

- `image` (str): URL of the input image.
- `prompt` (str, optional): The prompt for the video generation. Defaults to "A woman is talking".
- `context` (Optional[dict], optional): The context data from MindRoot.

**Returns:**

- `str`: Relative path to the generated video file (e.g., "imgs/[random-id].mp4").

**Raises:**

- `Exception`: Propagates any exceptions encountered after printing the traceback.

## License

MIT License
