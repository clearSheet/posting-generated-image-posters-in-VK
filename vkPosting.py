import dates
import requests
import vk
import os
import clear
import parsing

# 4147c9dc535e7668523ec5565bc2c07d4e2ee822f9f90a9c2152d83a5e01c52f709115e760de05c1ac795
# 201490967

acessToken = '4147c9dc535e7668523ec5565bc2c07d4e2ee822f9f90a9c2152d83a5e01c52f709115e760de05c1ac795'
group = 201490967
version = 5.122

text = f'Киноафиша на {dates.date} {dates.month}\nПодробнее на нашем сайте: https://bratsk.com/poster\n#афиша@everydaybratsk #Братск'

session = vk.Session(access_token=acessToken)
apiVk = vk.API(session)

upload_url = apiVk.photos.getWallUploadServer(group_id=group, v=version, scope='wall')['upload_url']

attach = []

clear.clear_directory()

parsing.started()

count = 0

for root, dirs, files in os.walk("baner"):
    for filename in files:
        if count < 11:
            request = requests.post(upload_url, files={"file": open(f'baner/{filename}', 'rb')})

            save_wall_photo = apiVk.photos.saveWallPhoto(group_id=group,
                                                         v=version,
                                                         photo=request.json()['photo'],
                                                         server=request.json()['server'],
                                                         hash=request.json()['hash'])

            saved_photo = 'photo' + str(save_wall_photo[0]['owner_id']) + "_" + str(save_wall_photo[0]['id']) + "_" + str(save_wall_photo[0]['id']) + "_" + acessToken
            attach.append(saved_photo)
        else:
            break

apiVk.wall.post(owner_id=-(group),
                v=version,
                attachments=attach,
                message=text
                )

print('[PUSH] Cinema posting!')





