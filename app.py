import requests
# def create_album()
# gigz
# "albumkey": "1cea39818e07f5bb66f7606b85200daa4df0c64526b4e0be7c8af8dc4b7a0199"
def create_album():
    url = "https://lambda-face-recognition.p.rapidapi.com/album"

    payload = "album=gigz"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "370aa249b8msh84aac5936b96f69p1d5e51jsn57f407d92c3f",
        'x-rapidapi-host': "lambda-face-recognition.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    import pdb;pdb.set_trace()
    print(response.text)


def train_album():
    url = "https://lambda-face-recognition.p.rapidapi.com/album_train"

    payload = {
        "album": 'gigz',
        'albumkey': '1cea39818e07f5bb66f7606b85200daa4df0c64526b4e0be7c8af8dc4b7a0199',
        'entryid': 'gg',
        "urls": 'https://res.cloudinary.com/mutti/image/upload/v1612303196/g1_fukgxi.jpg,\
                 https://res.cloudinary.com/mutti/image/upload/v1612303159/g3_f5zp6x.jpg, \
                 https://res.cloudinary.com/mutti/image/upload/v1612303159/g3_f5zp6x.jpg, \
                 https://res.cloudinary.com/mutti/image/upload/v1612303196/g1_fukgxi.jpg, \
                 https://res.cloudinary.com/mutti/image/upload/v1612303165/g2_cr2z4x.jpg, \
                 https://res.cloudinary.com/mutti/image/upload/v1612303159/g3_f5zp6x.jpg'

    }


    # payload = {
    #     "album": 'gigz',
    #     'albumkey': '1cea39818e07f5bb66f7606b85200daa4df0c64526b4e0be7c8af8dc4b7a0199',
    #     'entryid': 'dan',
    #     "urls": 'https://res.cloudinary.com/mutti/image/upload/v1612303140/d1_zb4ho5.png'
    #     # [
    #     # 'https://res.cloudinary.com/mutti/image/upload/v1612303159/g3_f5zp6x.jpg',
    #     # 'https://res.cloudinary.com/mutti/image/upload/v1612303196/g1_fukgxi.jpg',
    #     # 'https://res.cloudinary.com/mutti/image/upload/v1612303165/g2_cr2z4x.jpg',
    #     # 'https://res.cloudinary.com/mutti/image/upload/v1612303159/g3_f5zp6x.jpg'
    #     # ],
    # }
 

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "370aa249b8msh84aac5936b96f69p1d5e51jsn57f407d92c3f",
        'x-rapidapi-host': "lambda-face-recognition.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    import pdb; pdb.set_trace()
    print(response.text)

# train_album()


def recognize():

    url = "https://lambda-face-recognition.p.rapidapi.com/recognize"

    payload = {
        "albumkey": "1cea39818e07f5bb66f7606b85200daa4df0c64526b4e0be7c8af8dc4b7a0199",
        "urls": "https://res.cloudinary.com/mutti/image/upload/v1612303175/g4_vvmymh.jpg",
        # "urls":"https://res.cloudinary.com/mutti/image/upload/v1612303159/g3_f5zp6x.jpg", #correct
        # "urls": "https://res.cloudinary.com/mutti/image/upload/v1612303196/g1_fukgxi.jpg", # correct
        # "urls": "https://res.cloudinary.com/mutti/image/upload/v1612303165/g2_cr2z4x.jpg",
        # "urls":"https://res.cloudinary.com/mutti/image/upload/v1612303140/d1_zb4ho5.png",
        # "urls": "https://res.cloudinary.com/mutti/image/upload/v1612303135/d3_p7xlxr.png",
        "album": "gigz",
    }

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "370aa249b8msh84aac5936b96f69p1d5e51jsn57f407d92c3f",
        'x-rapidapi-host': "lambda-face-recognition.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    import pdb; pdb.set_trace()

    print(response.text)

recognize()