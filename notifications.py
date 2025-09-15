def notify_email(to: str, subject: str, body: str):
    # Simulação de envio: escrever no stdout
    print(f"[NOTIFY] Para: {to} | Assunto: {subject}\n{body}\n")

def notify_bulk(recipients, subject, body):
    for r in recipients:
        notify_email(r, subject, body)