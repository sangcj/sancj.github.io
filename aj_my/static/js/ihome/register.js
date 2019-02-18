// function getCookie(name) {
//     var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     return r ? r[1] : undefined;
// }
//
// var imageCodeId = "";
//
// function generateUUID() {
//     var d = new Date().getTime();
//     if(window.performance && typeof window.performance.now === "function"){
//         d += performance.now(); //use high-precision timer if available
//     }
//     var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
//         var r = (d + Math.random()*16)%16 | 0;
//         d = Math.floor(d/16);
//         return (c=='x' ? r : (r&0x3|0x8)).toString(16);
//     });
//     return uuid;
// }

function generateImageCode() {
    // 获取验证码并渲染页面
    // do {
    //     var num = parseInt(Math.random()*10000)
    // }while (num<999);
    // $('.image-code p').text(num)
    $.ajax({
        url: '/user/code/',
        dataType: 'json',
        type: 'GET',
        success:function (data) {
        //    渲染验证码
        //     console.log(data);
            $('.image-code p').text(data.data);
        //    TODO:将字符串生成图片
        }
    })
}

$(document).ready(function() {
    //阻止表单提，使用ajax
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        imagecode = $("#imagecode").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();
        numbercode1 = $("#imagecode").val();
        numbercode2 = $(".image-code p").text();
        // console.log(numbercode1, numbercode2);
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            //阻止提交
            // e.preventDefault();
            return;
        }
        // if (!phoneCode) {
        //     $("#phone-code-err span").html("请填写短信验证码！");
        //     $("#phone-code-err").show();
        //     return;
        // }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            // e.preventDefault();
            return;
        }
        if (numbercode1 != numbercode2) {
            $("#image-code-err span").html("验证码错误!");
            $("#image-code-err").show();
            // e.preventDefault();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            // e.preventDefault();
            return;
        }
    //    异步提交注册请求，ajax
        $.ajax({
            url:'/user/register/',
            type:'POST',
            dataType:'json',
            data:{'mobile': mobile, 'imagecode': imagecode, 'passwd':passwd, 'passwd2':passwd2},
            success:function (data) {
                // alert('ok');
                if(data.code == '1001'){
                     $("#image-code-err span").html(data.msg);
                     $("#image-code-err").show();
                }if(data.code == '1002'){
                     $("#mobile-err span").html(data.msg);
                     $("#mobile-err").show();
                }
                if(data.code == '1003'){
                     $("#image-code-err span").html(data.msg);
                     $("#image-code-err").show();
                }
                if(data.code == '1004'){
                     $("#password2-err span").html(data.msg);
                     $("#password2-err").show();
                }if(data.code == '1005'){
                     $("#mobile-err span").html(data.msg);
                     $("#mobile-err").show();
                }
               if(data.code == '200'){
               //    页面跳转
                   location.href = '/user/login/'
               }
            },
            error:function (data) {
                alert('error')
            }
        })
    });
});