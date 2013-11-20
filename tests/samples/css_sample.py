# -*- coding: utf-8 -*-
css_sample = """
@import '/css/file1.css ';
@import "/css/file2.css    ";
@import    "/css/file3.css";
@import
   "/css/file4.css";
@import "/css/file5.css"    ;
@import "/css/file6.css'    ;
body {
    font-family: monospace;
    margin: 0;
    padding: 0;
}
img {
    max-width: 100%;
}
article, header {
    margin: 0 auto;
    max-width: 500px;
    padding: 0 5%;
    position: relative;
}
header {
    padding-top: 5%;
    padding-bottom: 2%;
    background: url(/img/file1.png);
}
h1 {
    font-weight: normal;
    margin: 0;
    position: absolute;
    top: 60px;
    background: url("/img/file2.png");

}
h1 span {
    background-color: rgba(255, 255, 255, 0.75);
    padding: 0 10px;
    background: url('/img/file3.png');
}
a {
    color: #08C;
    text-decoration: none;
    background: url( /img/file4.png );
}
a:hover {
    text-decoration: underline;
    background: url(    "/img/file5.png    ");
}
blockquote {
    font-style: italic;
    margin: 0;
    padding: 0 5%;
    background: url(
        '/img/file6.png'
    );
}
.contact, .contact a, .legal {
    color: #707070;
    background: url('/img/file7.png);
    font-size: 12px;
}
"""
