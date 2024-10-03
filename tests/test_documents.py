from http import HTTPStatus

from fastapi_project.schemas import DocumentSchema



def test_create_document(client,token):
    response = client.post(
        '/documents/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'content': 'Assunto do dia',
            'topic': 'teste'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'content': 'Assunto do dia',
        'owner_id': 1,
        'topic': 'teste'        
    }


def test_create_document_missing_content(client, token):
    response = client.post(
        '/documents/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'topic': 'teste'
        }
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_document_missing_topic(client, token):
    response = client.post(
        '/documents/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'content': 'Assunto do dia'
        }
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY 


def test_read_documents(client, token):
    response = client.get(
        '/documents/',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'documents':[]}


def test_read_document_by_topic(client, document, token):
    response = client.get(
        f'/documents/?topic={document.topic}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'documents': [{
                                    'id': 1,
                                    'content': 'Assunto do dia',
                                    'owner_id': 1,
                                    'topic': 'teste' 
                                }]
                               }


def test_patch_document(client, document, token):
    response = client.patch(
        f'/documents/{document.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'content': 'Assunto de ontem',
            'topic': 'teste'            
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'content': 'Assunto de ontem',
        'owner_id': 1,
        'topic': 'teste'        
    }


def test_update_document_not_found(client, token):
    response = client.patch(
        '/documents/666',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'content': 'Assunto de ontem',
            'topic': 'teste'            
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Document not found'}


def test_delete_document(client, document, token):
    response = client.delete(
        f'/documents/{document.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Document deleted'}


def test_delete_document_not_found(client, token):
    response = client.delete(
        '/documents/666',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Document not found'}