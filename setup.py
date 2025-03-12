from setuptools import setup, find_packages

setup(
    name="mr_wani2v_replicate",
    version="1.0.0",
    description="Convert image to video using replicate's wan-2.1-i2v-480p model",
    author="MindRoot",
    author_email="info@mindroot.ai",
    packages=find_packages(where="src"),
    package_dir={"" : "src"},
    package_data={
        "mr_wani2v_replicate": [
            "static/js/*.js",
            "static/css/*.css",
            "templates/*.jinja2",
            "inject/*.jinja2",
            "override/*.jinja2"
        ],
    },
    install_requires=[
        "nanoid",
        "Pillow",
        "replicate"
    ],
    python_requires=">=3.8",
)