import argparse
from .utils import process_images_from_directory


def main():
    parser = argparse.ArgumentParser(
        description='Process images and convert to PDF.')
    parser.add_argument('-i', '--input_dir', type=str, required=True,
                        help='Directory containing images to process.')
    parser.add_argument('-o', '--output_pdf', type=str,
                        required=True, help='Path to save the output PDF.')

    args = parser.parse_args()

    process_images_from_directory(args.input_dir, args.output_pdf)


if __name__ == "__main__":
    main()
