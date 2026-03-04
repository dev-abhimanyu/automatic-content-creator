import requests
import json

API_KEYS_FILE = 'keys.json'
SITE_NAME = 'pixabay'
DOWNLOAD_DIR = './res'
SITE_STRING = 'https://pixabay.com/api/videos/?key='
INPUT_PARAMETER_FILE = 'parameters.json'


def get_api_key(site_name):
    f = open(API_KEYS_FILE)
    data = json.load(f)
    api_key = data[site_name]
    f.close()
    return api_key


def get_user_input():
    # takes input from user and returns a string replace space with +
    print('Enter the keywords: ')
    user_input_str = input()
    return(user_input_str.replace(' ', '+'))


def get_api_url(site_string, key, params):
    api_url = site_string + key
    # params is a dict
    for p in params:
        api_url = api_url + '&' + p + '=' + params[p]
    return api_url


# site dependent functions
def get_params_dict(user_input):
    params_dict = {}
    params_dict['q'] = user_input
    f = open(INPUT_PARAMETER_FILE)
    data = json.load(f)
    params_dict.update(data["params"])
    print('PARAMS:')
    print(type(params_dict))
    print(params_dict)
    f.close()
    return params_dict


# def get_resource_url(api_response):




api_url = get_api_url(SITE_STRING, get_api_key(SITE_NAME), get_params_dict(get_user_input()))
# api_url = SITE_STRING + get_api_key(SITE_NAME) 
print(api_url)
api_response = requests.get(api_url)
# api_response = requests.get(api_url, get_params_dict(get_user_input()))
print(api_response.json())



# api_key = get_api_key(SITE_NAME)
# api_url = "https://pixabay.com/api/?key=" + api_key + "&q=yellow+flowers&image_type=photo&pretty=true&download=1"
# api_url = "https://pixabay.com/api/videos/?key=" + api_key + "&q=yellow+flowers&pretty=true&download=1"
# response = requests.get(api_url)
# print(response.json())


