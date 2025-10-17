#!/usr/bin/env python3
import argparse, re
from pathlib import Path
from datetime import datetime

try:
    from PyPDF2 import PdfMerger, PdfReader
except Exception as e:
    raise SystemExit("Este script requiere PyPDF2 o pypdf. Instala con: pip install pypdf") from e

RX_PLAIN = re.compile(r"^(\d+)\.pdf$", re.IGNORECASE)
RX_S     = re.compile(r"^(\d+)\s+S\.pdf$", re.IGNORECASE)

def find_pairs(input_dir: Path):
    plain, sfiles = {}, {}
    for p in input_dir.glob("*.pdf"):
        if m := RX_PLAIN.match(p.name):
            plain[m.group(1)] = p
        elif m := RX_S.match(p.name):
            sfiles[m.group(1)] = p
    # Identifica los pares completos y faltantes
    all_ids = set(plain.keys()) | set(sfiles.keys())
    pairs, missing = {}, {}
    for num in all_ids:
        s_path = sfiles.get(num)
        p_path = plain.get(num)
        if s_path and p_path:
            pairs[num] = (s_path, p_path)
        else:
            missing[num] = {
                "S.pdf": bool(s_path),
                "normal.pdf": bool(p_path)
            }
    return pairs, missing

def merge_pair(s_first: Path, second: Path, out_path: Path):
    merger = PdfMerger(strict=False)
    with s_first.open("rb") as f1:
        merger.append(PdfReader(f1))
    with second.open("rb") as f2:
        merger.append(PdfReader(f2))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as fo:
        merger.write(fo)
    merger.close()

def main():
    ap = argparse.ArgumentParser(description="Unifica pares '<num>  S.pdf' + '<num>.pdf' -> 'MT-<num>.pdf'")
    ap.add_argument("--input",  required=True, help="Carpeta a analizar con PDFs de entrada")
    ap.add_argument("--output", required=True, help="Carpeta de salida para los PDFs resultantes")
    args = ap.parse_args()

    in_dir  = Path(args.input).expanduser().resolve()
    out_dir = Path(args.output).expanduser().resolve()

    pairs, missing = find_pairs(in_dir)

    print("\n=== ARCHIVOS ENCONTRADOS ===")
    for base, (s_path, p_path) in pairs.items():
        print(f"✔ {base} → {s_path.name} + {p_path.name}")

    if missing:
        print("\n=== ARCHIVOS INCOMPLETOS ===")
        for base, info in missing.items():
            s_ok = "✔" if info["S.pdf"] else "✗"
            p_ok = "✔" if info["normal.pdf"] else "✗"
            print(f"{base}: S.pdf[{s_ok}]  normal.pdf[{p_ok}]")

    print("\n=== PROCESANDO UNIONES ===")
    for base, (s_path, p_path) in pairs.items():
        out_path = out_dir / f"MT-{base}.pdf"
        merge_pair(s_path, p_path, out_path)
        print(f"✅ Generado: {out_path}")

    if not pairs:
        print("\n⚠ No se encontraron pares completos para unir.")
    else:
        print(f"\n✅ Proceso finalizado. Archivos creados en: {out_dir}")

    # Generar reporte.txt
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "reporte.txt"
    with report_path.open("w", encoding="utf-8") as report_file:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_file.write(f"Reporte generado: {now_str}\n\n")

        report_file.write("=== ARCHIVOS ENCONTRADOS ===\n")
        for base, (s_path, p_path) in pairs.items():
            report_file.write(f"✔ {base} → {s_path.name} + {p_path.name}\n")

        report_file.write("\n=== ARCHIVOS INCOMPLETOS ===\n")
        if missing:
            for base, info in missing.items():
                s_ok = "✔" if info["S.pdf"] else "✗"
                p_ok = "✔" if info["normal.pdf"] else "✗"
                report_file.write(f"{base}: S.pdf[{s_ok}]  normal.pdf[{p_ok}]\n")
        else:
            report_file.write("No hay archivos incompletos.\n")

        report_file.write("\n=== RESUMEN ===\n")
        if not pairs:
            report_file.write("⚠ No se encontraron pares completos para unir.\n")
        else:
            report_file.write(f"Archivos generados: {len(pairs)}\n")
            report_file.write(f"Ruta de salida: {out_dir}\n")

if __name__ == "__main__":
    main()