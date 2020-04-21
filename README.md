# Correios

Sistema de notificacao para Correios. Busca atualizacoes a cada 2 min e, caso encontre mudancas, manda mensagens para o Desktop (apenas linux) e para o celular.

# Configuracao

Para executar, basta escrever o codigo de rastreio no arquivo `codigo.txt` e rodar `correios.py` a partir de um terminal, com `python3` instalado.

## Notificacoes para Desktop (apenas linux)

Requer `notify-send`, presente em grande parte das distribuicoes.

## Notificacoes para Celular

Usa [https://notify.run/](https://notify.run/), veja no link as instrucoes.
