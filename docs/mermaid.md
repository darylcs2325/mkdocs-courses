## Diagramas

``` mermaid
graph LR
  A[Estos son los errores que se originan] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```