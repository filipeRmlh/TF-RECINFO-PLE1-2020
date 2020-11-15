# Coletor e refinador de dados do Twitter

Para fazer este código funcionar é necessário fazer uma cópia do arquivo `.env.example` e renomeá-la como `.env`.

Em seguida é necessário preencher o valor da variável de ambiente com a chave Bearer, obtida ao realizar uma solicitação de acesso a Api do Twitter.

## Execução

Para executar, rode os seguintes comandos.

* Instalação de dependencias.
```shell script
npm i
```

* Coleta de dados (necessário chave da api)
```shell script
npm run collect
```

* Refinamento dos dados coletados
> O refinamento consiste em remover duplicatas e filtrar apenas os tweets que fazem referência ou são referenciados dentro da própria coleção, para que a coleção seja fechada em si mesma.
```shell script
npm run refine
```
