import argparse
import logging
from pathlib import Path
from shutil import copyfile
from threading import Thread

parser = argparse.ArgumentParser(description="Program for sorting files")

parser.add_argument("--source", "-src", type=str, help="Source folder", required=True)
parser.add_argument("--output", "-out", type=str, help="Output folder", default="dist")

args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))

folders = list()


def copy_files_to_folders(path: Path):
    for el in path.iterdir():
        if el.is_file():
            extension = el.suffix[1:]
            extension_folder = output / extension
            extension_folder.mkdir(parents=True, exist_ok=True)
            try:
                if not (extension_folder / el.name).exists():
                    copyfile(el, extension_folder / el.name)
                else:
                    i = 1
                    while (extension_folder / f"{el.stem}_{i}{el.suffix}").exists():
                        i += 1
                    copyfile(el, extension_folder / f"{el.stem}_{i}{el.suffix}")
            except OSError as err:
                logging.error(err)
        elif el.is_dir() and not el.is_symlink():
            copy_files_to_folders(el)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    print(f"Процес обробки теки розпочато")
    folder_for_sorting = Path(source)
    folder_to_save = Path(output)
    folders.append(folder_for_sorting)

    threads = []
    for folder in folders:
        th = Thread(target=copy_files_to_folders, args=(folder,))
        threads.append(th)
        th.start()

    [th.join() for th in threads]

    print(f"Файли відсортовано і скопійовано в теку '{output}'\n"
          f"Стара тека '{source}' може бути видалена.")
