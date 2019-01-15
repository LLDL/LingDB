
$(function(){
    $("#exposure_table").change(function(){
        console.log("changed");
        var temp = 0;
        for(var i=0; i<5; i++){
            var curr = "#id_form-" + i + "-percentage_exposure";
            console.log(curr);
            var val = $(curr).prop('value');
            if(val != ''){
                console.log(val);
                temp += parseInt(val);
            }
        }
        console.log(temp)
        $("#sumExposure").val(temp);
        if(temp == 100){
            $("#sumExposure").removeClass("bg-danger")
            $("#sumExposure").addClass("bg-success")
        }else{
            $("#sumExposure").removeClass("bg-success")
            $("#sumExposure").addClass("bg-danger")
        }
    });
    $("#exposure_table").change();
});