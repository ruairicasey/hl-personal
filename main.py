from src.client import get_info


def main():
    info = get_info()
    meta = info.meta()
    print(f"Connected. Universe has {len(meta['universe'])} assets.")


if __name__ == "__main__":
    main()
