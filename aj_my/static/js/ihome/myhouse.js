function setLi(item){
    var li =  '<a href="/house/detail/?house_id='+ item.id +'">\n' +
            '                            <div class="house-title">\n' +
            '                                <h3>房屋ID: '+ item.id +' —— '+ item.title +'</h3>\n' +
            '                            </div>\n' +
            '                            <div class="house-content">\n' +
            '                                <img src="/static/images/'+ item.image +'/">\n' +
            '                                <div class="house-text">\n' +
            '                                    <ul>\n' +
            '                                        <li>位于：\n' +
                                                                item.area +
            '                                        </li>\n' +
            '                                        <li>价格：￥'+ item.price +'/晚</li>\n' +
            '                                        <li>发布时间：'+ item.create_time +'</li>\n' +
            '                                    </ul>\n' +
            '                                </div>\n' +
            '                            </div>\n' +
            '                        </a>';
    return li
}


$(document).ready(function(){
    $.get('/user/user_info/', function (data) {
        // console.log(121);
        if(data.code == 1014){
            // console.log(121);
            $('.auth-warn').hide();
            var my_house_html = '';
            var other_house_html = '';
            var houses_list = data.houses_list;
            // console.log(houses_list);
            for(var index=0;index<houses_list.length;index++){
                // console.log(8888);
                // console.log(data.data.id);
                // console.log(houses_list[index].user_id);
                // console.log(8888);
                if(data.data.id == houses_list[index].user_id) {
                    my_house_html += setLi(houses_list[index]);
                    // console.log(my_house_html)
                }else {
                    other_house_html += setLi(houses_list[index]);
                    // console.log(houses_list[index])
                }
            }
            if(!my_house_html){
                $('#my-house span').text('当前未发布房源!');
            }else {
                $('#my-house').html(my_house_html);
            }
            if(!other_house_html){
                $('#other-house span').text('当前无用户发布房源');
            }else {
                $('#other-house').html(other_house_html);
            }
        }
        if(data.code == 200){
            $('#houses2').show();
            $('#houses-list').hide();
        }
    })
});