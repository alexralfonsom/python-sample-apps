Si quieres automatizarlo por carpeta con parámetros --input y --output, aquí tienes un script listo para usar (usa PyPDF2/pypdf). Guarda esto como merge_mt.py y ejecútalo

```
python merge_mt.py --input "RUTA/DE/ENTRADA" --output "RUTA/DE/SALIDA"
```

Notas y decisiones clave
*	Patrones de nombre: el script detecta exactamente "<numero>  S.pdf" (uno o más espacios antes de S) y "<numero>.pdf". Si varía, dime y lo ajustamos.
*	Orden garantizado: siempre concatena primero el archivo con S y luego el “normal”, como pediste.
*   Salida: MT-{numero}.pdf (ej. MT-17026447.pdf) en la carpeta --output.
*	Dependencia: instala pypdf (o PyPDF2): pip install pypdf.

```python
python3 merge_mt_check.py --input "C:\Reportes" --output "C:\Reportes\Final"
```
