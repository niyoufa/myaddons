$(function(){
    initGoodSearchPage();
    $("#search").click(function(){
        $("#track_detail").hide();
        $("#good_detail").hide();
        searchGood();
    });
    function initGoodSearchPage(){
        $("#track_detail").hide();
        $("#good_detail").hide();
        $("#search_info_tab").hide();
    }
    function searchGood(){
        var search_type = $("#search_type").val();
        var number = $("#number").val();
        if(search_type == "2"){
            alert("暂不支持!");
            return;
        }
        if(number == ""){
            alert("请输入物资编号！")
            return;
        }else if(isNaN(number)){
            alert("请输入正确的物资编号！");
            return;
        }else{
            console.log("查询物资" + number);
        }

        var api_server_addr = "/good" ;
        var params = {
            "good_number":number,
        }
        $.get(api_server_addr,params,function(res){
            if(res.code != 1){
                $("#search_info_tab").html(res.message);
                $("#search_info_tab").show();
                return
            }else{
                $("#tracks").empty();

                data = res.data;
                good = data.good;
                tracks = data.tracks;
                console.log(good);
                console.log(tracks);

                if(!good){
                    $("#search_info_tab").show();
                    setTimeout(function(){
                        $("#search_info_tab").hide();
                    },3000)
                }

                $("#category_id").html(good.category_id[1]);
                $("#amount").html(good.amount);
                $("#unit").html(good.unit[1]);
                $("#doantor").html(good.doantor_id[1]);
                $("#donate_time").html(good.donate_time);
                $("#donee").html(good.donee_id[1]);
                $("#donee_type").html(good.donee_type[1]);
                $("#donee_type").html(good.donee_type[1]);

                if(!good.remark){
                    $("#remark").html("暂无备注！");
                }

                if(tracks.length == 0){
                    $("#tracks").html("暂无追踪信息！");
                }
                for(var i=0,len=tracks.length;i<len;i++){
                    var track = tracks[i];
                    $("#tracks").append(String.format(''+
                    '<li>'+
                        '<span>{0}</span>'+
                        '<p>{1}</p>'+
                    '</li>'
                    ,track.write_date,track.type[1]))
                }

                $("#track_detail").show();
                $("#good_detail").show();
            }
        },"json");
    }
});
