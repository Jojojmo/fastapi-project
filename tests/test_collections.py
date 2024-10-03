from http import HTTPStatus



import os

def test_create_collection(client, 
                           token, 
                           document,
                           patch_save_vector_dir):
    name = "string"
    response = client.post(
        '/collections/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            "name": name,
            #"topic": "string",
            #"skip": 0,
            #"limit": 100
            }
    )

    assert response.status_code == HTTPStatus.CREATED

    file_path = 'tests/embeddings_test/' + name + '.bin'
    if os.path.exists(file_path):
        os.remove(file_path)


    assert response.json() == {
                        "id": 1,
                        "name": "string"
                        }
    
def test_list_collection(client,
                         token,
                         collection):
    response = client.get(
        '/collections/',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
                        "collections": [
                            {
                            "id": 1,
                            "name": "string"
                            }
                        ]
                        }