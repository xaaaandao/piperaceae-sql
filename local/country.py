from models import Local, LocalTrusted


def update_country(session):
    """
    Seleciona todos ids onde foi encontrado uma variações da palavra BR, e atualiza com a palavra correta.
    :param session: conexão com banco de dados.
    """
    br_variations = ['Brasil', 'BRASIL', 'Brasil/Bolivia', 'Brasilia', 'brazil', 'Brazil', 'BRazil', 'BRAZIL',
                     '[Brésil]', 'Brésil']
    query = session.query(Local.id).filter(Local.country.in_(br_variations)).all()

    locals_id = [q[0] for q in query]
    session.query(LocalTrusted) \
        .filter(LocalTrusted.local_id.in_(locals_id)) \
        .update({LocalTrusted.country: 'Brasil'}, synchronize_session=False)
