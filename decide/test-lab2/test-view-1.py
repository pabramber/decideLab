from django.conf import settings

from base.tests import BaseTestCase
from voting.models import Voting, Question, QuestionOption
from census.models import Census
from mixnet.models import Auth

class ApiTestCase(BaseTestCase):

    def setUp(self):
        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()
        self.v = self.create_voting()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.census = None
        self.v = None

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    
    # Ejemplo ===========================================================================
    
    def test_update_voting_400(self):
        v = self.create_voting()
        data = {} #El campo action es requerido en la request
        self.login()
        response = self.client.put('/voting/{}/'.format(v.pk), data, format= 'json')
        self.assertEquals(response.status_code, 400)

    # Ejercicio =========================================================================

    def testCreateVotinAPI(self):
        self.login()
        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

        voting = Voting.objects.get(name='Example')
        self.assertEqual(voting.desc, 'Description example')
