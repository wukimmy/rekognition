import boto3

if __name__ == "__main__":
    # Change the value of bucket to the S3 bucket that contains your image file.
    # Change the value of photo to your image file name.
    bucket='nome do bucket'
    photo='nome da imagem'

    client=boto3.client('rekognition')
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    status = False
    textDetections=response['TextDetections']
    print ('Detected text: ')
    for text in textDetections:
            conf = int(text['Confidence'])
            if conf> 97 :
                print (text['DetectedText'] + str(text['Confidence']))
            if 'leite' in text['DetectedText'].lower():
                status = True
            print
    if status:
        print('**ESSE PRODUTO POSSUI LACTOSE**')
