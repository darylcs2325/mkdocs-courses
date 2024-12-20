Un ejemplo de bloques de códigos

```py title="creando_dataframes.py" hl_lines="4 5 6 7" linenums="1"
import pandas as pd
import polars as pl

data={
    "producto": ["Apple", "Apple", "Apple", "Samsung", "Samsung", "Samsung", "Linux", "Linux", "Linux"],
    "pais": ["Colombia", "Perú", "Ecuador", "Colombia", "Perú", "Ecuador", "Colombia", "Perú", "Ecuador"],
    "año": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "ventas": [1000, 800, 600, 1200, 900, 700, 1100, 850, 650]
}

df = pd.DataFrame(data)
dl = pl.DataFrame(data)
```

Lo siguente puede ser `#!sql SELECT`