# setup.py
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md for the long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="fits_metadata_extractor",  # Replace with your desired package name
    version="0.1.0",
    author="Junaid Ramzan Bhat",
    author_email="junaidramzan3573@gmail.com",
    description="A Python library for processing FITS metadata and searching points/areas in the fits.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # Github URL 
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "requests>=2.25.0",
        "astropy>=4.2",
        "mocpy>=1.2.0",
        "pandas>=1.1.0",
        "shapely>=1.7.0",
        "matplotlib>=3.3.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Change if you use a different license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords="FITS metadata polygon astronomy",
    project_urls={  # Optional
        "Bug Reports": "https://github.com/yourusername/fits_polygon_tools/issues",
        "Source": "https://github.com/yourusername/fits_polygon_tools",
    },
)
