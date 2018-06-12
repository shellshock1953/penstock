from penstock import get_sources_list


configuration = {
    'sources': [
        {
            'url': 'http;//example.com'
        },
        {
            'url': 'http;//example.com'
        },
        {
            'url': 'http;//aaa.com'
        }
    ]
}

def test_answer():
    
    assert len(get_sources_list(configuration)) == 2