## Definición

La **reestructuración de datos** es el proceso de cambiar de forma un conjunto de datos un mejor entendimiento o facilidad en el análisis. Es la reorganización de los datos sin alterar su información escencial.

## Pivot
Es el poder pasar un conjunto de dato **Long Form** a **Wide Form**, esto se logra mediante tres puntos claves. Se tiene una o varias **columnas fijas** que se mantendrán, otra columna que será el **pivote** (sus valores se convertirán en columnas), y una tercera columna que es numérica (puede también no ser numérica) el cual se le aplicará una **función de agregación** (1) para cuando se tenga datos duplicados respecto a la columna fija y la de pivote.
{.annotate}

1. SUM(), COUNT(), MAX(), MEAN(), etc.

### Sintáxis

=== "Pandas"

    ```py
    # .pivot
    dataframe.pivot(
        index=<no_default>, # Columna(s) fija(s) que se convertirá en un índice
        columns=<no_default>, # Columna para el pivote
        values=<no_default> # Columna numérica o no numérica
        )

    # .pivot_table
    Dataframe.pivot_table(
        index=<no_default>, # Columna(s) fija(s) que se convertirá en un índice
        columns=<no_default>, # Columna para el pivote
        values=<no_default>, # Columna obligatoriamente numérica
        aggfunc="mean", # Función de agregación, por defecto es `mean`
        fill_value=None # Rellenar los valores NaN
        )
    ```

=== "Polars"

    ```py
    DataFrame.pivot(
        on=<no_default>,  # Columna para el pivote
        index=<no_default>, # Columna(s) fija(s)
        values=<no_default>, # Columna numérica o no numérica
        aggregate_function=<no_default> # Función de agregación
        )
    ```
=== "SQL Server"

    ```sql
    SELECT 
    'columna_fija',
    [val1], [val2], [valn]  -- Valores distintos de la columna pivot

    FROM (
        SELECT 'columna_fija', 'columna_pivot', 'valor' FROM  tabla_original
    ) AS tabla_intermedia
    PIVOT
    (
        aggfunc('valor')
        FOR 'columna_pivot' IN ([val1], [val2], [valn])
    ) AS tabla_pivoteada
    ```


!!! Note "Index en Pandas"
    Pandas convierte columnas en índices al pivotear ya que permite representar una estructura jerárquica de los datos, además de optimizar las operaciones de selección y agrupamiento; esto también se cumple con los métodos `groupby()` y `set_index()`. Para convertir un índice en una columna se utiliza `reset_index()`.
    ``

### Ejemplo
Tenemos los siguientes datos:

|producto |pais      |año   |ventas|
|---------|----------|------|------|         
|   Apple | Colombia | 2016 | 1000 |
|   Apple |     Perú | 2017 |  800 |
|   Apple |  Ecuador | 2018 |  600 |
| Samsung | Colombia | 2019 | 1200 |
| Samsung |     Perú | 2020 |  900 |
| Samsung |  Ecuador | 2021 |  700 |
|   Linux | Colombia | 2022 | 1100 |
|   Linux |     Perú | 2023 |  850 |
|   Linux |  Ecuador | 2024 |  650 |

!!! example "Pivot"
    Se quiere tener una nueva tabla que se muestre el tipo la venta que se origina en cada país por cada producto.
    === "Pandas"

        ```py
        import pandas as pd

        df=pd.Dataframe(data)
        
        df.pivot(index="pais", columns="producto", values="ventas") #(1)!
        ```

        1. `pais` ya no es una columna, es un índice.

        |  **pais**   | Apple|Linux|Samsung| 
        |---------|------|------|------|
        |**Colombia** | 1000 | 1100 | 1200 |
        |**Ecuador**  |  600 |  650 |  700 |
        |**Perú**     |  800 |  850 |  900 |

    === "Polars"

        ```py
        import polars as pl
        dl=pl.DataFrame(data)

        dl.pivot("producto", index="pais", values="ventas")
        ```

        |  Pais   | Apple|Samsung|Linux| 
        |---------|------|------|------|
        |Colombia | 1000 | 1200 | 1100 |
        |Perú     |  800 |  900 |  850 |
        |Ecuador  |  600 |  700 |  650 |

    === "SQL Server"

        ```sql
        SELECT pais,
            [Apple], [Samsung], [Linux]
        FROM 
        (
            SELECT pais, producto, ventas FROM prueba_pivot
        ) AS tabla1
        PIVOT 
        (
            SUM(ventas)
            FOR producto IN ([Apple], [Samsung], [Linux])
        ) AS tabla_resumen
        ```

        | pais     | Apple   | Samsung  | Linux   |
        |----------|---------|----------|---------|
        | Colombia | 1000.00 | 1200.00  | 1100.00 |
        | Ecuador  | 600.00  | 700.00   | 650.00  |
        | Peru     | 800.00  | 900.00   | 850.00  |

---

