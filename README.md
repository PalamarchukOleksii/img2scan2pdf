# img2scan2pdf

`img2scan2pdf` is a Command-Line Interface (CLI) tool that processes images and converts them into a single PDF. The tool performs automatic document detection and enhancement to ensure high-quality output, making it ideal for scanning documents.

## Features

- **Automatic Document Detection**: Identifies and extracts document regions from images.
- **Perspective Correction**: Fixes skewed or angled documents.
- **PDF Conversion**: Converts processed images into a single PDF.
- **A4 Sizing**: Resizes documents to fit standard A4 dimensions with optional padding.

## Installation

Install `img2scan2pdf` using `pip`:

```bash
pip install img2scan2pdf
```

## Usage

The tool can be run directly from the command line. Specify the input directory containing images and the output PDF file path.

```bash
img2scan2pdf -i <input_directory> -o <output_pdf_path>
```

### Arguments

- `-i`, `--input_dir`: Path to the directory containing images to process. Supported formats are `.png`, `.jpg`, and `.jpeg`.
- `-o`, `--output_pdf`: Path to save the resulting PDF file.

### Example

```bash
img2scan2pdf -i ./scanned_images -o ./output/document.pdf
```

This command processes all images in the `./scanned_images` directory and saves the resulting PDF as `./output/document.pdf`.

## Development

### Cloning the Repository

Clone the repository:

```bash
git clone https://github.com/yourusername/img2scan2pdf.git
cd img2scan2pdf
```

### Installing Dependencies

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### Running Locally

Run the tool locally:

```bash
python -m img2scan2pdf.cli -i <input_directory> -o <output_pdf_path>
```

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to suggest improvements or report bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This tool uses the following libraries:

- [NumPy](https://numpy.org/)
- [OpenCV](https://opencv.org/)
- [Pillow](https://python-pillow.org/)
