# Fits Metadata Extractor

**Fits Metadata Extractor** is a Python library tailored for  working with FITS (Flexible Image Transport System) files. It provides tools to extract homogenized metadata, perform geometric searches (points, circles, polygons), and overlay FITS data with MOCs (Multi-Order Coverage maps). 

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Installation via GitHub](#installation-via-github)
    - [Installing Locally](#installing-locally)
4. [Code Descriptions](#code-descriptions)
    - [Fits Metadata Extractor](#fits-metadata-extractor-fits_metadata_ex)
    - [Polygon Functionality](#polygon-functionality-polygon_func)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

---

## Overview

**Fits Metadata Extractor** simplifies the handling of FITS files by extracting and standardizing their metadata. It supports RA/DEC conversion, resolves celestial object names, and generates MOC maps. Additionally, it enables geometric operations such as determining if a point lies within a FITS image and identifying regions that overlap FITS coverage.

This library can be used locally, installed via pip, or accessed through GitHub. 

---

## Features

- **Homogenized Metadata Extraction**: Extract and standardize fields like RA, DEC, DATE-OBS, and EXPTIME from FITS files.
- **Polygon and Region Searches**:
  - Search if a given point lies within the coverage of any FITS file.
  - Perform circular or polygonal searches for regions overlapping FITS coverage.
- **MOC and WCS Visualization**:
  - Overlay MOCs on FITS images without requiring re-projection.
  - Efficiently align axes using transform-based mappings.
- ** CSV Generation**:
  - Compile metadata, including polygons and MOCs, into an easy-to-use CSV file.

---

## Installation

### Prerequisites

- **Python Version**: Python 3.6 or higher is required.
- **Package Manager**: Ensure `pip` is installed for package management.

### Installation via GitHub

To install the library directly from GitHub, use the following command:

```bash
pip install git+https://github.com/Bhat-Junaid/fits_extractor.git
```
Alternatively, clone the repository and install it locally:
```bash
git clone https://github.com/Bhat-Junaid/fits_extractor.git
cd fits_metadata_extractor
pip install .
```
### Installing locally
For local installation, download the repository or obtain the ZIP file. Extract it and navigate to the folder in the terminal. Then, run:
```bash
pip install .
```
Alternatively, run:

```bash
python setup.py install
```

#### Note:
one can also make sure that all the dependencies are installed by running the below given command before `pip install .`

```bash
pip install -r requirements.txt
```

---
## Code Descriptions

### Fits Metadata Extractor (`fits_metadata_ex`)

The **Fits Metadata Extractor** is a powerful Python module designed for working with FITS (Flexible Image Transport System) files. It focuses on extracting, homogenizing, and managing metadata from FITS files while providing tools for spatial analysis and advanced data handling.

---

#### Key Functionalities

1. **Metadata Extraction and Standardization**:
   - Extracts essential metadata from FITS files, including:
     - File name (`FILENAME`)
     - Right Ascension (`RA`) and Declination (`DEC`)
     - Observation date (`DATE-OBS`) and Modified Julian Date (`MJD-OBS`)
     - Exposure time (`EXPTIME`)
     - Instrument (`INSTRUME`) and Telescope (`TELESCOP`).
   - Handles coordinate transformations:
     - Converts galactic coordinates (`GLON`, `GLAT`) to ICRS if the reference system is `GALACTIC`.
     - Extracts fallback RA/DEC values from WCS headers if primary RA/DEC fields are unavailable.

2. **MOC and Polygon Generation**:
   - Calculates the Multi-Order Coverage (MOC) map for spatial coverage of FITS images.
   - Converts spatial footprints into STCS polygon syntax, enabling advanced region-based searches.

3. **Celestial Object Resolution**:
   - Integrates with the **Sesame Service** to resolve celestial object names into standardized formats.
   - Handles ambiguous or missing object names.

4. **Homogenized Metadata CSV Generation**:
   - Aggregates metadata from multiple FITS files into a single, structured CSV file.
   - Includes MOC strings and STCS polygon definitions for further analysis or visualization.

5. **Error Handling and Logging**:
   - Comprehensive logging for easy debugging and tracking of errors.
   - Handles invalid headers, missing metadata, and coordinate transformation failures.

---

#### How It Works

The `fits_metadata_ex` module comprises several key functions:

1. **`resolve_object_name`**:
   - Resolves celestial object names using the Sesame service.
   - Returns a standardized name for the object or the original name if resolution fails.

2. **`extract_fits_metadata`**:
   - Extracts metadata from a single FITS file.
   - Handles advanced coordinate transformations and generates MOC and polygon representations for spatial coverage.

3. **`create_fits_csv`**:
   - Processes a folder of FITS files and aggregates their metadata into a CSV file.
   - Ensures consistent and standardized metadata fields across all files.

4. **Supporting Utilities**:
   - **`parse_sesame_response`**: Parses the response from the Sesame service to extract a standardized object name.
   - **WCS Handling**: Automatically extracts and converts WCS information to RA/DEC when possible.

---

#### Note:
The primary code as well as the test jupyter notebook have been commented sufficiently to be understandable easily. The tests done in **`test_moc.ipynb`** are all commented and extra description has been provided so that the notebook is self-explanatory.

---
### Polygon Functionality (`polygon_func`)

This module provides functionality to determine whether a point lies within a convex polygon using the **dot product method**. It is specifically designed to handle convex polygons and efficiently computes the result by analyzing vector relationships between the point and polygon edges.

#### Function: `is_in_polygon`

**Description**:  
The `is_in_polygon` function checks if a given point lies inside or on the edge of a convex polygon. It uses the dot product method to determine the relative orientation of vectors connecting the point to polygon vertices and the edges of the polygon.

#### Parameters:
- **`point`** (`tuple`):  
  Coordinates of the point to check, in the format `(x, y)`.

- **`vertices`** (`list`):  
  A list of tuples representing the polygon vertices, ordered in a **clockwise direction**. Each vertex is defined as `(x, y)`.

#### Returns:
- **`bool`**:  
  - `True` if the point is inside or on the edge of the polygon.
  - `False` if the point is outside the polygon.

#### Key Steps:
1. **Vector Construction**:
   - For each edge of the polygon, compute the vector from the given point to the starting vertex of the edge (`M⃗Pᵢ`).
   - Compute the vector representing the edge itself (`PᵢPᵢ₊₁`).

2. **Dot Product Calculation**:
   - Calculate the dot product of the vectors for each edge.
   - Record the sign of the dot product for consistency.

3. **Sign Consistency Check**:
   - If all dot products have the same sign (or are zero), the point lies within or on the edge of the polygon.
   - If any dot product has a differing sign, the point lies outside the polygon.


### Contributing

Contributions to **Fits Metadata Extractor** are welcome! If you have ideas, bug fixes, or enhancements, feel free to contribute by following these steps:

1. **Fork the Repository**:
   - Navigate to the repository and fork it to your GitHub account.

2. **Create a Feature Branch**:
   - Clone your fork locally.
   - Create a new branch for your feature or bug fix:
     ```bash
     git checkout -b feature/your-feature-name
     ```

3. **Implement Your Changes**:
   - Write well-documented code.
   - 
3.1 **Commit Your Changes**:
    - Stage your changes:
      ```bash
      git add .
      ```
    - Commit with a descriptive message:
      ```bash
      git commit -m "Add feature:description of your changes"
      ```


4. **Submit a Pull Request**:
   - Push your changes to your fork:
     ```bash
     git push origin feature/your-feature-name
     ```
   - Navigate to the original repository and create a pull request.


## License

This project is licensed under the **MIT License**. For more details, see the [LICENSE](LICENSE) file.

---

## Contact

For questions, issues, or collaboration opportunities, feel free to reach out:

- **Name**: Junaid Ramzan Bhat
- **GitHub**: [github.com/Bhat-Junaid](https://github.com/Bhat-Junaid)  
- **Email**: junaidramzan3573@gmail.com

