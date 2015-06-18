from pdp.views.api.identity import Publish
import json
from pdp.test.util import TestWithMocks, mock_request
from restclients.exceptions import DataFailureException, IRWSPersonNotFound


class TestIdentity(TestWithMocks):

    def setup_class(self):
        self.mock_items = {'irws': 'pdp.views.api.identity.IRWS'}

    def test_publish_basic(self):
        assert (set((key, value)
                    for key, value in Publish.publish_options.items()) ==
                {('Y', 'yes'), ('N', 'no'), ('E', 'no email')})
        assert (set((key, value)
                    for key, value
                    in Publish.publish_options_reverse.items()) ==
                {('yes', 'Y'), ('no', 'N'), ('no email', 'E')})

    def test_publish_get_no(self):
        publish = Publish()
        get_hepps = self.irws.return_value.get_hepps_person_by_netid
        get_hepps.return_value.wp_publish = 'N'

        response = publish.GET(mock_request())

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body['publish'] == 'no'
        get_hepps.assert_called_once_with('jjj')

    def test_publish_get_no_email(self):
        publish = Publish()
        get_hepps = self.irws.return_value.get_hepps_person_by_netid
        get_hepps.return_value.wp_publish = 'E'

        response = publish.GET(mock_request())

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body['publish'] == 'no email'

    def test_publish_get_unexpected_publish_value(self):
        publish = Publish()
        get_hepps = self.irws.return_value.get_hepps_person_by_netid
        get_hepps.return_value.wp_publish = 'Q'

        response = publish.GET(mock_request())

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body['publish'] == 'Q'

    def test_publish_get_not_hepps_person(self):
        publish = Publish()
        self.irws.return_value.get_hepps_person_by_netid.side_effect = (
            IRWSPersonNotFound('not a hepps person'))

        response = publish.GET(mock_request())

        assert response.status_code == 404

    def test_publish_get_df_exception(self):
        publish = Publish()
        self.irws.return_value.get_hepps_person_by_netid.side_effect = (
            DataFailureException('foo', '200', 'service error'))
        exception_caught = False

        try:
            publish.GET(mock_request())
        except DataFailureException:
            exception_caught = True

        assert exception_caught

    def test_publish_put_basic(self):
        publish = Publish()
        self.irws.return_value.post_hepps_person_by_netid.return_value = {}

        response = publish.PUT(mock_request(body={'publish': 'no email'}))

        assert response.status_code == 200
        (self.irws.return_value.post_hepps_person_by_netid
         .assert_called_once_with('jjj', json.dumps({'wp_publish': 'E'})))

    def test_publish_put_not_hepps_person(self):
        publish = Publish()
        self.irws.return_value.post_hepps_person_by_netid.side_effect = (
            IRWSPersonNotFound('not hepps'))

        response = publish.PUT(mock_request(body={'publish': 'no email'}))

        assert response.status_code == 404

    def test_publish_put_not_hepps_person(self):
        publish = Publish()
        self.irws.return_value.post_hepps_person_by_netid.side_effect = (
            IRWSPersonNotFound('not hepps'))

        response = publish.PUT(mock_request(body={'publish': 'no email'}))

        assert response.status_code == 404

    def test_publish_put_bad_request(self):
        publish = Publish()
        self.irws.return_value.post_hepps_person_by_netid.side_effect = (
            IRWSPersonNotFound('not hepps'))

        response = publish.PUT(mock_request(body={'publish': 'Q'}))

        assert response.status_code == 400

    def test_publish_put_df_exception(self):
        publish = Publish()
        self.irws.return_value.post_hepps_person_by_netid.side_effect = (
            DataFailureException('foo', '200', 'service error'))
        exception_caught = False

        try:
            publish.PUT(mock_request(body={'publish': 'no email'}))
        except DataFailureException:
            exception_caught = True

        assert exception_caught
