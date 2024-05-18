import logging

from database.models import Local


def update_country(session):
    """
    Seleciona todos ids onde foi encontrado uma variações da palavra BR, e atualiza com a palavra correta.
    :param session: conexão com banco de dados.
    """
    br_variations = ['Brasil', 'BRASIL', 'Brasil/Bolivia', 'Brasilia', 'brazil', 'Brazil', 'BRazil', 'BRAZIL',
                     '[Brésil]', 'Brésil']

    query = session.query(Local.id).filter(Local.country_old.in_(br_variations)).all()

    locals_id = [q[0] for q in query]
    session.query(Local) \
        .filter(Local.id.in_(locals_id)) \
        .update({Local.country: 'Brasil'}, synchronize_session=False)

    session.commit()

    count_variations_br = session.query(Local) \
        .filter(Local.country_old.in_(br_variations)) \
        .count()

    logging.info('count of variations in %d' % count_variations_br)