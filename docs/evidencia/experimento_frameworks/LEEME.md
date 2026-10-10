# Experimento: la misma prueba en 4 herramientas

Desde esta carpeta (con el entorno activado y `pip install nose2 pytest hypothesis`):

```
python -m unittest test_unittest_style
python -m pytest test_pytest_style.py -q
python -m pytest test_param_pytest.py -v
python -m nose2 -v --pretty-assert test_nose2_style
python -m nose2 -v test_nose2_style            # sin el plugin: compara el mensaje
python -m pytest ../../../tests/test_properties.py -q --hypothesis-show-statistics
```

Cada archivo tiene una prueba correcta y `test_error_intencional`, que espera un resultado equivocado a propósito para
comparar el mensaje de fallo. Esa prueba debe fallar: es parte del experimento, no un error.
Salidas de referencia en `../frameworks_salidas.txt`.
