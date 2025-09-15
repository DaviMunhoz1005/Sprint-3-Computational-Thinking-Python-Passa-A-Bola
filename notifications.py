def notify_email(to: str, subject: str, body: str):
    """
    Simula o envio de um email.

    Parâmetros:
    - to (str): destinatário do email
    - subject (str): assunto do email
    - body (str): corpo do email

    Como é uma simulação, o envio real não ocorre.
    Apenas imprime a mensagem no terminal (stdout).
    """
    print(f"[NOTIFY] Para: {to} | Assunto: {subject}\n{body}\n")


def notify_bulk(recipients, subject, body):
    """
    Envia notificações para múltiplos destinatários.

    Parâmetros:
    - recipients (list[str]): lista de emails ou contatos
    - subject (str): assunto da notificação
    - body (str): corpo da notificação

    Internamente chama 'notify_email' para cada destinatário.
    """
    for r in recipients:
        notify_email(r, subject, body)
