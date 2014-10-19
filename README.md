Pancake HipChat bot
============
Simple bot created for fun. There is also the unsupported [version](https://github.com/idooo/pancake-campfire-bot) for Campfire

#### Install and run

```
pip install -r requirements.txt
./pancake.py -c example.conf
```
Also you need to create an API key in HipChat administration panel and paste it in Pancake config file.
Please note: it must be HipChat API version 1 key.

#### Plugins:
There are some builtin plugins enabled by default:

+ get random cat gif (http://thecatapi.com)
+ get staging servers status
+ get random Chuck's geek phrase (http://api.icndb.com)
+ get random pony picture (http://ponyfac.es/)
+ play Rock-Paper-Scissors-Lizard-Spock
+ blame somebody
+ roll number from 0 to 100
+ get random Arnold Schwarzenegger's phrase
+ get random XKCD comics (http://xkcd.com/xxxx/info.0.json)
+ get random gif by keyword (http://api.giphy.com/)
+ get random LEGO Movie quotes
+ ask bot a question

Type `/help` to see all available commands and detailed description

#### Plugins development
To create a plugin simply create python file in `/plugins` directory like `awesome.py` or create a subfolder there with `__init__.py` file like `/awesome/__init__.py`. This will be a main file for your plugin.

Then you will need to create a plugin class in the main plugin file. The plugin class must have two attributes: `command` and `help` and method `response`.

The `command` attribute will be used to bind the plugin. Each time Pancake will see `/<command>` in chat room, it will execute `response` method of your plugin.

If you want to add any configuration parameters you will need to create a constructor for your class with `conf` argument like `def __init__(self, conf)`. Plugin loader will inject the configuration from the `.conf` file specified during Pancake launch. For example you can have a look on `plugins/geckoboard.py`.

###### `response` method
Your plugin must have `response` method which can be static or not. Message which contains the command you specified as an argument for your plugin class will trigger execution of `response` method. 

Plugin loader will inject arguments you specified for this method. The list of arguments that can be injected:

+ `room` - room name where triggered action appeared
+ `author_id` - the id of author who posted message which triggered the action
+ `author` - message author’s name 
+ `message` - the message itself that triggered the action
+ `random_user` - random user in the room (@username)
+ `mentioned_user` - the first mentioned user in the message that triggered the action

`response` method must return value. It can be a string (single message) or list (array of message to post). This value will be posted to HipChat room by Pancake bot.  

Example:

```
def response(message, author):
    formattedMessage = self.doSomethingWithMessage(message)
    ...
    if somethingWrong:
        return author + ‘, something wrong!’
	
	return formattedMessage

```

### License

##### The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

