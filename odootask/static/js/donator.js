$(function(){
    initGoodSearchPage();

    function initGoodSearchPage(){
        $("#mobile").focus();
    }

    $("#make_search").click(function(){
        var mobile = $("#mobile").val();
        if(!mobile){
            alert("请输入手机号！");
            return;
        }
        $.get("/donator_number",{"mobile":mobile},function(data){
            if(data.code != 1){
                alert(data.message);
                return;
            }
            donator = data.data.donator;
            number = donator.number;
            if(number){
                $("#donator_search_list").text("您的志愿者编号："+number);
            }
        },"json");

    });
});