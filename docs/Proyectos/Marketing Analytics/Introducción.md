## Problematica

ShopEasy, una empresa minorista en línea, enfrenta una reducción en la interacción con los clientes y las tasas de conversión a pesar de haber lanzado varias campañas de marketing en línea nuevas. Se están comunicando con usted para que los ayude a realizar un análisis detallado e identificar áreas de mejora en sus estrategias de marketing.

### Puntos claves
Estos son los puntos que se puede observar con respecto a la problemática. 

* **Reducción de la participación de los clientes**.
* **Reducción en la tasa de conversión**: Menos visitantes del sitio se convierten en clientes  de pago.
* **Altos gastos de Marketing**: Las inversiones significativas en campañas de marketing no están dando los resultados esperados.
* **Comprender la necesidad de los clientes mediante sus comentarios**.

### KPI
Medidas para realizar el análisis
* **Conversion Rate**: Mide el porcentaje de visitantes o usuarios que completan una acción deseada (compra, registro, una descarga, etc.).

$$
= \frac{\text{N° de conversiones}}{\text{N° total de visitantes}}*100\%
$$

* **Customer Engagement Rate**: Mide el nivel de interacción que tienen los clientes con la marca, ya sea en redes sociales, página web u otros canales (likes, comentarios, compartidos, aperturas de correo).
* **Average Order Value (AOV)**: Calcula el valor promedio de cada pedido realizado en tu negocio.
$$
= \frac{\text{Ingresos totales}}{\text{N° total de pedidos}}
$$
* **Customer Feedback Score**: Mide la satisfacción del cliente con la marca, productos o servicios a través de comentarios. Se centra en la opinión del cliente sobre su experiencia, medición cualitativa.

### Objetivos

**Increase Conversion Rates**:

* *Goal*: Identificar los factores que afectan la tasa de conversión y brindar recomendaciones para mejorarla.
* *Insight*: Destacar las etapas clave en las que los visitantes abandonan el sitio y sugerir mejoras para optimizar el embudo de conversión.

**Enhance Customer Engagement**:

* *Goal*: Determinar qué tipos de contenido generan la mayor participación. 
* *Insight*: Analizar los niveles de interacción con diferentes tipos de contenido de marketing para informar mejores estrategias de contenido.

**Improve Customer Feedback Scores**:

* *Goal*: Comprender los temas comunes en las reseñas de los clientes y brindar información útil.
* *Insight*: Identificar comentarios positivos y negativos recurrentes para orientar las mejoras de los productos y servicios.


### Tablas

#### Customers
Tabla con los datos de los clientes o usuarios.

|customers       |Tipo de dato   |Descripción|
|----------------|---------------|-----------|
|CustomerID      |*tinyint*      |ID del cliente|
|CustomerName    |*nvarchar(50)* |Nombre completo del cliente|
|Email           |*nvarchar(50)* |Correo del cliente|
|Gender          |*nvarchar(50)* |Género del cliente ('Female', 'Male')|            
|Age             |*tinyint*      |Edad del cliente|
|GeographyID     |*tinyint*      |ID del lugar geográfico del cliente|

#### Customer_Journey
Tabla con la navegación que realizó un cliente o usuario dentro de la página web.

|customer_journey|Tipo de dato|Descripción|
|----------------|------------|-----------|
|JourneyID       |*smallint*    |Cada ID representa una navegación diferente en el sitio web|
|CustomerID      |*tinyint*     |ID del cliente que realiza la navegación|
|ProductID       |*tinyint*     |ID del producto con que interactuó|
|VisitDate       |*date*        |Fecha de visita|
|Stage           |*nvarchar(50)*|Etapa donde realizó una acción ('HomePage', 'ProductPage', 'Checkout', 'Purchase')|
|Action          |*nvarchar(50)*|Acción que realizó|
|Duration        |*float*       |Tiempo que estuvo en la etapa (segundos)|

#### Customer_Reviews
Reseñas realizada por el usuario a un producto

|customer_reviews|Tipo de dato   |Descripción|
|----------------|---------------|-----------|
|ReviewID        |*smallint*     |ID del review|
|CustomerID      |*tinyint*      |ID del cliente que realizó la review|
|ProductID       |*tinyint*      |ID del producto en que realizó la review|
|ReviewDate      |*date*         |Fecha del review|            
|Rating          |*tinyint*      |Puntaje (1 al 5)|
|ReviewText      |*nvarchar(100)*|Comentario del review|


#### Products
Datos de los productos

|Products        |Tipo de dato   |Descripción|
|----------------|---------------|-----------|
|ProductID       |*smallint*     |ID del producto|
|ProductName     |*nvarchar(50)* |Nombre del producto|
|Category        |*nvarchar(50)* |Categoría del producto|
|Price           |*float*        |Precio del producto|

#### Engagement
Datos sobre la publicidad realizada y cómo le fue.

|engagement_data    |Tipo de dato  |Descripción|
|-------------------|--------------|-----------|
|EngagementID       |*smallint*    |ID de la interacción|
|ContentID          |*tinyint*     |ID del contenido de la publicidad|
|ContentType        |*nvarchar(50)*|El medio en que se hizo la publicidad ('newsletter', 'video', 'socialmedia', 'blog')|
|Likes              |*smallint*    |Cantidad de likes que recibió la publicidad|
|EngagementDate     |*date*        |Fecha de la interacción|
|CampaignID         |*tinyint*     |ID de la campaña en que se realizó la publicidad|
|ProductID          |*tinyint*     |ID del producto que se publicitó|
|ViewsClickCombined |*nvarchar(50)*|Cantidad de vistas y clicks que se obtuvo|

#### Geography
Tabla de los países de los clientes o usuarios.

|geography    |Tipo de dato|Descripción|
|-------------|--------------|-----------|
|GeographyID  |*tinyint*     |ID de la geografía|
|Country      |*nvarchar(50)*|Nombre del país del usuario|
|City         |*nvarchar(50)*|Nombre de la ciudad del usuario|
