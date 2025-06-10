import requests
import HTTPClientRequests

module_list = HTTPClientRequests.GET_Modules()
if not(module_list is None):
    print("Выберите модель для конвертации аудио:\n")
    for i, name in enumerate(module_list):
        print(f"{i+1}. {name};\n")
    print(f"{i+2}. Отменить\n")

while True:
    try:
        answer = input()
        if not(answer == f"{i+2}"):
            tts = module_list[int(answer)-1]
            print(tts)
        else:
            tts = None
        break
    except:
        print("Введите номер одного из представленных вариантов!")

if not(tts is None):
    print(HTTPClientRequests.POST_Modules(tts))

    print(HTTPClientRequests.GET_audio("example"))