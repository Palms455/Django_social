(function(){
 if (window.myBookmarklet !== undefined){
 myBookmarklet();
 }
 else {
 document.body.appendChild(
 document.createElement('script')
 ).src='https://1a110c0f21b6.ngrok.io/static/js/bookmarklet.js?r=' +
 Math.floor(Math.random()*99999999999999999999);
 }
})();