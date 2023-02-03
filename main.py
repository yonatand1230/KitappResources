import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import BotCommand, ReplyKeyboardMarkup
import json
import bs4
import requests 
from urllib.request import urlopen, quote
from time import sleep

def scrap(n):
    url = "https://www.movieland-cinema.co.il/api/Events"
    response = urlopen(url)
    data = json.loads(response.read())

    #######################
    ### GET DESCRIPTION ###
    #######################

    movies = {} #new dict, contains name+id for every movie

    for i in data:
        movies[i['Name']] = i['MovieId'] #in the new dict insert movie name (key) and id (value)

    if movies.get(n) != None:
        # Movie found - everything's ok
        url = "https://www.movieland-cinema.co.il/movie/" + str(movies.get(n))


        response = requests.get(url)
        page = bs4.BeautifulSoup(response.text, features="lxml")
        desc = page.find('meta', {"name":"og:description"})['content'] #scrap description from html

        desc = desc.replace('<p>','').replace('</p>','') #remove html tags <p> and </p>

        htmlCodes = (
                ("'", '&#39;'),
                ('"', '&quot;'),
                ('>', '&gt;'),
                ('<', '&lt;'),
                ('&', '&amp;')
            )

        for code in htmlCodes:
            desc = desc.replace(code[1], code[0]) #decode special characters
        
        #######################
        #### GET ENG-NAME, ####
        #### RELEASE DATE, ####
        ### DIRECTOR & CAST ###
        #######################
        
        span = page.find('div', {'class':'rtl-wrapper'}).find('div',{'class':'main-container page-top-margin','id':'change-bg','tabindex':'-1'}).find('div', {'class':'product-pagee movieid product-pagee-mob movie-page','data-movieid':str(movies.get(n))}).find('div',{'class':'container','style':'margin-top:2.813rem;'}).find('div', {'class':'row mt-3'}).find('div',{'class':"col-12 col-sm-8 col-md-8 col-lg-9"}).find('div', {'class':"pg-description mr-40"}).find('div',{'class':'bg-more text-left'}).find('div',{'class':'bg-more-b'}).get_text()
        engname = span.splitlines()[2]

        date = (span.splitlines()[3])[13:]

        director = span.splitlines()[4]
        director = director.replace("בימוי:","**בימוי:**")
        cast = span.splitlines()[5]
        cast = cast.replace("שחקנים:","**שחקנים:**")

        #######################
        ###### GET GENRE ######
        #######################

        movies_index = {}

        for i in range(0,len(data)):
            movies_index[data[i]['Name']] = i

        index = movies_index[n]
        genres = data[index].get('Genres')



        #######################
        ##### GET POSTER ######
        #######################

        poster = "https://movieland-cinema.co.il/images/" + quote(data[index].get('Pic'))


        info = {
            "genres":genres,
            "description":desc,
            "poster":poster,
            "eng_name":engname,
            "date":date,
            "director":director,
            "cast":cast
        }

        return info
    else:
        heb_name=None
        eng_name=None
        
        return {
            "genres":"תקלה - הסרט לא נמצא!",
            "description":'הסרט "'+n+'" לא נמצא. נסה שוב.',
            "poster":None, 
            "eng_name":"error",
            "data":"error"
        }
        


Bot_token = '5921511328:AAFrugT7oa8Iad4-cW2-Uo9F8cIzGV5iL-c'

app = Client(
    name="MovieDatesBot",
    bot_token=Bot_token
    )


heb = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י','כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
eng = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
nums = ['1','2','3','4','5','6','7','8','9','0']


app.start()
print("bot started!")


heb_name = ''
eng_name = ''
genre = ''
desc = ''
us_date = ''
il_date = ''


def finalpost(heb, eng, gen, des, date, poster, dirctr, cst):
    if poster !=None:
        usdate = date.split('/')
        usdate[0] = str(int(usdate[0])+1)
        
        if len(usdate[0])==1:
            usdate[0] = "0"+usdate[0]
        
        usdate = usdate[0]+'/'+usdate[1]+'/'+usdate[2]
        
        msg = "**🎬 " + heb + " (2023) " + eng + " 🎬**\n" + "\n**ז'אנר:** " + gen + "\n"+dirctr + "\n"+cst + "\n\n**תקציר:**\n" + des + '\n--תאריך יציאה לקולנוע:--\n🇮🇱 - ' + date + '\n🇺🇸 - ' + usdate + "\n--תאריך יציאה לרשת:--\n**Digital** - \n**BluRay** -"
        chat = -1001768820808
        
        if len(msg)>1024:
            app.send_message(-1001873632278, 'הפוסט לסרט **'+heb+'** ארוך מדי - הפוסטר יישלח בנפרד')
            app.send_photo(chat, poster)
            app.send_message(chat, msg)
        else:
            post = app.send_photo(chat, poster, caption=msg)
            app.send_message(-1001873632278, "הפוסט לסרט **" + heb + "** נשלח בערוץ ההכנות!")
    else:
        app.send_message(-1001873632278, 'שגיאה - הסרט לא נמצא')
    
    # delete all variables for another use:
    data=None
    heb_name=None
    eng_name=None
    genre=None
    desc=None
    us_date=None
    il_date=None



@app.on_message(filters.command('test'))
async def test(client, message):
    replies = [None]
    await message.reply_text(text="test", reply_markup=ReplyKeyboardMarkup([replies]))

@app.on_message(filters.command("חדש"))
async def hi_cmd(client, message):

    if message.chat.id == -1001873632278 or True: 
        year_prompt = await message.reply("בוא נכין הודעה חדשה")
        
        url = "https://www.movieland-cinema.co.il/api/Events"
        response = urlopen(url)
        data = json.loads(response.read())

        movies = [None]*len(data)
        
        for i in range(0,len(data)):
            movies[i] = data[i].get('Name')

        replies = [[None]*len(data)]
        
        for i in movies:
            replies.append([i])
        
        replies = replies[1:]
        print(replies)
        await message.reply_text(text="מה שם הסרט? (היעזר בכפתורים)", reply_markup=ReplyKeyboardMarkup(replies))
        
        # step 1: get hebrew name
        # step 2: get english name
        # step 3: get genre
        # step 4: get description
        # step 5: get us date
        # step 6: get il date


        @app.on_message()
        def get_hebname(client2, message2):
            global heb_name
            global eng_name, genre, desc, us_date, il_date
            
            for i in heb:
                if message2.text[0] == i: #step 1 - heb name (is hebrew && heb name not defined)
                    heb_name = message2.text
                    print('heb name: '+heb_name)
                    message2.reply("מכין את הפוסט לסרט **" + heb_name + "**...")
                    
                    global data
                    data = scrap(heb_name)
                    
                    genre = data.get('genres')
                    genre = genre.replace(',','').replace(' ', ' #')
                    genre = '#' + genre
                    
                    print('genre: '+genre)
                    
                    eng_name = data.get('eng_name')
                    print('eng name: '+eng_name)
                    
                    desc = data.get('description')
                    print('description:\n'+desc)
                                    
                    poster = data.get('poster')
                    print("poster: "+str(poster))
                    
                    date = data.get('date')
                    print("date: "+ str(date))
                    
                    director = data.get('director')
                    print('director: '+director)
                    
                    cast = data.get('cast')
                    print('cast: '+cast)
                    
                    if date!=None:
                        finalpost(heb_name, eng_name, genre, desc, date, poster, director, cast)
                    
                    
                
            
            for i in nums: 
                if message2.text[0] == i: #
                    date = message2.text.replace('.','/')
    else:
        reply = await message.reply("אינך מורשה להשתמש בבוט!")


idle()