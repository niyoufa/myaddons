$(function(){
    var good_number = location.href.split("?number=")[1];
    $.get("/good",{"good_number":good_number},function(data){
        if(data.code != 1){
            alert("加载数据失败!");
            return;
        }
        result = data.data.good;
        $("#category_id").html(result["category_id"][1]);
        $("#amount").html(result["amount"]);
        $("#unit").html(result["unit"][1]);
        $("#doantor").html(result["donator_id"][1]);
        $("#donate_time").html(result["create_date"]);
        $("#remark").html(result["remark"]);
        var tracks = data.data.tracks;
        for(var i=0,len=tracks.length;i<len;i++){
            if(i==0){
                flag = "first";
            }else{
                flag = null;
            }
            $("#track_detail_list").append(String.format(''+
                    '<li class="{0}">'+
                        '<p>{1}</p>'+
                        '<p>{2}</p>'+
                        '<span class="before"></span><span class="after"></span>'+
                    '</li>'
            ,flag,tracks[i].create_date,tracks[i].type[1]))
        }
    },"json");
})