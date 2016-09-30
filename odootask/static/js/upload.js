$(function () {
    // var image_path = "/api/image?id=";
    // // 选择并加载头像的内容
    // $('#take_photo').fileupload({
    //     url: api_path + '/api/image/list',
    //     method:"POST",
    //     sequentialUploads: true,
    //     dataType: 'json',
    //     done: function (e, data) {
    //         var result = data.result.response;
    //         if (result['success'] != 1) {
    //             alert("上传失败");
    //         } else {
    //             console.log(result);
    //             var image = result.data[0];
    //             file_path = image.file_path;
    //             image_url = api_path + file_path;
    //             console.log(image_url);
    //             $("#media_content").html('<img  id="image_url" style="margin-right:10px;width:50px;height:50px;" src=' + image_url + '>');
    //         }
    //     }
    // });
    
    //checkcode
    var api_path = "http://139.224.26.81:8500";
//      var api_path = "http://localhost:8500";

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
            if(result[i]["unit"]){
                good_unit = "/"+result[i]["unit"][1];
            }else{
                good_unit = "";
            }
            $("#good_type").append(String.format(''+
                '<option value="{0}">{1}</option>'
            ,result[i].name,result[i].name+ good_unit));
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

    $("#get_phone_code").click(function(){
        $("#get_phone_code").css({"color":"#337ab7"});
        var phone = $("#phone").val();
        if(phone==""){
            alert("请输入手机号!");
            return;
        }
        $.get(api_path + "/api/checkcode/mobile",{"mobile":phone},function(data){
            $("#get_phone_code").attr("disabled",true);
            if(data.response.success != 1){
                alert(data.response.return_code);
                $("#get_phone_code").attr("disabled",false);
                return;
            }
            var index = 60;
            var interval_obj = setInterval(function(){
                    index = index -1;
                    $("#get_phone_code").html(String(index) + "s") ; 
                    if(index == 1){
                        index = 60;
                        $("#get_phone_code").html("获取验证码") ;
                        $("#get_phone_code").attr("disabled",false);
                        clearInterval(interval_obj);
                    }
            },1000);
            console.log(data.response.data.code);

            $.get("/donator",{"mobile":phone},function(data){
                if(data.code != 1){
                    return;
                }
                var donator = data.data.donator;
                var donator_name = donator.donator_name;
                var cardid = donator.cardid;
                $("#donator_name").val(donator_name);
                $("#cardid").val(cardid);
                return;
            },"json") ; 

        },"json");
    });

    $("#upload_good_info").click(function(){
        var community_name = $("#community_name").val();
        var phone = $("#phone").val();
        var phone_code = $("#phone_code").val();
        var cardid = $("#cardid").val();
        var donator_name = $("#donator_name").val();
        var good_type = $("#good_type").val();
        var amount = $("#amount").val();
        var remark = $("#remark").val();
        // var image_url = $("#image_url").attr("src");
        // var image_path = $("#image_path").val();

        if(phone==""){
            alert("请输入手机号!");
            return;
        }else if(phone != "" && phone_code == ""){
            alert("请输入手机验证码!");
            return;
        }
        else if(donator_name==""){
            alert("请输入姓名");
            return;
        }else if(amount == ""){
            alert("请输入数量!");
            return;
        }

        //验证手机验证码
        $.post(api_path + "/api/mobile/check",{"phone":phone,"phone_code":phone_code},function(data){
            if(data.response.success != 1){
                alert("验证码错误!");
                return;
            }

            var good = {
                "community_name":community_name,
                "phone":phone,
                "cardid":cardid,
                "donator_name":donator_name,
                "good_type":good_type,
                "amount":amount,
                "remark":remark,
                // "image_url":image_url,
                // "image_path":image_path,
            }
            $.post("/upload",good,function(data){
                if(data.code != 1){
                    alert("提交异常!");
                    return;
                }
                console.log(data.data);
                alert(String.format("您的志愿者编号为：{0},您也可以在志愿者查询页面查询!",data.data.donator_number));
                location.href = "/index.html" ; 
            },"json");

        },"json");
    });

});
