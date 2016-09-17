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
                $("#media_content").html('<img  id="image_url" style="margin-right:10px;width:50px;height:50px;" src=' + image_url + '>');
            }
        }
    });

    $("#upload_good_info").click(function(){
        var community_name = $("#community_name").val();
        var phone = $("#phone").val();
        var cardid = $("#cardid").val();
        var donator_name = $("#donator_name").val();
        var good_type = $("#good_type").val();
        var amount = $("#amount").val();
        var unit = $("#unit").val();
        var remark = $("#remark").val();
        var image_url = $("#image_url").attr("src");
        var image_path = $("#image_path").val();

        if(phone=="" && cardid == ""){
            alert("请输入手机号或身份证号!");
            return;
        }else if(donator_name==""){
            alert("请输入姓名");
            return;
        }else if(amount == ""){
            alert("请输入数量!");
            return;
        }else if(unit==""){
            alert("请输入计量单位");
            return;
        }

        var good = {
            "community_name":community_name,
            "phone":phone,
            "cardid":cardid,
            "donator_name":donator_name,
            "good_type":good_type,
            "amount":amount,
            "unit":unit,
            "remark":remark,
            "image_url":image_url,
            "image_path":image_path,
        }
        $.post("/upload",good,function(data){
            if(data.code != 1){
                alert("提交异常!");
                return;
            }
            console.log(data.data);
            location.href = "/index.html" ; 
        },"json");

    });

    $.get("/communitys",{},function(data){
        if(data.code != 1){
            alert("加载数据失败!");
            return;
        }
        result = data.data.communitys;
        for(var i=0,len=result.length;i<len;i++){
            $("#community_name").append(String.format(''+
                '<option value="{0}">{0}</option>'
            ,result[i].name));
        }
    },"json");

    $.get("/good_types",{},function(data){
        if(data.code != 1){
            alert("加载数据失败!");
            return;
        }
        result = data.data.good_types;
        for(var i=0,len=result.length;i<len;i++){
            $("#good_type").append(String.format(''+
                '<option value="{0}">{0}</option>'
            ,result[i].name));
        }
    },"json");

    $.get("/units",{},function(data){
        if(data.code != 1){
            alert("加载数据失败!");
            return;
        }
        result = data.data.units;
        for(var i=0,len=result.length;i<len;i++){
            $("#unit").append(String.format(''+
                '<option value="{0}">{0}</option>'
            ,result[i].name));
        }
    },"json");

});