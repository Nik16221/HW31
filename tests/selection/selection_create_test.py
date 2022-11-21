import pytest

from tests.factories import AdFactory


@pytest.mark.django_db
def test_create_selection(client, ad, access_token, user):
    ads = AdFactory.create_batch(5)
    response = client.post('/selection/',
                           {"name": "test",
                            "owner": user.pk,
                            "items": [ad.pk for ad in ads]},
                           HTTP_AUTHORIZATION="Bearer " + access_token)

    assert response.status_code == 201
    assert response.data == {
        "id": 1,
        "name": "test",
        "owner": user.pk,
        "items": [ad.pk for ad in ads]
    }
