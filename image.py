import boto3
from Check import Elements

if __name__ == "__main__":
    # Change the value of bucket to the S3 bucket that contains your image file.
    # Change the value of photo to your image file name.
    bucket='nome do bucket'
    photo='nome da foto'

    client=boto3.client('rekognition')
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    status = False
    textDetections=response['TextDetections']

    el = Elements()
    contents = el.getElements()
    print(contents)
    for text in textDetections:
            if int(text['Confidence'])> 97 :
                for cont in contents:
                    if text == cont:
                        status = True
    if status:

        print('**ESSE PRODUTO POSSUI LACTOSE**')
