const watermark=document.querySelector(".watermark");

if(watermark){

setInterval(function(){

watermark.style.left=Math.random()*70+"%";

watermark.style.top=Math.random()*70+"%";

},8000);

}