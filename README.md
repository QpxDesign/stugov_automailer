# Better Daily Email

## About

This is a Python web-scraper (used with authorization from website operators) whose goal is to
automate the process of sending a daily email to the student body that contains information about
the lunch menu, scheduled athletic events, and club meetings. It uses ICS Feeds, along with basic
html scarping of one public webpage.

## Installation & Implementation

The only required file for download is Emailer.py, with emailtemplate.html existing as a convenience should
you ever need to change the design of the email. Emailer.py requires configuration to work, as EmailSender username
and password and email.send receivers and sender needs to be set. Also - you may want to change the email message, which
can be done inside emailtemplate.html (please note instructions for getting Emailer.py to use the new template, which can be found
at the top of emailtemplate.html). To Implementate the automated email sender, simply set a server to run Emailer.py once a day at a
given time. I suggest Heroku's dynos as an inexpensive and easy option. You can use basically any hardware for the server, but it has
only been tested on Unix and Windows.

## Credits

Developed By Quinn Patwardhan using open source software.

## Support

For any help, please email Quinn Patwardhan (quinn@qpxdesign.com).

## License:

Copyright 2022 by Quinn Patwardhan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
	
