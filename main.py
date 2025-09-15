# main.py
import argparse
import services as s  # módulo com funções de negócio (jogadoras, times, torneios, inscrições)
import json


def main():
    """
    Ponto de entrada do CLI da Plataforma Copa PAB.
    Permite gerenciar jogadoras, times, torneios e inscrições via terminal.
    """
    parser = argparse.ArgumentParser(description="Plataforma Copa PAB - CLI")
    sub = parser.add_subparsers(dest="cmd")  # subcomandos principais (jogadora, time, torneio, inscrever)

    # ----------------- Jogadoras -----------------
    jog = sub.add_parser("jogadora", help="Gerenciar jogadoras")
    jog_sub = jog.add_subparsers(dest="action")  # ações possíveis para jogadora

    jog_sub.add_parser("listar", help="Listar todas as jogadoras")  # listar todas jogadoras

    # criar nova jogadora: nome, idade e contato
    cj = jog_sub.add_parser("criar", help="Criar nova jogadora")
    cj.add_argument("nome")
    cj.add_argument("idade", type=int)
    cj.add_argument("contato")

    # ----------------- Times -----------------
    tm = sub.add_parser("time", help="Gerenciar times")
    tm_sub = tm.add_subparsers(dest="action")  # ações possíveis para times

    tm_sub.add_parser("listar", help="Listar todos os times")  # listar todos os times

    # criar novo time: nome + lista de IDs de jogadoras
    ct = tm_sub.add_parser("criar", help="Criar novo time")
    ct.add_argument("nome")
    ct.add_argument("integrantes", nargs="+", help="IDs das jogadoras")  # aceita múltiplos IDs

    # ----------------- Torneios -----------------
    tr = sub.add_parser("torneio", help="Gerenciar torneios")
    tr_sub = tr.add_subparsers(dest="action")  # ações possíveis para torneios

    tr_sub.add_parser("listar", help="Listar todos os torneios")  # listar todos os torneios

    # criar novo torneio: nome + número de vagas
    ctr = tr_sub.add_parser("criar", help="Criar novo torneio")
    ctr.add_argument("nome")
    ctr.add_argument("vagas", type=int)

    # ----------------- Inscrições -----------------
    ins = sub.add_parser("inscrever", help="Inscrever time em torneio")
    ins.add_argument("torneio_id")  # ID do torneio
    ins.add_argument("time_id")     # ID do time

    # ----------------- Execução -----------------
    args = parser.parse_args()  # parseia os argumentos do CLI

    try:
        # ---------- Jogadora ----------
        if args.cmd == "jogadora":
            if args.action == "listar":
                # imprime lista de jogadoras em JSON formatado
                print(json.dumps(s.listar_jogadoras(), indent=2, ensure_ascii=False))
            elif args.action == "criar":
                nova = s.criar_jogadora(args.nome, args.idade, args.contato)
                print(json.dumps(nova, indent=2, ensure_ascii=False))

        # ---------- Time ----------
        elif args.cmd == "time":
            if args.action == "listar":
                print(json.dumps(s.listar_times(), indent=2, ensure_ascii=False))
            elif args.action == "criar":
                novo = s.criar_time(args.nome, args.integrantes)
                print(json.dumps(novo, indent=2, ensure_ascii=False))

        # ---------- Torneio ----------
        elif args.cmd == "torneio":
            if args.action == "listar":
                print(json.dumps(s.listar_torneios(), indent=2, ensure_ascii=False))
            elif args.action == "criar":
                novo = s.criar_torneio(args.nome, args.vagas)
                print(json.dumps(novo, indent=2, ensure_ascii=False))

        # ---------- Inscrição ----------
        elif args.cmd == "inscrever":
            # inscreve um time em um torneio
            insc = s.inscrever_time(args.torneio_id, args.time_id)
            print(json.dumps(insc, indent=2, ensure_ascii=False))

        else:
            # caso comando inválido ou vazio, mostra ajuda
            parser.print_help()

    except Exception as e:
        # captura qualquer erro e exibe no terminal
        print(f"Erro: {e}")


# execução do script
if __name__ == "__main__":
    main()
