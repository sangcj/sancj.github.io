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

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-accept").on("click", function(){
        // console.log(121);
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-accept").attr("order-id", orderId);
    });

    $('.modal-accept').on('click', function () {
       // 确定接单
        var order_id = $(this).attr('order-id');
        $.ajax({
            url: '/user/take_order/',
            type: 'PATCH',
            dataType: 'json',
            data: {'order_id': order_id, 'status': 'accept'},
            success:function (data) {
                // alert(121)
                var order_accept_id = '#order-accept' + order_id;
                var order_reject_id = '#order-reject' + order_id;
                $(order_accept_id).hide();
                $(order_reject_id).hide();
                location.href = '/user/lorders/'
            }
        });
    });

    $(".order-reject").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-reject").attr("order-id", orderId);
    });

        // 确定拒单
    $('.modal-reject').on('click', function () {
        var order_id = $(this).attr('order-id');
        var reject_reason = $('#reject-reason').val();
        $.ajax({
            url: '/user/take_order/',
            type: 'PATCH',
            dataType: 'json',
            data: {'order_id': order_id, 'reject_reason': reject_reason, 'status': 'reject'},
            success: function (data) {
                // alert(121)
                if(data.code == 200){
                    var order_accept_id = '#order-accept' + order_id;
                    var order_reject_id = '#order-reject' + order_id;
                    $(order_accept_id).hide();
                    $(order_reject_id).hide();
                    location.href = '/user/lorders/'
                }
                if(data.code == 1019){
                    alert(data.msg)
                    location.href = '/user/lorders/'
                }
            }
        })
    })
});