# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 20:24:17 2020

@author: karan
"""
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request
import json
import imdb
import os
PORT = int(os.environ.get('PORT', 5000))
api_key='7d852108'
ia = imdb.IMDb() 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def reply(update, context):
    """Echo the user message."""
    movie_name=update.message.text
    search = ia.search_movie(movie_name) 
      
    id='tt'+search[0].movieID
    
    url= 'http://www.omdbapi.com/?i='+id+'&apikey='+api_key
    
    x=urllib.request.urlopen(url)
    
    for line in x:
        x=line.decode()
    
    data=json.loads(x)
    
    ans=''
    ans+='*'+data['Title']+'* ('+data['Year']+')'+'\n'
    ans+='IMDb Rating: '+'*'+data['imdbRating']+'* \n'
    ans+='Cast: '+data['Actors']+'\n'
    ans+='Genre: '+data['Genre']+'\n'
    ans+='[.]('+data['Poster']+')'
    update.message.reply_text(ans,parse_mode='markdown')  


def main():

    updater = Updater("1476373283:AAHrdQE394_J8qd78J974y_AwVdwrsis1r0", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, reply))
    dp.add_error_handler(error)

    #updater.start_webhook(listen="0.0.0.0",
    #                      port=int(PORT),
    #                      url_path="1476373283:AAHrdQE394_J8qd78J974y_AwVdwrsis1r0")
    #updater.bot.setWebhook('https://imdb-movie-bot.herokuapp.com/' + "1476373283:AAHrdQE394_J8qd78J974y_AwVdwrsis1r0")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main() 