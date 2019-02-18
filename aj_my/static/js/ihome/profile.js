function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $("#a4").focus(function(){
        $(".error-msg").hide();
    });
    $("#user-name").focus(function(){
        $(".error-msg").hide();
    });
    $.ajax({
       url: '/user/user_info/',
       type: 'GET',
       dataType: 'json',
       success:function (data) {
           // console.log(data);
           if(data.data.avatar){
               $('.menu-title img').attr('src', '/static/media/'+ data.data.avatar + '/')
           }else {
               $('.menu-title img').hide();
               $('#a1').text('当前未设置用户头像')
           }
           $('#a2').text(data.data.name)
       }
    });

    // console.log('1');
    $('#form-avatar').submit(function (e) {
        // console.log('2');
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/user/profile/',
            dataType: 'json',
            type: 'PATCH',
            success:function (data) {
                // console.log('3')
                if(data.code == 200){
                    location.href = '/user/profile/'
                }
                if(data.code == 1010){
                    $('#a3 span').text(data.msg);
                    $('#a3').show();
                }
            }
        })
    })

    $('#form-name').submit(function (e) {
        e.preventDefault();
        var name = $('#user-name').val();
        $.ajax({
            url: '/user/name_profile/',
            type: 'POST',
            dataType: 'json',
            data: {'new_name': name},
            success:function (data) {
                // console.log(121)
                if(data.code == 1011){
                    $('#a5 span').text(data.msg);
                    $('#a5').show();
                }
                if(data.code == 1012){
                    $('#a5 span').text(data.msg);
                    $('#a5').show();
                }
                if(data.code == 200){
                    location.href = '/user/profile/'
                }
            }
        })
    })
});
