# Tabs

Se presenta el código para el pivot en python y sql server

=== "Python"

    ``` py
    import pandas as pd
    import polars as pl
    df_pivotada = df.pivot_table(index="año", columns="producto", values="ventas", fill_value=0)
    df_pivotada
    ```

=== "SQL Server"

    ``` sql
    WITH cte_pivot AS (
    SELECT 
        año, pais,
        [Apple], [Samsung], [Linux]

    FROM (
        SELECT año, pais, producto, ventas FROM  prueba_pivot
    ) AS tabla1
    PIVOT
    (
        SUM(ventas)
        FOR producto IN ([Apple], [Samsung], [Linux])
    ) AS tabla
    )
    SELECT
        año,
        pais,
        ISNULL(Apple, 0) AS Apple,
        ISNULL(Samsung, 0) AS Samsung, 
        ISNULL(Linux, 0) AS Linux
    FROM cte_pivot
    ORDER BY año
    ```