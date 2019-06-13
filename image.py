import boto3
from Check import Elements

if __name__ == "__main__":
    # Change the value of bucket to the S3 bucket that contains your image file.
    bucket='bucket'
    # Change the value of photo to your image file name.
    photo='picture'

    client=boto3.client('rekognition')
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    status = False
    textDetections=response['TextDetections']

    el = Elements()
    contents = el.getElements()
    neg = False
    for text in textDetections:
        for cont in contents:
            if text['DetectedText'].upper() == "SEM" or text['DetectedText'].upper() == "NÃO" or text['DetectedText'].upper() == "ZERO":
                neg = True
            if text['DetectedText'].lower() == cont:
                status = True
    if status and neg:
        print('**ESSE PRODUTO NÃO POSSUI LACTOSE**')
    elif status is False:
        print('**ESSE PRODUTO NÃO POSSUI DESCRIÇÃO**')
    else:
        print('**ESSE PRODUTO POSSUI LACTOSE**')
 