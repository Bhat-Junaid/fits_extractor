import os
import requests
import warnings
import logging
import csv
from astropy.io import fits
from astropy.wcs import WCS
from astropy.time import Time
from mocpy import MOC
from astropy.coordinates import SkyCoord
import astropy.units as u

from astropy.utils.exceptions import AstropyWarning

warnings.filterwarnings('ignore', category=AstropyWarning)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Sesame service
SESAME_URL = "https://cds.unistra.fr/cgi-bin/nph-sesame/@NSV?{}"


def parse_sesame_response(response_text):
    """
    Parse the Sesame service response to extract the standardized object name.

    Parameters
    ----------
    response_text : str
        The raw text response from the Sesame service.

    Returns
    -------
    str or None
        The standardized object name if found, else None.
    """
    # Split the response by lines in case of multiple entries
    lines = response_text.strip().splitlines()

    if not lines:
        return None

    # first line contains the standardized name
    standardized_name = lines[0].strip()


    return standardized_name if standardized_name else None

def resolve_object_name(object_name):
    """
    Resolve a celestial object name to a standardized form using the Sesame service.

    Parameters
    ----------
    object_name : str
        Name of the celestial object to resolve.

    Returns
    -------
    str
        Standardized object name if resolved successfully, or the original name if not.
    """
    # Validate input
    if not object_name or object_name.strip().lower() == "unknown":
        logging.info("Input object name is empty or 'unknown'. Returning 'Unknown'.")
        return "Unknown"

    try:
        # Send a GET request with a timeout of 10 seconds
        response = requests.get(SESAME_URL.format(object_name.strip()), timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response content to extract the standardized name
            standardized_name = parse_sesame_response(response.text)

            if standardized_name:
                logging.info(f"Resolved '{object_name}' to '{standardized_name}'.")
                return standardized_name
            else:
                logging.warning(f"No standardized name found for '{object_name}'. Returning original name.")
                return object_name
        else:
            logging.warning(f"Failed to resolve '{object_name}'. HTTP Status Code: {response.status_code}.")
            return object_name

    except requests.exceptions.RequestException as e:
        # Log the exception details
        logging.error(f"Error resolving object name '{object_name}': {e}")
        return object_name

def extract_fits_metadata(fits_file):
    """
    Extract metadata from a FITS file header, homogenize the data,
    and calculate spatial coverage if possible.

    Handles:
    - RA/DEC in GALACTIC by converting them to ICRS if RADESYS='GALACTIC'.
    - MOC from footprint (Polygon).

    Returns
    -------
    dict
        A dictionary of consistently named fields.
    """
    # Open the FITS file
    with fits.open(fits_file) as hdul:
        header = hdul[0].header
        wcs = WCS(header)

        # Build a baseline metadata dict with all expected columns
        metadata = {
            "FILENAME": os.path.basename(fits_file),
            "NAXIS": header.get("NAXIS", "N/A"),
            "OBJECT": resolve_object_name(header.get("OBJECT", "Unknown")),
            "RA": None,
            "DEC": None,
            "RADESYS": header.get("RADESYS", "ICRS"),
            "DATE-OBS": None,
            "MJD-OBS": None,
            "EXPTIME": 0.0,
            "INSTRUME": header.get("INSTRUME", "Unknown"),
            "TELESCOP": header.get("TELESCOP", "Unknown"),
            "MOC": None,
            "Polygon": None
        }

        # 1) RA / DEC from header or WCS
        try:
            if metadata["RADESYS"].upper() == "GALACTIC":
                # For Galactic coordinates, use CRVAL1 (l) and CRVAL2 (b)
                l_val = wcs.wcs.crval[0]
                b_val = wcs.wcs.crval[1]
                gal_coord = SkyCoord(l=l_val * u.deg, b=b_val * u.deg, frame='galactic')
                icrs = gal_coord.icrs
                metadata["RA"] = icrs.ra.deg
                metadata["DEC"] = icrs.dec.deg
            else:
                # For ICRS coordinates, use RA and DEC from header
                raw_ra = header.get("RA", None)
                raw_dec = header.get("DEC", None)
                if raw_ra is not None and raw_dec is not None:
                    ra_val = float(raw_ra)
                    dec_val = float(raw_dec)
                    metadata["RA"] = ra_val
                    metadata["DEC"] = dec_val
                else:
                    # Fallback to CRVAL1 and CRVAL2 if RA/DEC are missing
                    wcs_ra = wcs.wcs.crval[0]
                    wcs_dec = wcs.wcs.crval[1]
                    metadata["RA"] = wcs_ra
                    metadata["DEC"] = wcs_dec
        except Exception as e:
            logging.error(f"Error extracting RA/DEC for {fits_file}: {e}")

        # 2) DATE-OBS
        date_obs = header.get("DATE-OBS")
        if date_obs:
            try:
                t = Time(date_obs, format="isot", scale="utc")
                metadata["DATE-OBS"] = t.iso
                metadata["MJD-OBS"] = t.mjd
            except ValueError:
                logging.warning(f"Invalid DATE-OBS format in {fits_file}: '{date_obs}'")

        # 3) EXPTIME
        exptime_val = header.get("EXPTIME", 0)
        try:
            metadata["EXPTIME"] = float(exptime_val)
        except ValueError:
            logging.warning(f"Invalid EXPTIME value in {fits_file}: '{exptime_val}'")

        # 4) If we have a celestial WCS with at least 2 axes, build a MOC
        wcs_celestial = wcs.celestial
        if wcs_celestial.naxis >= 2:
            try:
                footprint = wcs_celestial.calc_footprint()
                coords = SkyCoord(footprint, unit="deg", frame="icrs")

                # Build MOC
                moc = MOC.from_polygon_skycoord(coords)
                metadata["MOC"] = str(moc)  # Convert to string for CSV storage

                # STCS polygon
                polygon_str = " ".join([f"{c.ra.deg} {c.dec.deg}" for c in coords])
                metadata["Polygon"] = f"Polygon ICRS {polygon_str}"
            except Exception as e:
                # If footprint or MOC fails, leave them None
                logging.error(f"Error building MOC for {fits_file}: {e}")

    return metadata

def create_fits_csv(folder_path, csv_path):
    """
    Creates a CSV file containing homogenized metadata from all FITS in folder_path.

    Parameters
    ----------
    folder_path : str
        Path to the folder containing FITS files.
    csv_path : str
        Where to write the CSV file.

    Returns
    -------
    None
        Writes a CSV file. No return object.
    """
    # We'll store all metadata dicts here
    metadata_list = []

    # Collect data
    for f in os.listdir(folder_path):
        if f.lower().endswith((".fit", ".fits")):
            fits_file = os.path.join(folder_path, f)
            try:
                md = extract_fits_metadata(fits_file)
                metadata_list.append(md)
            except Exception as e:
                logging.error(f"Error processing {f}: {e}")

    if not metadata_list:
        logging.warning(f"No valid FITS found in {folder_path}. No CSV created.")
        return

    # Determine a consistent list of columns
    # (all dicts have the same keys in the code, but we ensure it programmatically)
    columns = sorted(metadata_list[0].keys())

    # Write CSV
    try:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for mdict in metadata_list:
                writer.writerow(mdict)
        logging.info(f"CSV file created: {csv_path}")
    except Exception as e:
        logging.error(f"Failed to write CSV file '{csv_path}': {e}")
