## Definición

La **reestructuración de datos** es el proceso de cambiar de forma un conjunto de datos un mejor entendimiento o facilidad en el análisis. Es la reorganización de los datos sin alterar su información escencial.

## Pivot
Es el poder pasar un conjunto de dato **Long Form** a **Wide Form**, esto se logra mediante tres puntos claves. Se tiene una o varias **columnas fijas** que se mantendrán, otra columna que será el **pivote** (sus valores se convertirán en columnas), y una tercera columna que es numérica (puede también no ser numérica) el cual se le aplicará una **función de agregación** (1) para cuando se tenga datos duplicados respecto a la columna fija y la de pivote.
{.annotate}

1. SUM(), COUNT(), MAX(), MEAN(), etc.

### Sintáxis

=== "Pandas"

    ```py
    # .pivot #(10)
    dataframe.pivot(
        index=<no_default>, #(1)! 
        columns=<no_default>, #(2)! 
        values=<no_default> #(3)! 
        )

    # .pivot_table #(4)
    Dataframe.pivot_table( 
        index=<no_default>, #(5)! 
        columns=<no_default>, #(6)! 
        values=<no_default>, #(7)! 
        aggfunc="mean", #(8)! 
        fill_value=None #(9)! 
        )
    ```

    1. Columna(s) fija(s) que se convertirá en un índice
    2. Columna para el pivote
    3. Columna numérica o no numérica
    4. `.pivot_table` se utiliza cuando queremos aplicar una función de agregación, a diferencia de `.pivot` que no realiza ninguna cálculo de los valores.
    5. Columna(s) fija(s) que se convertirá en un índice
    6. Columna para el pivote
    7. Columna obligatoriamente numérica
    8. Función de agregación, por defecto es `mean`
    9. Rellenar los valores `NaN`
    10. Este método permite realizar pivot donde la columna `values` puede ser numérica y no-numérica.


=== "Polars"

    ```py
    DataFrame.pivot(
        on=<no_default>,  #(1)!
        index=<no_default>, #(2)!
        values=<no_default>, #(3)!
        aggregate_function=<no_default> #(4)!
        )
    ```

    1. Columna para el pivote.
    2. Columna(s) fija(s).
    3. Columna numérica o no numérica.
    4. Función de agregación.

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

