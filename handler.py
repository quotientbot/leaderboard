import json
import io
import base64
from PIL import Image, ImageDraw, ImageFont

def seller_label(team_obj):
    stats = str(team_obj.place_pts) + " " + str(team_obj.kill_pts) + " " + str(team_obj.total_pts)
    i = team_obj.pos
    seller = team_obj.name
    full_label = "%i  %s         %s" %(i+1, seller, stats)

    return full_label

def calc_dimensions(text, font):
    img = Image.open("test.png").resize((1400,788) ,Image.ANTIALIAS)
    draw = ImageDraw.Draw(img)
    width, height = 1400, 788
    font_size = 30
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    return text_x, text_y


def generate(event, context):
    font_path = 'calibrib.ttf'  # The font file will be available at this path inside Lambda
    title = json.loads(event["body"]).get('title')
    subtitle = json.loads(event["body"]).get('subtitle')
    teams = json.loads(event["body"]).get('teams')

    base = Image.new('RGB', (1400, 788), color='black')

    try:
        # font = ImageFont.truetype(font_path, 20)
        title_text_1 = ImageFont.truetype(font_path, 80)
        title_text_2 = ImageFont.truetype(font_path, 90)
    except IOError:
        return {
            'statusCode': 500,
            'body': json.dumps('Unable to load the custom font.'),
        }

    text_x, text_y = calc_dimensions(title, title_text_1)
    ImageDraw.Draw(base).text((text_x+5, 5+5), title, 'rgb(235, 146, 52)', font=title_text_1, spacing=10)
    ImageDraw.Draw(base).text((text_x+3, 5+3), title, 'rgb(0, 0, 0)', font=title_text_1, spacing=10)
    ImageDraw.Draw(base).text((text_x, 5), title, 'rgb(255, 255, 255)', font=title_text_1, spacing=10)

    text_x, text_y = calc_dimensions(subtitle, title_text_2)
    ImageDraw.Draw(base).text((text_x+5, 65+5), subtitle, 'rgb(235, 146, 52)', font=title_text_2, spacing=10)
    ImageDraw.Draw(base).text((text_x+3, 65+3), subtitle, 'rgb(0, 0, 0)', font=title_text_2, spacing=10)
    ImageDraw.Draw(base).text((text_x, 65), subtitle, 'rgb(255, 255, 255)', font=title_text_2, spacing=10)

    ImageDraw.Draw(base).rectangle([(60, 160), (700, 200)], fill='rgb(252, 144, 3)')
    normal_font = ImageFont.truetype(font_path, 20)

    table_head = "#                 TEAMNAMES                                           POS     KILLS    TOTAL"
    ImageDraw.Draw(base).text((90, 170), table_head, 'rgb(0, 0, 0)', font=normal_font, spacing=10)

    t = 44
    s = 40
    l = teams


    for i in range(0, 13):
        ImageDraw.Draw(base).rectangle([(60, 160+t), (700, 200+t)], fill='rgb(250, 250, 250)')
        
        t+=44
    ImageDraw.Draw(base).rectangle([(60, 160+44), (130, 772)], fill='rgb(23, 23, 23)')

    t = 44
    for i in range(0, 13):
        ImageDraw.Draw(base).text((90, 170+t), str(l[i]["pos"] + 1), 'rgb(250, 250, 250)', font=normal_font, spacing=10)
        ImageDraw.Draw(base).text((180, 170+t), l[i]["name"], 'rgb(0, 0, 0)', font=normal_font, spacing=10)
        stats1 = str(l[i]["place_pts"])
        ImageDraw.Draw(base).text((520, 170+t), stats1, 'rgb(0, 0, 0)', font=normal_font, spacing=10)
        stats2 = str(l[i]["kill_pts"])
        ImageDraw.Draw(base).text((580, 170+t), stats2, 'rgb(0, 0, 0)', font=normal_font, spacing=10)
        stats3 = str(l[i]["total_pts"])
        ImageDraw.Draw(base).text((650, 170+t), stats3, 'rgb(0, 0, 0)', font=normal_font, spacing=10)
        t+=44


    ImageDraw.Draw(base).rectangle([(720, 160), (1360, 200)], fill='rgb(252, 144, 3)')
    normal_font = ImageFont.truetype(font_path, 20)

    table_head = "#                 TEAMNAMES                                           POS     KILLS    TOTAL"
    ImageDraw.Draw(base).text((750, 170), table_head, 'rgb(0, 0, 0)', font=normal_font, spacing=10)

    t = 44
    s = 40
    l = teams


    for i in range(0, 13):
        ImageDraw.Draw(base).rectangle([(720, 160+t), (1360, 200+t)], fill='rgb(250, 250, 250)')
        
        t+=44
    ImageDraw.Draw(base).rectangle([(720, 160+44), (790, 772)], fill='rgb(23, 23, 23)')

    t = 44
    for i in range(13, 26):
        ImageDraw.Draw(base).text((750, 170+t), str(l[i]["pos"] + 1), 'rgb(250, 250, 250)', font=normal_font, spacing=10)
        ImageDraw.Draw(base).text((850, 170+t), l[i]["name"], 'rgb(0, 0, 0)', font=normal_font, spacing=10)
        stats1 = str(l[i]["place_pts"])
        ImageDraw.Draw(base).text((1180, 170+t), stats1, 'rgb(0, 0, 0)', font=normal_font, spacing=10)
        stats2 = str(l[i]["kill_pts"])
        ImageDraw.Draw(base).text((1240, 170+t), stats2, 'rgb(0, 0, 0)', font=normal_font, spacing=10)
        stats3 = str(l[i]["total_pts"])
        ImageDraw.Draw(base).text((1310, 170+t), stats3, 'rgb(0, 0, 0)', font=normal_font, spacing=10)
        t+=44

    buffer = io.BytesIO()
    base.save(buffer, format='PNG')
    # base.save('temp.png')

    # draw = ImageDraw.Draw(image)
    # draw.text((10, 10), 'Hello, Lambda!', font=font, fill='black')


    # image_data = io.BytesIO()
    # image.save(image_data, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Return the base64 encoded image
    return {
        'statusCode': 200,
        'body': json.dumps(
            {'image_base64': base64_image}
        ),
    }
