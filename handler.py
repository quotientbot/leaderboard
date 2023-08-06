import json
import io
import base64
from PIL import Image, ImageDraw, ImageFont

# This function calculates the correct x, y position of the text so that it is centered w.r.t. the image
def calc_dimensions(text, font):
    img = Image.open("test.png").resize((1400,788) ,Image.ANTIALIAS)
    draw = ImageDraw.Draw(img)
    width, height = 1400, 788
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    return text_x, text_y


def generate(event, context):
    '''
    This function generates the image of the leaderboard and returns it as a base64 encoded string.

    The parameters are sent as a JSON object in the body of the request.

    The parameters are::

    1. title - The title of the image - string
    2. subtitle - The subtitle of the image - string
    3. teams - The teams to be displayed in the image - list of dictionaries
    The teams dictionary should be of the following format:
        {   
            "title": "title",
            "subtitle": "subtitle",
            "background_url": null,
            "teams": [
                        {"pos": 0, "name": "0-team", "place_pts": 6, "kill_pts": 4, "total_pts": 9}, 
                        {"pos": 1, "name": "1-", "place_pts": 5, "kill_pts": 1, "total_pts": 1},
                        ...
                    ]
        }
}
    '''
    font_path = 'calibrib.ttf'  # The font file will be available at this path inside Lambda

    # Get the parameters from the context(event) that was sent
    title = json.loads(event["body"]).get('title')  # The title of the image - string
    subtitle = json.loads(event["body"]).get('subtitle')    # The subtitle of the image - string
    teams = json.loads(event["body"]).get('teams')  # The subtitle of the image - list of dictionaries


    # Create a new image
    base = Image.new('RGB', (1400, 788), color='black')

    # Load the font
    try:
        title_text_1 = ImageFont.truetype(font_path, 80)
        title_text_2 = ImageFont.truetype(font_path, 90)
    except IOError:
        return {
            'statusCode': 500,
            'body': json.dumps('Unable to load the custom font.'),
        }

    # Draw the text title and subtitle on the image
    text_x, text_y = calc_dimensions(title, title_text_1)   # Calculate the correct x, y position of the text so that it is centered
    ImageDraw.Draw(base).text((text_x+5, 5+5), title, 'rgb(235, 146, 52)', font=title_text_1, spacing=10)   #orange text
    ImageDraw.Draw(base).text((text_x+3, 5+3), title, 'rgb(0, 0, 0)', font=title_text_1, spacing=10)    #black text
    ImageDraw.Draw(base).text((text_x, 5), title, 'rgb(255, 255, 255)', font=title_text_1, spacing=10)  #white text

    text_x, text_y = calc_dimensions(subtitle, title_text_2)    # Calculate the correct x, y position of the text so that it is centered
    ImageDraw.Draw(base).text((text_x+5, 65+5), subtitle, 'rgb(235, 146, 52)', font=title_text_2, spacing=10)   #orange text
    ImageDraw.Draw(base).text((text_x+3, 65+3), subtitle, 'rgb(0, 0, 0)', font=title_text_2, spacing=10)    #black text
    ImageDraw.Draw(base).text((text_x, 65), subtitle, 'rgb(255, 255, 255)', font=title_text_2, spacing=10)  #white text


    # Left column header drawn
    ImageDraw.Draw(base).rectangle([(60, 160), (700, 200)], fill='rgb(252, 144, 3)')    #orange header
    normal_font = ImageFont.truetype(font_path, 20) #font style/size
    table_head = "#                 TEAMNAMES                                           POS     KILLS    TOTAL" #header text
    ImageDraw.Draw(base).text((90, 170), table_head, 'rgb(0, 0, 0)', font=normal_font, spacing=10) #header text drawn

    # Pixels to move down for each row
    t = 44
    l = teams

    # Draw the rows - white rectangles of left table
    for i in range(0, 13):
        ImageDraw.Draw(base).rectangle([(60, 160+t), (700, 200+t)], fill='rgb(250, 250, 250)')
        t+=44

    # Draw the black column in the first column (#) of left table
    ImageDraw.Draw(base).rectangle([(60, 160+44), (130, 772)], fill='rgb(23, 23, 23)')

    # Draw the text in the first column (#) of left table
    t = 44
    for i in range(0, 13):
        ImageDraw.Draw(base).text((90, 170+t), str(l[i]["pos"] + 1), 'rgb(250, 250, 250)', font=normal_font, spacing=10)    #pos
        ImageDraw.Draw(base).text((180, 170+t), l[i]["name"], 'rgb(0, 0, 0)', font=normal_font, spacing=10)  #name
        #stats displayed
        stats1 = str(l[i]["place_pts"])
        ImageDraw.Draw(base).text((520, 170+t), stats1, 'rgb(0, 0, 0)', font=normal_font, spacing=10) #place points
        stats2 = str(l[i]["kill_pts"])
        ImageDraw.Draw(base).text((580, 170+t), stats2, 'rgb(0, 0, 0)', font=normal_font, spacing=10) #kill points
        stats3 = str(l[i]["total_pts"])
        ImageDraw.Draw(base).text((650, 170+t), stats3, 'rgb(0, 0, 0)', font=normal_font, spacing=10) #total points
        t+=44


    # Right column header drawn
    ImageDraw.Draw(base).rectangle([(720, 160), (1360, 200)], fill='rgb(252, 144, 3)')  #orange header
    normal_font = ImageFont.truetype(font_path, 20) #font style/size
    table_head = "#                 TEAMNAMES                                           POS     KILLS    TOTAL" #header text
    ImageDraw.Draw(base).text((750, 170), table_head, 'rgb(0, 0, 0)', font=normal_font, spacing=10) #header text drawn


    # Pixels to move down for each row
    t = 44

    # Draw the rows - white rectangles of right table
    for i in range(0, 13):
        ImageDraw.Draw(base).rectangle([(720, 160+t), (1360, 200+t)], fill='rgb(250, 250, 250)')
        t+=44
    
    # Draw the black column in the first column (#) of right table
    ImageDraw.Draw(base).rectangle([(720, 160+44), (790, 772)], fill='rgb(23, 23, 23)')

    # Draw the text in the right table
    t = 44
    for i in range(13, 26):
        ImageDraw.Draw(base).text((750, 170+t), str(l[i]["pos"] + 1), 'rgb(250, 250, 250)', font=normal_font, spacing=10)   #pos
        ImageDraw.Draw(base).text((850, 170+t), l[i]["name"], 'rgb(0, 0, 0)', font=normal_font, spacing=10) #name
        stats1 = str(l[i]["place_pts"])
        ImageDraw.Draw(base).text((1180, 170+t), stats1, 'rgb(0, 0, 0)', font=normal_font, spacing=10) #place points
        stats2 = str(l[i]["kill_pts"])
        ImageDraw.Draw(base).text((1240, 170+t), stats2, 'rgb(0, 0, 0)', font=normal_font, spacing=10) #kill points
        stats3 = str(l[i]["total_pts"])
        ImageDraw.Draw(base).text((1310, 170+t), stats3, 'rgb(0, 0, 0)', font=normal_font, spacing=10) #total points
        t+=44

    # Save the image to a buffer
    buffer = io.BytesIO()
    base.save(buffer, format='PNG')

    # Convert the image to base64
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Return the base64 encoded image
    return {
        'statusCode': 200,
        'body': json.dumps(
            {'image_base64': base64_image}
        ),
    }
