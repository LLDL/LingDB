function validate(){
    var types = $(".type");
    types.each(function(index){
        var type = this.textContent
        var curr = ''
        if($("#result_table_ass").length==1){
            curr = "#id_assessment_field_scores-";
        }else{
            curr = "#id_experiment_section_field_scores-";
        }
        curr += index +'-score';
        var input = $(curr);
        console.log(input)
        var val = input.val();
        console.log(val)
        console.log(type + " | " + curr + " | " + val)
        if(type == "Numeric"){
            if(isNaN(parseInt(val,10))){
                console.log(curr + " isNaN")
                input.get(0).setCustomValidity("Input a numeric score")
            }else{
                input.get(0).setCustomValidity('')
            }
        }
        else if(type === "Pass/Fail"){
            if(val.toLowerCase() != 'pass' && val.toLowerCase() != 'fail'){
                console.log(curr + " is not pass/fail")
                input.get(0).setCustomValidity("Enter 'pass' or 'fail'")
            }else{
                input.get(0).setCustomValidity('')
            }
        }
    
    });
}

$(function(){
    
    if($("#result_table_ass")){
        $("#result_table_ass").change(validate);
    }
    if($("#result_table_exp")){
        $("#result_table_exp").change(validate);
    }




        
        // console.log("changed");
        // var temp = 100;
        // for(var i=0; i<5; i++){
        //     var curr = "#id_form-" + i + "-percentage_exposure";
        //     console.log(curr);
        //     var val = $(curr).prop('value');
        //     if(val != ''){
        //         console.log(val);
        //         temp -= parseInt(val);
        //     }
        // }
        // console.log(temp)
        // $("#sumExposure").val(temp);
        // if(temp == 0){
        //     $("#sumExposure").removeClass("bg-danger")
        //     $("#sumExposure").addClass("bg-success")
        // }else{
        //     $("#sumExposure").removeClass("bg-success")
        //     $("#sumExposure").addClass("bg-danger")
        // }
    
    $("#result_table_ass").change();
    $("#result_table_exp").change();

    // var fam = $("#id_child-family");

    // fam.attr('required', false)
});