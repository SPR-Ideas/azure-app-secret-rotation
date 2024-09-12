import requests
from azure.identity import EnvironmentCredential

####################################################################################################
# Network Utilities 
####################################################################################################

def _exit(msg:str): 
    """
    """
    print("Error: " + msg)
    exit(1)


def make_get_request(uri,params,data ):
    """
    """
    try : 
        response = requests.get(uri, params=params, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error : unable to perform GET request at {response.url}")
            _exit(response.text)

    except Exception as e:
        _exit(e)
    return response.json()


def make_post_request( uri ,params,data):
    """
    """
    try :
        response = requests.post(uri, params=params, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error : unable to perform POST request at {response.url}")
            _exit(response.text)
    
    except Exception as e:
        _exit(e)
    return response.json()


def make_put_request(uri, params, data):
    """
    """
    try :
        response = requests.put(uri, params=params, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error : unable to perform PUT request at {response.url}")
            _exit(response.text)

    except Exception as e:
        _exit(e)
    return response.json()


def make_delete_request(uri, params, data):
    """
    """
    try :
        response = requests.delete(uri, params=params, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error : unable to perform DELETE request at {response.url}")
            _exit(response.text)

    except Exception as e:
        _exit(e)


####################################################################################################
# Azure Utilities 
####################################################################################################


def get_acces_token():
    """
    """
    try:
        credential = EnvironmentCredential()
        scope = "Directory.ReadWrite.All"
        return credential.get_token(scope)
    except Exception as e:
        _exit("Unable to Get access token\n"+e)
