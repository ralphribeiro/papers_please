""" 

receive_bulletin

    Each morning you are issued an official bulletin from
the Ministry of Admission.
    
     (Bulletin from Ministry)

    This bulletin will provide updates to regulations and procedures and the
name of a wanted criminal.

     (Bulletin is updated with Policies and Criminal)

    The bulletin is provided in the form of a string. It may include one or
more of the following:

        Updates to the list of nations (comma-separated if more than one)
    whose citizens may enter (begins empty, before the first bulletin):

        (list of Nations of Citizens)
        
        example 1: Allow citizens of Obristan
        example 2: Deny citizens of Kolechia, Republia

        Updates to required documents
        Updates to required vaccinations
        Update to a currently wanted criminal
    
    ----------------

inspect

    The inspect method will receive an object representing each entrant's set
of identifying documents. This object will contain zero or more properties
which represent separate documents. Each property will be a string value.
These properties may include the following:

    Applies to all entrants:
    
    passport
    certificate_of_vaccination

    Applies only to citizens of Arstotzka:

    ID_card

    Applies only to foreigners:

    access_permit
    work_pass
    grant_of_asylum
    diplomatic_authorization
    

 """

import pytest

from src.app.model import Bulletin, regulations


class TestRegulations:
    def test_regulation_for_citizens_of_nation(self):
        regulation = 'Allow citizens of Obristan'
        assert regulations(regulation) == {'Allow': ('Obristan', )}

    def test_regulation_for_citizens_of_nations(self):
        regulation = 'Deny citizens of Kolechia, Republia'
        assert regulations(regulation) == {'Deny': ('Kolechia', 'Republia')}

    def test_more_than_regulation_for_citizens_of_nations(self):
        regulation = '''Deny citizens of Kolechia, Republia
        Allow citizens of Obristan'''

        assert regulations(regulation) == {
            'Deny': ('Kolechia', 'Republia'),
            'Allow': ('Obristan', )
        }

    def test_documents_regulations_foreigners_require_access_permit(self):
        regulation = 'Foreigners require access permit'
        assert regulations(regulation) == {
            'Foreigners': ('require', 'access', 'permit', )
        }

    def test_documents_regulations_aztrotzca_citizen_require_id_card(self):
        regulation = 'Citizens of Arstotzka require ID card'
        assert regulations(regulation) == {
            'Citizens': ('Arstotzka', 'require', 'ID card')
        }

    def test_documents_regulations_workers_require_work_pass(self):
        regulation = 'Workers require work pass'
        assert regulations(regulation) == {
            'Workers': ('require', 'work', 'pass')
        }

    def test_vaccination_regulations_citzens_require_polio(self):        
        regulation = 'Citizens of Antegria, Republia, Obristan require polio vaccination'
        assert regulations(regulation) == {
            'vaccination': ('Antegria', 'Republia', 'Obristan', 'polio')
        }

        # example 2: Entrants no longer require tetanus vaccination


@pytest.mark.skip('not implemented')
class TestInspetor:
    def test_inspetor_receiver_bulletin(self):
        regulations = [
            'Allow citizens of Obristan',
            'Deny citizens of Kolechia',
            'Republia'
        ]
        bulletin = Bulletin(regulations)
        inspetor = Inspetor()
        inspetor.receive_bulletin(regulations)
        assert inspetor.bulletins == [bulletin]
