//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/house/search/?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    var areaName = $(th).attr("area-name");
    if (undefined == areaName) areaName="";
    url += ("aname=" + areaName);
    url += "&";
    url += ("sd=" + $(th).attr("start-date"));
    url += "&";
    url += ("ed=" + $(th).attr("end-date"));
    location.href = url;
}


function a(){
    // console.log('121')
        $.ajax({
        url: '/index/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // console.log(data);
            var all_house_msg = data.all_house_msg;
            var html = '';
            for(var index=0;index<all_house_msg.length;index++) {
                html += setDiv(all_house_msg[index])
                // console.log(setDiv(all_house_msg[index]));
                // console.log(all_house_msg[index].house_title);
            }
            // console.log(html);
            $('.swiper-wrapper').html(html);
            //轮播
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationClickable: true
            });

            var area_html = '';
            // console.log(data.area);
            var area_dict = data.area;
            for(var i=0;i<area_dict.length;i++){
                // console.log(area_dict[i].id);
                area_html += '<a href="#" area-id="'+ area_dict[i].id +'">'+ area_dict[i].name +'</a>'
            }
            $('.area-list').html(area_html);
            $(".area-list a").click(function(e){
                // alert($(this).text());
                $("#area-btn").text($(this).text());
                $(".search-btn").attr("area-id", $(this).attr("area-id"));
                $(".search-btn").attr("area-name", $(this).html());
                $("#area-modal").modal("hide");
            });

            if(data.code == 200){
                $('.register-login').html(
                    '<a class="btn top-btn btn-theme" href="/user/my/" style="width: 100%">'+ data.user_phone +'</a>'
                );
            }
        }
    });
}


function setDiv(item){
    div = '<div class="swiper-slide">\n' +
        '                        <a href="/house/detail/?house_id='+ item.house_id +'"><img src="/static/images/'+ item.house_image +'/"></a>\n' +
        '                        <div class="slide-title">\n' +
        '                            '+ item.house_title +'\n' +
        '                        </div>\n' +
        '                    </div>';
    return div
}


$(document).ready(function(){
    a();
    $(".top-bar>.register-login").show();
    // var mySwiper = new Swiper ('.swiper-container', {
    //     loop: true,
    //     autoplay: 2000,
    //     autoplayDisableOnInteraction: false,
    //     pagination: '.swiper-pagination',
    //     paginationClickable: true
    // });
    // $(".area-list a").click(function(e){
    //     alert($(this).text());
    //     $("#area-btn").text($(this).text());
    //     $(".search-btn").attr("area-id", $(this).attr("area-id"));
    //     $(".search-btn").attr("area-name", $(this).html());
    //     $("#area-modal").modal("hide");
    // });
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });
});