### Ejemplos
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
        
        df_pivot = df.pivot(index="pais", columns="producto", values="ventas") #(1)!
        print(df_pivot)
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

        dl_pivot = dl.pivot("producto", index="pais", values="ventas")
        print(dl_pivot)
        ```

        |  pais   | Apple|Samsung|Linux| 
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

### Ejemplos

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

## Group by

Es la agrupación de datos basado en una o más columnas y calcular métricas resumidas mediante una función de agregación.
El uso del `groupby` tiene tres finalidades los cuales son:
* Agregación
* Transformación
* Filtro

Pudiendo ser útil en una fase inicial del análisis exploratorio hasta un análisis avanzado.

Tenemos que saber cuando aplicamos solo `.groupby("column_name)` en Python, lo que hacemos es agrupar toda la tabla a través de su columna

### Agregación
Permite calcular estadísitcas resumidas (suma, promedio, conteo,  máximo, etc.) para cada grupo.

#### Sintáxis


=== "Pandas"

    ```py

    dataframe.groupby('column')['value'].sum()  #(1)!
    dataframe.groupby('column')['value'].agg(func, engine) #(2)!
    ```

    1. `sum()` es una de las funciones de agregación, pero pueden ser otras: `mean()`, `max()`, `count()` etc.
    2. * `func` hace referencia a funciones de agregación o funciones propias.
        * `engine` hace referenia a el uso del motor de cálculo, puedo ser **cpython** o **numba**, por defecto se elige la más óptima (cpython).

=== "Polars"

    ```py
    dataframe.group_by('column', maintain_order=False).agg
                (
                pl.col('values').aggfunc() | pl.aggfunc('values')
                ) #(1)!
    ```

    1. En Polars solo hay una forma de hacer un groupby, es mediante el método `agg()`, hay dos formas de llamar a sus argumentos:

        * `pl.col('values').aggfunc()`: Se indica la columna `values` y se le aplica una función de transformación (`sum()`, mean()`, `max()`, `len(), etc.)
        * `pl.aggfunc('values')`: Este es más corto, se llama a la función de agregación indicando a la columna.
        
        !!! success "Diferencias"
            La principal diferencia entre ambas formas es que la primera (`pl.col('values').aggfunc()`) permite realizar una transformación previa a aplicar una transformación de agregación, un pequeño ejemplo sería `#!py DataFrame.groupby('cliente').agg((pl.col('costo')*1.18).pl.sum())`
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

#### Ejemplos

Para estos ejemplos se utilizará la tabla siguiente, que indica las deudas de los clientes.

| cliente | producto  | monto     | estado_mora | periodo |
|---------|-----------|-----------|-------------|---------|
| C001    | Prestamo  | 15000.00  | Al dia      | 2023-Q1 |
| C002    | Tarjeta   | 2000.00   | En mora     | 2023-Q1 |
| C003    | Prestamo  | 12000.00  | Al dia      | 2023-Q1 |
| C001    | Tarjeta   | 2500.00   | Al dia      | 2023-Q2 |
| C004    | Prestamo  | 18000.00  | En mora     | 2023-Q2 | 
| C005    | Tarjeta   | 3000.00   | Al dia      | 2023-Q2 | 
| C002    | Prestamo  | 10000.00  | En mora     | 2023-Q3 |
| C003    | Tarjeta   | 4000.00   | En mora     | 2023-Q3 |
| C004    | Prestamo  | 15000.00  | Al dia      | 2023-Q3 |
| C005    | Prestamo  | 22000.00  | En mora     | 2023-Q4 |

!!! example "Ejemplos de uso de función de agregación"

    === "Pandas"

        ```py
        df.groupby("cliente")["monto"].sum().reset_index() #(1)!

        df.groupby("cliente")["monto"].agg(["sum", "mean"]).reset_index() #(2)!

        df.groupby("cliente").agg({
            "monto": ["sum", "mean", "count"]
            }).reset_index() #(3)!

        df.groupby("cliente")["monto"].agg(
                [
                    ("Calculos", ["sum", "mean"]),
                    ("Cantidad Total", "count")
                 ]) #(4)!
        ```

        1. Calculo simple, se reseta el índice (cliente) para que sea una columna

            |   | cliente | monto |
            |---|---------|-------|
            | 0 | C001    | 17500 |
            | 1 | C002    | 12000 |
            | 2 | C003    | 16000 |
            | 3 | C004    | 33000 |
            | 4 | C005    | 25000 |
        2. Múltiples cálculos

            |   |cliente | sum   | mean    |
            |---|--------|-------|---------|
            | 0 |C001    | 17500 | 8750.0  |
            | 1 |C002    | 12000 | 6000.0  |
            | 2 |C003    | 16000 | 8000.0  |
            | 3 |C004    | 33000 | 16500.0 |
            | 4 |C005    | 25000 | 12500.0 |

        3. Cálculos múltiples, pero reserva el nombre de la columna a la cual se le aplica la agregación, en este caso es "monto".

            <style>
                table {
                width: 100%;
                border-collapse: collapse;
                }
                th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: center;
                }
                th {
                    font-weight: bold;
                }
                /* Clase para centrar texto */
                .centrar-texto {
                text-align: center;
                }
            </style>

            <table>
                <thead>
                    <tr>
                    <th rowspan="2">cliente</th>
                    <th colspan="3" class="centrar-texto">monto</th>
                    </tr>
                    <tr>
                    <th>sum</th>
                    <th>mean</th>
                    <th>count</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>C001</td>
                    <td>17500</td>
                    <td>8750.0</td>
                    <td>2</td>
                    </tr>
                    <tr>
                    <td>C002</td>
                    <td>12000</td>
                    <td>6000.0</td>
                    <td>2</td>
                    </tr>
                    <tr>
                    <td>C003</td>
                    <td>16000</td>
                    <td>8000.0</td>
                    <td>2</td>
                    </tr>
                    <tr>
                    <td>C004</td>
                    <td>33000</td>
                    <td>16500.0</td>
                    <td>2</td>
                    </tr>
                    <tr>
                    <td>C005</td>
                    <td>25000</td>
                    <td>12500.0</td>
                    <td>2</td>
                    </tr>
                </tbody>
            </table>

        4. En este caso, se indica primero la columna y luego podemos darle un "alias" a las columnas nuevas.

            <table>
                <thead>
                    <tr>
                    <th rowspan="2">cliente</th>
                    <th colspan="2">Calculos</th>
                    <th colspan="1">Cantidad Total</th>
                    </tr>
                    <tr>
                    <th class="centrar-texto">sum</th>
                    <th class="centrar-texto">mean</th>
                    <th class="centrar-texto">monto</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>C001</td>
                    <td class="centrar-texto">17500</td>
                    <td class="centrar-texto">8750.0</td>
                    <td class="centrar-texto">2</td>
                    </tr>
                    <tr>
                    <td>C002</td>
                    <td class="centrar-texto">12000</td>
                    <td class="centrar-texto">6000.0</td>
                    <td class="centrar-texto">2</td>
                    </tr>
                    <tr>
                    <td>C003</td>
                    <td class="centrar-texto">16000</td>
                    <td class="centrar-texto">8000.0</td>
                    <td class="centrar-texto">2</td>
                    </tr>
                    <tr>
                    <td>C004</td>
                    <td class="centrar-texto">33000</td>
                    <td class="centrar-texto">16500.0</td>
                    <td class="centrar-texto">2</td>
                    </tr>
                    <tr>
                    <td>C005</td>
                    <td class="centrar-texto">25000</td>
                    <td class="centrar-texto">12500.0</td>
                    <td class="centrar-texto">2</td>
                    </tr>
                </tbody>
            </table>

    === "Polars"

        ```py
            dl.group_by("cliente", maintain_order=True).agg([
                pl.col("monto").sum().alias("Monto total"), 
                pl.col("monto").mean().alias("Monto promedio")
            ]) #(1)!
        ```

        1. Podemos ver la gran facilidad de realizar un `group_by` a diferencia de pandas.

            |cliente|  Monto|  total Monto promedio  |
            |-------|-------|------------------------|
            |  str  | i64   |  f64                   |
            |"C001" | 17500 | 8750.0                 |
            |"C002" | 12000 | 6000.0                 |
            |"C003" | 16000 | 8000.0                 |
            |"C004" | 33000 | 16500.0                |
            |"C005" | 25000 | 12500.0                |

    === "SQL Server"

        ```sql
            SELECT 
                cliente,
                SUM(monto) AS 'Monto Total',
                AVG(monto) AS 'Monto Promedio'
            FROM historial_crediticio
            GROUP BY cliente; --(1)!
        ```

        1. Si bien en SQL no es obligatorio poner alias a las columnas, es una buena práctica. Se puede también notar su fácil declaración.

            | cliente | Monto Total | Monto Promedio  |  
            |---------|-------------|-----------------|
            | C001    | 17500.00    | 8750.00         |
            | C002    | 12000.00    | 6000.00         |                  
            | C003    | 16000.00    | 8000.00         |                  
            | C004    | 33000.00    | 16500.00        |      
            | C005    | 25000.00    | 12500.00        |                      

