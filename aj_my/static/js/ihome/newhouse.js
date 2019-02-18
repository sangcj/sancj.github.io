function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $.ajax({
        url: '/index/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var area_html = '';
            // console.log(data.area);
            var area_dict = data.area;
            for(var i=0;i<area_dict.length;i++){
                // console.log(area_dict[i].id);
                // area_html += '<a href="#" area-id="'+ area_dict[i].id +'">'+ area_dict[i].name +'</a>'
                area_html += '<option value="'+ area_dict[i].id +'">'+ area_dict[i].name +'</option>'
            }
            // console.log(area_dict);
            $('#area-id').html(area_html);

            var facility_html = '';
            var all_facility_dict = data.all_facility;
            for(var i=0;i<all_facility_dict.length;i++){
                // console.log(i)
                facility_html += '<li>\n' +
                    '                                <div class="checkbox">\n' +
                    '                                     <label>\n' +
                    '                                          <input type="checkbox" name="facility" value="'+ all_facility_dict[i].id +'">'+ all_facility_dict[i].name +'\n' +
                    '                                     </label>\n' +
                    '                                </div>\n' +
                    '                            </li>'
            }
            // console.log(area_dict);
            $('.house-facility-list').html(facility_html);
        }
    });

    $('#form-house-info').submit(function (e) {
        // console.log('122');
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/house/newhouse/',
            type: 'POST',
            dataType: 'json',
            success:function (data) {
                // console.log('122')
                if(data.code == 200){
                    // console.log('121')
                    location.href = '/user/myhouse/'
                }
                if(data.code == 1016){
                    // console.log(data.msg)
                    $('.text-center span').text(data.msg);
                    $('.text-center').show();
                }
            }
        })
    })
});