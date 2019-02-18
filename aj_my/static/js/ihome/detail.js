function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    $(".book-house").show();

    // 获取key，value
    var adr = location.search;
    console.log(adr);
    var house_id = adr.split('=')[1];
    console.log(house_id);
    $.ajax({
        url: '/house/detail_info/',
        type: 'POST',
        dataType: 'json',
        data: {'house_id': house_id},
        success:function (data) {
            console.log(data)
        }
    })
});