!!! success "Importante"
    En **Polars** es **obligatorio colocar las alias de las nuevas columnas de agregación** cuando se aplica a una misma columna (valor), si no se coloca se obtiene un error `DuplicateError`


### Transformación

En transformación se aplica funciones sobre cada grupo, devolviendo un objeto del mismo tamaña de la tabla original (sin agrupar), transforma los datos pero manteniendo la estructura. Suele usarse como normalización de los datos.

#### Sintáxis

=== "Pandas"

    ```py
    DataFrame.groupby('column')['value'].transform(func) #(1)!
    ```

    1. `func` hace referencia a una función de agregación (`"sum", "mean"`, "count", etc.) o una función personalizada (`lambda`). La evaluación para cada grupo y ese valor es asignado a cada uno de las filas que corresponde (tabla original sin agrupar) a cada grupo.

=== "Polars"

    ```py
    DataFrame.with_columns(
        (
            pl.col("value")/pl.col("value").sum().over("column")
        ).alias("nombre_nuevo")
    ) #(1)!
    ```

    1. En **Polars** no se requiere el uso de funciones `lambda`, aprovecha que su diseño de basa en vectores y usa operaciones expresivas, es más óptimo.
        * `with_columnas()`: Este método devuelve el dataframe con columna modificada o una nueva columna, evalúa todas las filas al mismo tiempo (recuerda que está basada en vectores).
        * `pl.col("value")`: Se hace referencia a la columna "value", puede haber varios `pl.col()` utilizando otras columnas para realizar una transformación.
        * `over()`: Over aplica operaciones calculadas sobre grupos directamente a las filas correspondiente al dataframe original.
        * `pl.col("value").sum().over("column")`: La operación se realiza en una columna, se optiene la suma de cada grupo, recuerda que no necesariamente es `sum()`, puede ser también `mean()`, `max()`, etc.
        * `alias("nombre_nuevo")`: Se **usa `alias()`siempre y cuando querramos agregar una nueva columna** con los valores calculas, si queremos modificar la columna en que hemos trabajdo, no es necesario.

