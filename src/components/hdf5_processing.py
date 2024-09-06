import os
import subprocess
import h5py
import numpy as np
import rasterio
from rasterio.transform import from_origin

# Directory for temporary files
TEMP_FOLDER = 'temp'
os.makedirs(TEMP_FOLDER, exist_ok=True)  # Ensure the folder exists

def process_hdf5(file_path, selected_band=None):
    """Processes an HDF5 file to extract a selected band and convert it to COG format."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found")

    with h5py.File(file_path, 'r') as hdf:
        available_bands = list(hdf.keys())
        print(f"Available bands: {', '.join(available_bands)}")

        # Prompt user if no band was provided
        if not selected_band:
            selected_band = input("Enter the band name to convert to COG from the above list: ")

        if selected_band not in available_bands:
            raise ValueError(f"Band '{selected_band}' not found in the available bands")

        dataset = hdf[selected_band][:]
        print(f"Debug: Dataset shape = {dataset.shape}")  # Debug print

        # Example geotransform values, replace with actual values if available
        geotransform = (0, 1, 0, 0, 0, -1)  # Replace with actual geotransform
        print(f"Debug: Geotransform = {geotransform}")  # Debug print

        # Calculate pixel size
        pixel_size = np.sqrt(geotransform[1] ** 2 + geotransform[5] ** 2)
        print(f"Debug: Calculated pixel_size = {pixel_size}")

        # Prepare file paths for outputs
        output_tiff = os.path.join(TEMP_FOLDER, f"{selected_band}.tif")

        if len(dataset.shape) == 2:
            # For 2D data
            convert_to_tiff(dataset, output_tiff, geotransform, pixel_size)
        elif len(dataset.shape) == 3:
            # For 3D data
            convert_3d_to_tiff(dataset, selected_band, geotransform, pixel_size)
        else:
            raise ValueError(f"Unsupported data shape for {selected_band}: {dataset.shape}")

        # Convert to COG
        cog_output_tiff = convert_to_cog(output_tiff, selected_band)
        return cog_output_tiff

def convert_to_tiff(data, output_tiff, geotransform, pixel_size):
    """Converts a 2D array to a GeoTIFF file."""
    with rasterio.open(output_tiff, 'w', driver='GTiff', height=data.shape[0], width=data.shape[1],
                       count=1, dtype=data.dtype, crs='+proj=latlong',
                       transform=from_origin(geotransform[0], geotransform[3], pixel_size, pixel_size)) as dst:
        dst.write(data, 1)
    print(f"GeoTIFF created: {output_tiff}")

def convert_3d_to_tiff(data, selected_band, geotransform, pixel_size):
    """Converts each band of a 3D array to a separate GeoTIFF file and then to COG."""
    for i in range(data.shape[0]):
        band_data = data[i, :, :]
        band_output_tiff = os.path.join(TEMP_FOLDER, f"{selected_band}.tif")
        convert_to_tiff(band_data, band_output_tiff, geotransform, pixel_size)
        cog_band_output_tiff = os.path.join(TEMP_FOLDER, f"{selected_band}.tif")
        convert_to_cog(band_output_tiff, f"{selected_band}_band_{i}")

def convert_to_cog(input_tiff, output_prefix):
    """Converts a GeoTIFF file to a Cloud Optimized GeoTIFF (COG)."""
    cog_output_tiff = os.path.join(TEMP_FOLDER, f"{output_prefix}_COG.tif")
    result = subprocess.run([
        'gdal_translate',
        '-of', 'COG',
        input_tiff,
        cog_output_tiff
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")  # Debug print
        raise RuntimeError(f"Error converting to COG: {result.stderr}")
    print(f"COG created: {cog_output_tiff}")
    return cog_output_tiff

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process an HDF5 file and convert selected band to COG")
    parser.add_argument('file_path', type=str, help="Path to the HDF5 file")
    parser.add_argument('band_name', type=str, help="Name of the band to convert to COG", nargs='?', default=None)

    args = parser.parse_args()
    file_path = args.file_path
    selected_band = args.band_name

    cog_output_tiff = process_hdf5(file_path, selected_band)
    print(f"COG output file: {cog_output_tiff}")
