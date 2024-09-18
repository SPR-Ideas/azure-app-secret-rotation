import time
import requests
from azure.identity import EnvironmentCredential

ARM_BASE_URL = "https://management.azure.com/"
AD_BASE_URL = "https://graph.microsoft.com/"

ACCESS_TOKEN_OBJECT = {}

####################################################################################################
# Network Utilities
####################################################################################################

def _exit(msg):
    """Exit's the Program by printing the given message."""
    print("Error: " + msg)
    exit(1)


def authorize(func):
    """
    Decorator to manage authorization and token retrieval for Azure API requests.

    If the token for the requested URI is not present or expired, it retrieves a new access token.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function with access token management.
    """
    def get_access_token(*args, **kwargs):
        """
        Inner function to get access token and proceed with the original request.
        """
        global ACCESS_TOKEN_OBJECT
        if ACCESS_TOKEN_OBJECT.get(kwargs["uri"]) == None or ACCESS_TOKEN_OBJECT[kwargs["uri"]]["expires_on"] <= time.time():
            ACCESS_TOKEN_OBJECT[kwargs["uri"]] = make_authorization_request(kwargs["uri"])
        return func(*args, **kwargs)
    return get_access_token


def make_authorization_request(scope):
    """
    Retrieves the access token for the specified scope using Azure credentials.

    Args:
        scope (str): The URI scope for which the access token is needed.

    Returns:
        dict: A dictionary containing the access token and its expiration time.

    Raises:
        Exception: If unable to retrieve the access token.
    """
    try:
        credential = EnvironmentCredential()
        print("auth called ..")
        return credential.get_token(scope + ".default")._asdict()
    except Exception as e:
        _exit("Unable to Get access token\n" + repr(e))


@authorize
def make_get_request(uri, path, params=None, data=None):
    """
    Performs an HTTP GET request.

    Args:
        uri (str): The base URI for the request.
        path (str): The API path for the GET request.
        params (dict, optional): Query parameters for the request. Defaults to None.
        data (dict, optional): Additional data to send with the request. Defaults to None.

    Returns:
        dict: The JSON response from the GET request.

    Raises:
        Exception: If the GET request fails.
    """
    try:
        response = requests.get(
            uri + path,
            headers={"Authorization": "Bearer " + ACCESS_TOKEN_OBJECT[uri]["token"]},
            params=params, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to perform GET request at {response.url}")
            _exit(response.text)

    except Exception as e:
        _exit(repr(e))
    return response.json()


@authorize
def make_post_request(uri, path, params=None, data=None):
    """
    Performs an HTTP POST request.

    Args:
        uri (str): The base URI for the request.
        path (str): The API path for the POST request.
        params (dict, optional): Query parameters for the request. Defaults to None.
        data (dict, optional): JSON data to include in the POST request. Defaults to None.

    Returns:
        dict: The JSON response from the POST request.

    Raises:
        Exception: If the POST request fails.
    """
    try:
        response = requests.post(
            uri + path,
            headers={"Authorization": "Bearer " + ACCESS_TOKEN_OBJECT[uri]["token"]},
            params=params, json=data)

        if response.status_code in (200, 201):
            return response.json()
        elif response.status_code == 204:
            return {}
        else:
            print(f"Error: Unable to perform POST request at {response.url}")
            _exit(response.json())

    except Exception as e:
        _exit(repr(e))
    return response.json()


@authorize
def make_put_request(uri, path, params=None, data=None):
    """
    Performs an HTTP PUT request.

    Args:
        uri (str): The base URI for the request.
        path (str): The API path for the PUT request.
        params (dict, optional): Query parameters for the request. Defaults to None.
        data (dict, optional): Data to include in the PUT request. Defaults to None.

    Returns:
        dict: The JSON response from the PUT request.

    Raises:
        Exception: If the PUT request fails.
    """
    try:
        response = requests.put(
            uri + path,
            headers={"Authorization": "Bearer " + ACCESS_TOKEN_OBJECT[uri]["token"]},
            params=params, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to perform PUT request at {response.url}")
            _exit(response.text)

    except Exception as e:
        _exit(repr(e))
    return response.json()


@authorize
def make_delete_request(uri, path, params=None, data=None):
    """
    Performs an HTTP DELETE request.

    Args:
        uri (str): The base URI for the request.
        path (str): The API path for the DELETE request.
        params (dict, optional): Query parameters for the request. Defaults to None.
        data (dict, optional): Data to include in the DELETE request. Defaults to None.

    Returns:
        dict: The JSON response from the DELETE request.

    Raises:
        Exception: If the DELETE request fails.
    """
    try:
        response = requests.delete(
            uri + path,
            headers={"Authorization": "Bearer " + ACCESS_TOKEN_OBJECT[uri]["token"]},
            params=params, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to perform DELETE request at {response.url}")
            _exit(response.text)

    except Exception as e:
        _exit(repr(e))
