import os
import subprocess
import h5py
import numpy as np
import rasterio
from rasterio.transform import from_origin

def process_hdf5(file_path, selected_band=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' not found")

    with h5py.File(file_path, 'r') as hdf:
        available_bands = [band for band in hdf.keys()]
        print(f"Available bands: {', '.join(available_bands)}")

        if not selected_band:
            selected_band = input(f"Enter the band name to convert to COG from the above list: ")

        if selected_band not in available_bands:
            raise ValueError(f"Band '{selected_band}' not found in the available bands")

        dataset = hdf[selected_band][:]
        print(f"Debug: Dataset shape = {dataset.shape}")  # Debug print

        # Example geotransform values, replace with actual values if available
        geotransform = (0, 1, 0, 0, 0, -1)
        print(f"Debug: Geotransform = {geotransform}")  # Debug print
        

        top_left_x = geotransform[0]
        top_left_y = geotransform[3]
        pixel_width = geotransform[1]
        pixel_height = geotransform[5]
        pixel_size = np.sqrt(pixel_width**2 + pixel_height**2)
        print(f"Debug: Calculated pixel_size = {pixel_size}") 
        output_tiff = os.path.normpath(f"./temp/{selected_band}.tif")
        cog_output_tiff = os.path.normpath(f"./temp/{selected_band}_COG.tif")

        if len(dataset.shape) == 2:
            with rasterio.open(output_tiff, 'w', driver='GTiff', height=dataset.shape[0], width=dataset.shape[1], 
                               count=1, dtype=dataset.dtype, crs='+proj=latlong', 
                               transform=from_origin(top_left_x, top_left_y, pixel_size, pixel_size)) as dst:
                dst.write(dataset, 1)
        elif len(dataset.shape) == 3:
            print("Debug: Processing 3D data")  # Debug print
            for i in range(dataset.shape[0]):
                band_data = dataset[i, :, :]
                band_output_tiff = os.path.normpath(f"./temp/{selected_band}_band_{i}.tif")
                with rasterio.open(band_output_tiff, 'w', driver='GTiff', height=band_data.shape[0], width=band_data.shape[1], 
                                   count=1, dtype=band_data.dtype, crs='+proj=latlong', 
                                   transform=from_origin(top_left_x, top_left_y, pixel_size, pixel_size)) as dst:
                    dst.write(band_data, 1)
                cog_output_tiff = os.path.normpath(f"./temp/{selected_band}band{i}_COG.tif")
                cog_band_output_tiff = os.path.normpath(f"./temp/{selected_band}_band_{i}_COG.tif")
                result = subprocess.run([
                    'gdal_translate',
                    '-of', 'COG',
                    band_output_tiff,
                    cog_band_output_tiff
                ], capture_output=True, text=True)
                if result.returncode != 0:
                    raise RuntimeError(f"Error converting to COG: {result.stderr}")
                print(f"COG for {selected_band} band {i} created: {cog_band_output_tiff}")
        else:
            raise ValueError(f"Unsupported data shape for {selected_band}: {dataset.shape}")

        # Convert to COG (for 2D data or last band of 3D data)
        cog_output_tiff = os.path.normpath(f"./temp/{selected_band}_COG.tif")
        result = subprocess.run([
            'gdal_translate',
            '-of', 'COG',
            output_tiff,
            cog_output_tiff
        ], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Error converting to COG: {result.stderr}")
        print(f"COG created: {cog_output_tiff}")

        return cog_output_tiff

if __name__ == "_main_":
    import argparse

    parser = argparse.ArgumentParser(description="Process an HDF5 file and convert selected band to COG")
    parser.add_argument('file_path', type=str, help="Path to the HDF5 file")
    parser.add_argument('band_name', type=str, help="Name of the band to convert to COG", nargs='?', default=None)

    args = parser.parse_args()
    file_path = args.file_path
    selected_band = args.band_name

    cog_output_tiff = process_hdf5(file_path, selected_band)
    print(f"COG output file: {cog_output_tiff}")
    print(f"COG output file: {cog_output_tiff}")
