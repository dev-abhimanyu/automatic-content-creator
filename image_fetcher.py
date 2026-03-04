import requests

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920
MODEL = 'flux'
SEED = 42

def get_image(output_image, prompt):
    print('Fetching Image '+ output_image + '...')
    url = f"https://image.pollinations.ai/prompt/{prompt}?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}&model={MODEL}&seed={SEED}&nologo=true&enhance=false"
    response = requests.get(url)
    # output_image = IMAGE_PATH + '/image_name' + '.jpg'
    with open(output_image, 'wb') as file:
        file.write(response.content)
    print('Image downloaded!')
