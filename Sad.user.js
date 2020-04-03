// ==UserScript==
// @name         Sad Page
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  🕯️愿逝者安息，愿生者奋发，愿祖国昌盛！🕯️
// @author       You
// @include *
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var style = document.createElement("style");
style.type = "text/css";
var text = document.createTextNode(`html {
        -webkit-filter: grayscale(100%);
        -moz-filter: grayscale(100%);
        -ms-filter: grayscale(100%);
        -o-filter: grayscale(100%);
        filter:progid:DXImageTransform.Microsoft.BasicImage(grayscale=1);
        _filter:none;
    }`);
style.appendChild(text);
var head = document.getElementsByTagName("head")[0];
    console.log(head)
head.appendChild(style);



    // Your code here...
})();