"""
CLI Entry Point untuk testing model.

Usage:
    python -m app.core.model.main <path/to/gambar.jpg>

Contoh:
    python -m app.core.model.main test_images/sehat.jpg
    python -m app.core.model.main test_images/early_blight.jpg
"""

import sys
import json

from app.core.model.pipeline import predict


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.core.model.main <path/to/image>")
        print("Contoh: python -m app.core.model.main daun.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        result = predict(image_path)
        print(json.dumps(result, indent=2))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error saat prediksi: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
