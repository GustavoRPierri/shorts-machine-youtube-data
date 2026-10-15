# Estilo de código

- **Português obrigatório**: nomes de variáveis, funções, campos de model, comentários, flags de CLI e variáveis de env sempre em português. Termos técnicos sem tradução consagrada (API, URL, JSON…) ficam em inglês.
- **Nome de variaveis e funções**: Usar CamelCase para nomes de variáveis e funções. Nomes de classes e dataclasses devem ser em PascalCase. Nomes de constantes devem ser em UPPER_CASE.
- **Sem method chaining**: nunca encadeie mais de um `.metodo()` por linha. Quebre em variáveis intermediárias com nomes descritivos.
- **Sem helpers desnecessários**: prefira código explícito e inline a criar funções privadas para um único uso. Só extraia função quando ela for chamada em mais de um lugar.
- **Valores inline**: dicts de parâmetros, campos e configurações fixas ficam dentro do próprio método que os usa, não em arquivos de constantes separados.
- **Só o que foi pedido**: Não seja proativa e implemente exatamente o escopo solicitado. Não adicione funcionalidades, arquivos, refatorações ou "melhorias" extras por conta própria.
- **Tratamento de exceções**: Implemente tratamento de exceções em todas as funções, sempre trazendo mensgemns de erro via logs: "[nome de função] [nome do arquivo]: execao - erro", para facilitar a identificação do ponto de falha. Evite usar `raise` sem tratamento, a não ser que seja para interromper a execução do programa.
