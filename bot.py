# -*- coding: utf-8 -*-

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request
import json
import imdb
import os
PORT = int(os.environ.get('PORT', 5000))
api_key = "5059b1d7" 
ia = imdb.IMDb() 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi! \nWelcome to the *IMDb Bot*. \nSend me the name of any movie or TV show to get its details. \nHappy viewing! \n \nCreated by [EveryDayEnjoy](https://everydayenjoy.com/)',parse_mode='markdown')

def dmca(update, context):
    update.message.reply_text('Hi! \nWe dont store any files on our *bot server !*\nEverything is auto embedded by 3rd party website. \n[Submit DMCA / Copyright Complain Here .](https://api.everydayenjoy.com/dmca)\nThanking You! \n ',parse_mode='markdown')

def help(update, context):
    update.message.reply_text('Send me the name of any movie to get its details. \nTry out "Avengers Endgame" \n For Dmca Use /dmca')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def reply(update, context):
    movie_name=update.message.text
    search = ia.search_movie(movie_name) 
      
    id='tt'+search[0].movieID
    
    url= 'http://www.omdbapi.com/?i='+id+'&apikey='+api_key
    
    x=urllib.request.urlopen(url)
    
    for line in x:
        x=line.decode()
    
    data=json.loads(x)
    
    ans=''
    ans+='*'+data['Title']+'* ('+data['Year']+')'+'\n\n'
    ans+='*IMDb Rating*: '+data['imdbRating']+'\n'
    ans+='*Title*: [#IMDb](https://www.imdb.com/title/'+data['imdbID']+')\n'
    ans+='*Released*: '+data['Released']+' \n'
    ans+='*Rated*: '+data['Rated']+' \n'
    ans+='*Runtime*: '+data['Runtime']+' \n'
    ans+='*Genre*: '+data['Genre']+'\n'
    ans+='*Cast*: '+data['Actors']+'\n'
    ans+='*Poster*: [#Images]('+data['Poster']+')\n\n'

    
    ans+='*Plot*: '+data['Plot']+'\n\n'
    
    ans+='[#Watch Movie Online](https://api.everydayenjoy.com/?title='+data['imdbID']+')\n\n'
    
    ans+='[#Download Movie](http://www.omdbapi.com/?i='+data['imdbID']+')\n\n'
    
    ans+='.\n\n'
    update.message.reply_text(ans,parse_mode='markdown')  


def main():

    updater = Updater("1787622148:AAHHN8r3db1UPdZ4GbpVNcL1Zl0o0tllGBM", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("dmca", dmca))
    dp.add_handler(MessageHandler(Filters.text, reply))
    dp.add_error_handler(error)

    #updater.start_webhook(listen="0.0.0.0",
    #                      port=int(PORT),
    #                      url_path="1787622148:AAHHN8r3db1UPdZ4GbpVNcL1Zl0o0tllGBM")
    #updater.bot.setWebhook('https://imdbvideo.herokuapp.com/' + "1787622148:AAHHN8r3db1UPdZ4GbpVNcL1Zl0o0tllGBM")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main() 
