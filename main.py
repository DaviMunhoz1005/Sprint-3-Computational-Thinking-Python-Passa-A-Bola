# main.py
import argparse
import services as s
import json


def main():
    parser = argparse.ArgumentParser(description="Plataforma Copa PAB - CLI")
    sub = parser.add_subparsers(dest="cmd")

    # ----------------- Jogadoras -----------------
    jog = sub.add_parser("jogadora", help="Gerenciar jogadoras")
    jog_sub = jog.add_subparsers(dest="action")

    jog_sub.add_parser("listar", help="Listar todas as jogadoras")

    cj = jog_sub.add_parser("criar", help="Criar nova jogadora")
    cj.add_argument("nome")
    cj.add_argument("idade", type=int)
    cj.add_argument("contato")

    # ----------------- Times -----------------
    tm = sub.add_parser("time", help="Gerenciar times")
    tm_sub = tm.add_subparsers(dest="action")

    tm_sub.add_parser("listar", help="Listar todos os times")

    ct = tm_sub.add_parser("criar", help="Criar novo time")
    ct.add_argument("nome")
    ct.add_argument("integrantes", nargs="+", help="IDs das jogadoras")

    # ----------------- Torneios -----------------
    tr = sub.add_parser("torneio", help="Gerenciar torneios")
    tr_sub = tr.add_subparsers(dest="action")

    tr_sub.add_parser("listar", help="Listar todos os torneios")

    ctr = tr_sub.add_parser("criar", help="Criar novo torneio")
    ctr.add_argument("nome")
    ctr.add_argument("vagas", type=int)

    # ----------------- Inscrições -----------------
    ins = sub.add_parser("inscrever", help="Inscrever time em torneio")
    ins.add_argument("torneio_id")
    ins.add_argument("time_id")

    # ----------------- Execução -----------------
    args = parser.parse_args()

    try:
        if args.cmd == "jogadora":
            if args.action == "listar":
                print(json.dumps(s.listar_jogadoras(), indent=2, ensure_ascii=False))
            elif args.action == "criar":
                nova = s.criar_jogadora(args.nome, args.idade, args.contato)
                print(json.dumps(nova, indent=2, ensure_ascii=False))

        elif args.cmd == "time":
            if args.action == "listar":
                print(json.dumps(s.listar_times(), indent=2, ensure_ascii=False))
            elif args.action == "criar":
                novo = s.criar_time(args.nome, args.integrantes)
                print(json.dumps(novo, indent=2, ensure_ascii=False))

        elif args.cmd == "torneio":
            if args.action == "listar":
                print(json.dumps(s.listar_torneios(), indent=2, ensure_ascii=False))
            elif args.action == "criar":
                novo = s.criar_torneio(args.nome, args.vagas)
                print(json.dumps(novo, indent=2, ensure_ascii=False))

        elif args.cmd == "inscrever":
            insc = s.inscrever_time(args.torneio_id, args.time_id)
            print(json.dumps(insc, indent=2, ensure_ascii=False))

        else:
            parser.print_help()

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
