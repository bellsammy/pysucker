# -*- coding: utf-8 -*-
html_sample = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
        <title>new_file</title>
        <meta name="description" content="" />
        <meta name="author" content="Grégoire VIGNERON" />
        <meta name="viewport" content="width=device-width; initial-scale=1.0" />
        <link rel="shortcut icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="stylesheet" href="/apple-touch-icon.png" />
        <link rel="invalid"/>
        <script type="text/javascript" src="/script1.js"></script>
        <script>
   function utmx_section(){}function utmx(){}
(function(){var k='0172792736',d=document,l=d.location,c=d.cookie;function f(n){
if(c){var i=c.indexOf(n+'=');if(i&gt;-1){var j=c.indexOf(';',i);return escape(c.substring(i+n.
length+1,j&lt;0?c.length:j))}}}var x=f('__utmx'),xx=f('__utmxx'),h=l.hash;
d.write('&lt;sc'+'ript src="'+
'http'+(l.protocol=='https:'?'s://ssl':'://www')+'.google-analytics.com'
+'/siteopt.js?v=1&amp;utmxkey='+k+'&amp;utmx='+(x?x:'')+'&amp;utmxx='+(xx?xx:'')+'&amp;utmxtime='
+new Date().valueOf()+(h?'&amp;utmxhash='+escape(h.substr(1)):'')+
'" type="text/javascript" charset="utf-8"&gt;&lt;/sc'+'ript&gt;')})();
  </script>
    </head>
    <body>
        <form name="loginform" method="post" action="http://login.spray.se/date">
            <input id="login_username" name="username" type="text" class="text_input" tabindex="1" placeholder="E-postadress">
            <input id="login_password" name="password" type="password" class="text_input" placeholder="Lösenord" tabindex="2">
            <input type="hidden" name="ref" value="1">
            <input class="submit" type="submit" value="Logga in" tabindex="3">
        </form>
        <form id="reminderForm" name="reminderForm" method="post" action="">
            <label for="">Ange den e-post du registrerade dig med</label>
            <input type="text" name="input" id="forgotInput">
            <input id="submit" type="submit" class="button" value="Hämta" name="submit">
        </form>
        <form name="register_form" method="post" action="/registrera/">
            <input type="hidden" name="register_step1" value="1">
            <input type="hidden" name="stickyUser" id="stickyUser" value="">
        </form>
        <div>
            <header>
                <img src="/image1.png"/>
                <h1>new_file</h1>
            </header>
            <style>
                .test {background-image: url(/background.png)}
            </style>
            <nav>
                <p>
                    <a href="/file1.html ">Home</a>
                </p>
                <p>
                    <a href="/file2.html">Contact</a>
                </p>
            </nav>
            <div>
                <a title="invalid">
                <img src="/image2.png    "/>
                </a>
            </div>
            <footer>
                <p>
                    &copy; Copyright  by Grégoire VIGNERON
                </p>
            </footer>
        </div>
        <script>
            var url1 = "/inline-js-file.html"
        </script>
    </body>
<script type="text/javascript" src="/script2.js"></script>
</html>
"""