## Unpivot
Es lo inverso a Pivot, transforma columnas en filas, si se tiene una tabla que pasó por una transformación Pivot y este realizó una operación de agregación, no es posible obtener la misma tabla original mediante Unpivot. No trabaja con valores `NULL`, estos son eliminados al realizar Unpivot.

### Sintáxis

=== "Pandas"

    ```py
    # .melt
    dataframe.melt(
        id_vars=None, #(1)! 
        value_vars=None, #(2)!
        var_name=None #(3)!
        value_name=None #(4)!
        )
    ```

    1. Columna para identificar las variables (columna fija)
    2. Las columnas que serán convertidos a filas (columna pivotada)
    3. Nombre de la nueva columna que contendrá a `value_var`
    4. Nombre de la columna que contendrá los valores (columna values)

=== "Polars"

    ```py
    DataFrame.unpivot(
        on=None,  #(1)!  
        index=None, #(2)!  
        variable_name=None, #(3)!  
        value_name=None #(4)!  
        )
    ```

    1. Las columnas que serán convertidos a filas (columna pivotada)
    2. Columna para identificar las variables (columna fija)
    3. Nombre de la nueva columna que contendrá a `on`
    4. Nombre de la columna que contendrá los valores (columna values)

=== "SQL Server"

    ```sql
    SELECT 
        'columna_fija', 
        'nombre_columna_pivotada', --(1)!
        'nombre_columna_values' --(2)!
    FROM 
    (
        SELECT 'columna_fija', [col1], [col2], [coln] FROM  tabla_original
    ) AS tabla_intermedia
    PIVOT
    (
        'nombre_columna_values'
        FOR 'nombre_columna_pivotada' IN ([col1], [col2], [coln]) --(3)!
    ) AS tabla_unpivot
    ```

    1. Es la columna que contendrá a las columnas que van a ser convertidas en filas.
    2. Es la columna que contendrá los valores numérico o no-numéricos.
    3. Estas son las columnas que serán convertidas a filas.

### Ejemplo

!!! example "Unpivot"
    De la tabla que se obtuvo del ejemplo anterior, se quiere obtener la tabla original.

    === "Pandas"

        ```py
        # .melt
        df_pivot = df_pivot.reset_index() #(1)!
        df_pivot.melt(
            id_vars="pais",
            value_vars=["Apple", "Linux", "Samsung"],
            var_name="Producto"
            value_name="Ventas"
            )
        ```

        1. Como se mencionó antes, **Pandas** requiere de índices por lo que cuando se aplica un `.pivot()` la columna fija se convierte en un índice, pero cuando queremos hacer `.unpivot()` al resultado de un `.pivot()` se necesita trabajar con columnas, por lo que se debe aplicar `.reset_index()` al resultado del pivote.

        |      |  pais    | Producto | Ventas |
        |:----:|----------|----------|--------|
        |**0** | Colombia |    Apple |   1000 |
        |**1** |  Ecuador |    Apple |    600 | 
        |**2** |     Perú |    Apple |    800 | 
        |**3** | Colombia |    Linux |   1100 |
        |**4** |  Ecuador |    Linux |    650 | 
        |**5** |     Perú |    Linux |    850 | 
        |**6** | Colombia |  Samsung |   1200 | 
        |**7** |  Ecuador |  Samsung |    700 | 
        |**8** |     Perú |  Samsung |    900 | 


    === "Polars"

        ```py
        dl_pivot.unpivot(
            on=["Apple", "Linux", "Samsung"],
            index="pais",
            variable_name="Producto",
            value_name="Ventas"
            )
        ```


        | pais     | Producto | Ventas |
        |----------|----------|--------|
        | `str`    | `str`    | `i64`  |
        | Colombia | Apple    | 1000   |
        | Perú     | Apple    | 800    |
        | Ecuador  | Apple    | 600    |
        | Colombia | Linux    | 1100   |
        | Perú     | Linux    | 850    |
        | Ecuador  | Linux    | 650    |
        | Colombia | Samsung  | 1200   |
        | Perú     | Samsung  | 900    |
        | Ecuador  | Samsung  | 700    |

    === "SQL Server"

        ```sql
            SELECT 
                pais,
                producto,
                ventas
            FROM 
            (
                SELECT pais, [Apple], [Samsung], [Linux] FROM #tabla_pivotada --(1)!
            ) AS TablaFuente
            UNPIVOT
            (
                ventas
                FOR producto IN ([Apple], [Samsung], [Linux])
            ) AS tabla_unpivot
        ```
        
        1. `#tabla_pivotada` es una tabla temporal que almacena el resultado de la consulta del pivote.

        | pais      | producto  | ventas  |    
        |-----------|-----------|---------|
        | Colombia  | Apple     | 1000.00 |  
        | Colombia  | Samsung   | 1200.00 |  
        | Colombia  | Linux     | 1100.00 |  
        | Ecuador   | Apple     | 600.00  |  
        | Ecuador   | Samsung   | 700.00  |  
        | Ecuador   | Linux     | 650.00  |
        | Peru      | Apple     | 800.00  |  
        | Peru      | Samsung   | 900.00  |   
        | Peru      | Linux     | 850.00  |
