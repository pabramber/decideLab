from django.conf import settings

from base.tests import BaseTestCase
from voting.models import Voting, Question, QuestionOption
from census.models import Census
from mixnet.models import Auth

class VotingModelTestCase(BaseTestCase):
    
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

    # Ejemplos ==============================================================

    def test_store_census(self):
        self.assertEqual(Census.objects.count(), 1)

    def test_Voting_toString(self):
        self.assertEquals(str(self.v),"test voting")
        self.assertEquals(str(self.v.question),"test question")
        self.assertEquals(str(self.v.question.options.all()[0]),"option 1 (2)")

    # Ejercicio =============================================================

    def testExist(self):
        v=Voting.objects.get(name='test voting')
        self.assertEquals(v.question.options.all()[0].option, "option 1")
