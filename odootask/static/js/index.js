$(function(){
    initGoodSearchPage();

    function initGoodSearchPage(){
        $("#number")[0].blur();
    }

    $("#number").focus(function(){
        $("#number")[0].blur();
        location.href = "/search.html" ;
    });

    $.get("/nearby_donate",{},function(data){
        if(data.code != 1){
            alert("加载数据失败!");
            return;
        }
        result = data.data.goods;
        for(var i=0,len=result.length;i<len;i++){
            $("#nearby_donate").append(String.format(''+
                '<div class="good-tab row">'+
                    '<div class="col-xs-4">'+
                            '<p>{0}</p>'+
                            '<p>{1}</p>'+
                    '</div>'+
                    '<div class="col-xs-8 tab-content">'+
                        '<p>'+
                            '捐赠人：{2}'+
                        '</p>'+
                        '<p>'+
                            '捐赠物资 : {3}'+
                        '</p>'+
                    '</div>'+
                '</div>'
            ,result[i].show_date,result[i].show_time,result[i].donator_id[1],result[i].category_id[1]));
        }
    },"json");

});