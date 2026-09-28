import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main():
    parser = argparse.ArgumentParser(description="Gera o pacote de deploy sem banco ou credenciais locais.")
    parser.add_argument("--output", default="app.zip", help="Arquivo ZIP de destino (padrão: app.zip).")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    paths = [root / "manage.py", root / "Procfile", root / "requirements.txt"]
    paths.extend((root / ".ebextensions").glob("*.config"))
    for folder in ("lavouraInteligente_JG", "lavouras"):
        paths.extend(
            p for p in (root / folder).rglob("*.py")
            if "__pycache__" not in p.parts and p.name != "tests.py" and "tests" not in p.parts
        )
    output = root / args.output
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in sorted(set(paths)):
            archive.write(path, path.relative_to(root).as_posix())
    print(f"ZIP criado: {output} ({len(paths)} arquivos)")


if __name__ == "__main__":
    main()
