function logout() {
    $.get("/user/logout/", function(data){
        if (data.code == '200') {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url: '/user/user_info/',
        dataType: 'json',
        type: 'GET',
        success:function (data) {
            // console.log(data);
            var imageUrl = '/static/media/'+ data.data.avatar + '/';
            $('#user-name').html(data.data.name);
            $('#user-mobile').html(data.data.phone);
            $('#user-avatar').attr('src', imageUrl);
        }
    })
});