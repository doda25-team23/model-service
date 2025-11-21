import os
from urllib.request import urlretrieve

MODEL_DIR = os.environ.get("MODEL_DIR", "/models")
MODEL_VERSION = os.environ.get("MODEL_VERSION")
MODEL_BASE_URL = os.environ.get("MODEL_BASE_URL")

FILE = "model.joblib"


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    dest = os.path.join(MODEL_DIR, FILE)

    # If cached, do nothing
    if os.path.exists(dest):
        print(f"{dest} already exists, skipping download.")
        return

    # If variables missing, skip gracefully
    if not MODEL_VERSION or not MODEL_BASE_URL:
        print("MODEL_VERSION or MODEL_BASE_URL not set. Skipping download.")
        return

    url = f"{MODEL_BASE_URL}/{MODEL_VERSION}/{FILE}"
    print(f"Downloading {url} -> {dest}")

    urlretrieve(url, dest)


if __name__ == "__main__":
    main()
