$(function(){
    initGoodSearchPage();

    function initGoodSearchPage(){
        $("#list_number")[0].focus();
    }

    $("#cancel_search").click(function(){
        location.href = "/index.html" ;
    });

    $("#list_number").blur(function(){
        var donator_number = $("#list_number").val();
        $.get("/goods",{"donator_number":donator_number},function(data){
            if(data.code != 1){
                alert("加载数据失败!");
                return;
            }
            result = data.data.goods;
            $("#good_search_list").empty();
            for(var i=0,len=result.length;i<len;i++){
                $("#good_search_list").append(String.format(''+
                    '<div class="good-tab row">'+
                        '<div class="col-xs-4">'+
                                '<img src="/image?good_number={0}" alt="error" class="float-left"/>'+
                        '</div>'+
                        '<div class="col-xs-8 tab-content">'+
                            '<p>'+
                                '捐赠人：{1}'+
                            '</p>'+
                            '<p>'+
                                '捐赠物资 : {2}'+
                            '</p>'+
                            '<p>'+
                                '日期 {3}'+
                            '</p>'+
                        '</div>'+
                        '<span class="good_numer" style="display:none;">{4}<span>'+
                    '</div>'
                ,result[i].number,result[i].donator_id[1],result[i].category_id[1],result[i].create_date,result[i].number));
            }
            $(".good-tab").click(function(){
                var good_number = $(this).find(".good_numer").text();
                location.href = "/detail.html?number="+good_number;
            });
        },"json");
        
    });

});