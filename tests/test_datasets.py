import itertools

import numpy as np
import sqlalchemy as sa
from unittest import TestCase

from database.database import connect
from database.models import DatasetSamples, Exsiccata, Level, Local, County, State
from database.unaccent import unaccent


class TestDatasets(TestCase):
    counties = None
    states = None
    v2 = None
    v1 = None
    session = None
    engine = None
    br_variations = ['Brasil', 'BRASIL', 'Brasil/Bolivia', 'Brasilia', 'brazil', 'Brazil', 'BRazil', 'BRAZIL',
                     '[Brésil]', 'Brésil']
    genus_variations = ['Potomorphe', 'Peperonia', 'Piperamia']

    @classmethod
    def setUp(self):
        engine, session = connect()
        self.engine = engine
        self.session = session
        self.get_counties()
        self.get_states()
        self.set_samples_v1()
        self.set_samples_v2()
        self.exsiccate_available_v1()
        self.exsiccate_available_v2()

    @classmethod
    def tearDown(self):
        self.engine.dispose()
        self.session.close()

    @classmethod
    def set_samples_v1(self):
        self.v1 = self.session.query(DatasetSamples) \
            .filter(sa.and_(DatasetSamples.name.__eq__('br_dataset'),
                            DatasetSamples.minimum.__eq__(5),
                            DatasetSamples.version.__eq__(1)))

    @classmethod
    def set_samples_v2(self):
        self.v2 = self.session.query(DatasetSamples) \
            .filter(sa.and_(DatasetSamples.name.__eq__('br_dataset'),
                            DatasetSamples.minimum.__eq__(5),
                            DatasetSamples.version.__eq__(2)))

    @classmethod
    def exsiccate_available_v1(self):
        v1_seqs = [q.seq for q in self.v1]
        v2_seqs = [q.seq for q in self.v2]

        self.only_v1 = sorted(list(set(v1_seqs) - set(v2_seqs)))

    @classmethod
    def exsiccate_available_v2(self):
        v1_seqs = [q.seq for q in self.v1]
        v2_seqs = [q.seq for q in self.v2]

        self.only_v2 = sorted(list(set(v2_seqs) - set(v1_seqs)))

    def test_compare_count(self):
        """
        Verifica se todas as espécies que estão presentes na versão 1, porém não estão
        presentes na versão 2 (devido, ao novo pré-processamento) possuem uma quantidade inferior a 5.
        """
        query = self.session.query(Exsiccata) \
            .join(Level, Level.id.__eq__(Exsiccata.level_id)) \
            .filter(Exsiccata.seq.in_(self.only_v1)) \
            .all()

        for q in query:
            count = self.session.query(Exsiccata) \
                .join(Level, Level.id.__eq__(Exsiccata.level_id)) \
                .filter(sa.and_(Exsiccata.seq.__eq__(q.seq),
                                Level.genus.__eq__(q.level.genus),
                                Level.specific_epithet.__eq__(q.level.specific_epithet))) \
                .count()

            assert count < 5

    def test_compare_local(self):
        query = self.session.query(Exsiccata) \
            .join(Level, Level.id.__eq__(Exsiccata.level_id)) \
            .join(Local, Local.id.__eq__(Exsiccata.local_id)) \
            .filter(Exsiccata.seq.in_(self.only_v1)) \
            .all()

        for q in query:
            exsiccatas = self.session.query(Exsiccata) \
                .join(Level, Level.id.__eq__(Exsiccata.level_id)) \
                .join(Local, Local.id.__eq__(Exsiccata.local_id)) \
                .filter(sa.and_(Exsiccata.seq.__eq__(q.seq),
                                Level.genus.__eq__(q.level.genus),
                                Level.specific_epithet.__eq__(q.level.specific_epithet))) \
                .all()

            for exsiccata in exsiccatas:
                # verificar depois
                assert exsiccata.local.country_old.__ne__(None) or \
                       exsiccata.local.country_old not in self.br_variations or \
                       exsiccata.local.country.__ne__(None) or \
                       exsiccata.local.country not in self.br_variations

                assert exsiccata.local.state_province_old.__ne__(None) or \
                       exsiccata.local.state_province_old not in self.states or \
                       exsiccata.local.state_province.__ne__(None) or \
                       exsiccata.local.state_province not in self.states

                assert exsiccata.local.county_old.__ne__(None) or \
                       exsiccata.local.county_old not in self.counties or \
                       exsiccata.local.county.__ne__(None) or \
                       exsiccata.local.county not in self.counties

    def test_county_contains_mun(self):
        count = self.session.query(Exsiccata) \
            .join(Level, Level.id.__eq__(Exsiccata.level_id)) \
            .join(Local, Local.id.__eq__(Exsiccata.local_id)) \
            .filter(sa.and_(Exsiccata.seq.in_(self.only_v2),
                            Local.county_old.ilike('%Mun.'))) \
            .count()

        assert count > 1

    def test_county_all_uppercase_unaccent(self):
        count = self.session.query(Exsiccata) \
            .join(Level, Level.id.__eq__(Exsiccata.level_id)) \
            .join(Local, Local.id.__eq__(Exsiccata.local_id)) \
            .filter(sa.and_(Exsiccata.seq.in_(self.only_v2),
                            Local.county_old.__eq__(sa.func.upper(unaccent(Local.county))))) \
            .count()

        assert count > 1

    def test_difference_genus(self):
        count = self.session.query(Exsiccata) \
            .join(Level, Level.id.__eq__(Exsiccata.level_id)) \
            .join(Local, Local.id.__eq__(Exsiccata.local_id)) \
            .filter(sa.and_(Exsiccata.seq.in_(self.only_v2),
                            Level.genus_old.__ne__(Level.genus))) \
            .count()

        assert count > 1

    def test_difference_specific_epithet(self):
        count = self.session.query(Exsiccata) \
            .join(Level, Level.id.__eq__(Exsiccata.level_id)) \
            .join(Local, Local.id.__eq__(Exsiccata.local_id)) \
            .filter(sa.and_(Exsiccata.seq.in_(self.only_v2),
                            Level.specific_epithet_old.__ne__(Level.specific_epithet))) \
            .count()

        assert count > 1

    @classmethod
    def get_states(self):
        query = self.session.query(State.name, State.uf).all()
        self.states = [q for q in query]
        self.states = itertools.chain(*self.states)

    @classmethod
    def get_counties(self):
        query = self.session.query(County.name).all()
        self.counties = [q for q in query]
        self.counties = itertools.chain(*self.counties)