=== "SQL Server"

    ```sql
    --------------------------WINDOW FUNCTIONS---------------------------
    SELECT 
        column,
        value,
        aggfunc(value) OVER (PARTITION BY column) AS 'column_name'
    FROM table_name; --(1)!
    GO

    --------------------------------JOIN---------------------------------
    SELECT
        a.column,
        b.value,
        cantidad AS 'Mean'
    FROM table_name AS a
    INNER JOIN (
        SELECT
            col,
            SUM(value)/COUNT(value) AS 'cantidad'
        FROM table_name
        GROUP BY col
    ) AS b
    ON a.column=b.column; --(2)!
    GO
    ---------------------------SUBQUERY SELECT--------------------------
    SELECT
        a.column,
        b.value,
        (SELECT
            SUM(b.value)/COUNT(b.value)
        FROM table_name AS b
        WHERE a.column=b.column
        )
    FROM table_name AS a; --(3)!
    ```

    1. **Función Ventana** `OVER()`, es el más eficiente y flexible cuando se necesita realizar agregación a nivel de grupo sin perder el contexto de las filas. Puede ser la combinación de `SUM() OVER()`, `AVG() OVER()`, `RANK() OVER()`, entre otros. **Ideal para operaciones de agregación simple a dentro de grupos**.

    2. El uso de `JOIN` es muy buena opción si se combinará varias tablas o se necesita una agregación más compleja que no se puede hacer en `OVER()`, también es eficiente y flexible.

    3. Útiles en algunos casos, pero son muy costosos para grandes datos, ya que realiza la operación fila por fila porque es una **subconsulta correlacionada**.

#### Ejemplos

!!! example "Monto promedio por cada cliente"

=== "Pandas"

    ```py
    df["Monto Promedio"] = df.groupby("cliente")["monto"].transform("mean")
    df.sort_values("cliente") #(1)!

    df["Monto Promedio"] = df.groupby("cliente")["monto"].transform(
        lambda x: sum(x)/len(x)
        )
    df.sort_values("cliente") #(2)!
    ```

    1. Aquí se está creando una nueva columna llamada `Monto Promedio`, este contendrá una media de por grupo. Al final, se ordena los valores respecto a la columna `cliente`

    2. Mediante la función `lambda` se aplica una función personalizada, muy útil cuando queremos hacer una transformación compleja, al igual que el anterior caso. se calcula la media por cada grupo. Cabe recalcar que en lambda se utiliza `len()` para hallar la cantidad, es igual a `"count"` como función de agregación.

    | cliente| producto |  monto | estado_mora | periodo  | Monto Promedio|
    |:------:|:--------:|:------:|:-----------:|:--------:|:-------------:|
    | C001   | Prestamo | 15000  | Al dia      | 2023-Q1  | 8750.0        |
    | C001   | Tarjeta  | 2500   | Al dia      | 2023-Q2  | 8750.0        |
    | C002   | Tarjeta  | 2000   | En mora     | 2023-Q1  | 6000.0        |
    | C002   | Prestamo | 10000  | En mora     | 2023-Q3  | 6000.0        |
    | C003   | Prestamo | 12000  | Al dia      | 2023-Q1  | 8000.0        |
    | C003   | Tarjeta  | 4000   | En mora     | 2023-Q3  | 8000.0        |
    | C004   | Prestamo | 18000  | En mora     | 2023-Q2  | 16500.0       |
    | C004   | Prestamo | 15000  | Al dia      | 2023-Q3  | 16500.0       |
    | C005   | Tarjeta  | 3000   | Al dia      | 2023-Q2  | 12500.0       |
    | C005   | Prestamo | 22000  | En mora     | 2023-Q4  | 12500.0       |

