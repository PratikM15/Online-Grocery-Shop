$(document).ready(function() {
        $('.food-slider').slick({
                autoplay:true,
                slidesToShow:3,
                slidesToScroll:1,
                prevArrow:".prev-btn",
                nextArrow:".next-btn",
            
        });
});
let c = setInterval(showTime,1000);
function showTime(){

        let date = new Date();
        
        let hours = date.getHours();
        let minutes = date.getMinutes();
        let seconds = date.getSeconds();

document.getElementById('hours').innerHTML = hours;
document.getElementById('minutes').innerHTML = minutes;
document.getElementById('seconds').innerHTML = seconds;
}
