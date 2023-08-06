import json
import io
import base64
from PIL import Image, ImageDraw, ImageFont


def generate(event, context):
    font_path = 'calibrib.ttf'  # The font file will be available at this path inside Lambda
    image = Image.new('RGB', (200, 100), color='white')

    try:
        font = ImageFont.truetype(font_path, 20)
    except IOError:
        return {
            'statusCode': 500,
            'body': json.dumps('Unable to load the custom font.'),
        }

    draw = ImageDraw.Draw(image)
    draw.text((10, 10), 'Hello, Lambda!', font=font, fill='black')


    image_data = io.BytesIO()
    image.save(image_data, format='PNG')
    base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
    
    # Return the base64 encoded image
    return {
        'statusCode': 200,
        'body': json.dumps({'image_base64': base64_image}),
    }
