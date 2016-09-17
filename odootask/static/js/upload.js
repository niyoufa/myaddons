$(function () {

    var image_path = "/api/image?id=";
    var default_image_path = "http://192.168.1.104:8500";
    // 选择并加载头像的内容
    $('#take_photo').fileupload({
        url: default_image_path + '/api/image/list',
        method:"POST",
        sequentialUploads: true,
        dataType: 'json',
        done: function (e, data) {
            var result = data.result.response;
            if (result['success'] != 1) {
                alert("上传失败");
            } else {
                console.log(result);
                var image = result.data[0];
                file_path = image.file_path;
                image_url = default_image_path + file_path;
                console.log(image_url);
                $("#media_content").html('<img  style="margin-right:10px;width:50px;height:50px;" src=' + image_url + '>');
            }
        }
    });

    $("#upload_good_info").click(function(){
        location.href = "/index.html" ; 
    });
});