=== "Polars"

    ```py
    dl.with_columns(
        pl.col("monto").mean().over("cliente").alias("Monto Promedio")
        ).sort("cliente") #(1)!
    ```

    1. Se calcula la media (`mean()`) sobre el grupos generados por `cliente` y se agrega una nueva columna `Monto Promedio`.

    | cliente  | producto   |  monto | estado_mora   | periodo  | Monto Promedio|
    |:--------:|:----------:|:------:|:-------------:|:--------:|:-------------:|
    |  *str*   |   *str*    |  *i64* |    *str*      |   *str*  |     *f64*     |
    | "C001"   | "Prestamo" | 15000  | "Al dia"      | 2023-Q1  | 8750.0        |
    | "C001"   | "Tarjeta"  | 2500   | "Al dia"      | 2023-Q2  | 8750.0        |
    | "C002"   | "Tarjeta"  | 2000   | "En mora"     | 2023-Q1  | 6000.0        |
    | "C002"   | "Prestamo" | 10000  | "En mora"     | 2023-Q3  | 6000.0        |
    | "C003"   | "Prestamo" | 12000  | "Al dia"      | 2023-Q1  | 8000.0        |
    | "C003"   | "Tarjeta"  | 4000   | "En mora"     | 2023-Q3  | 8000.0        |
    | "C004"   | "Prestamo" | 18000  | "En mora"     | 2023-Q2  | 16500.0       |
    | "C004"   | "Prestamo" | 15000  | "Al dia"      | 2023-Q3  | 16500.0       |
    | "C005"   | "Tarjeta"  | 3000   | "Al dia"      | 2023-Q2  | 12500.0       |
    | "C005"   | "Prestamo" | 22000  | "En mora"     | 2023-Q4  | 12500.0       |


=== "SQL Server"

    ```sql
    -- OVER
    SELECT
        cliente,
        monto,
        AVG(monto) OVER (PARTITION BY cliente
                        ) AS 'Monto Medio'
    FROM historial_crediticio

    -- JOIN
    SELECT 
        HC1.cliente,
        HC1.monto,
        HC2.cantidad AS 'Monto Promedio'
    FROM historial_crediticio HC1
    INNER JOIN (
        SELECT
            cliente,
            SUM(monto)/COUNT(monto) AS cantidad
        FROM historial_crediticio
        GROUP BY cliente
    ) HC2
    ON HC1.cliente=HC2.cliente

    -- Subquery SELECT
    SELECT
        HC1.cliente,
        HC1.monto,
        (SELECT 
            SUM(HC2.monto)/COUNT(HC2.monto)
        FROM historial_crediticio HC2
        WHERE HC2.cliente=HC1.cliente)
    FROM historial_crediticio HC1
    ORDER BY HC1.cliente;
    ```

    | cliente | monto     | Monto Medio |  
    |:-------:|:---------:|:-----------:|
    | C001 |    15000.00  | 8750.00     |
    | C001 |    2500.00   | 8750.00     |
    | C002 |    2000.00   | 6000.00     |
    | C002 |    10000.00  | 6000.00     |
    | C003 |    4000.00   | 8000.00     |
    | C003 |    12000.00  | 8000.00     |
    | C004 |    18000.00  | 16500.00    |
    | C004 |    15000.00  | 16500.00    |
    | C005 |    22000.00  | 12500.00    |
    | C005 |    3000.00   | 12500.00    |

### Filtrado


