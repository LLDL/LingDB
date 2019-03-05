$(function(){
    $("#result_table").change(function(){
        var types = $(".type");
        types.each(function(index){
            var type = this.textContent
            var curr = 'id_assessment_field_scores-'+ index +'-score';
            var input = $('#' + curr).val();
            console.log(type + " | " + curr + " | " + input)
            if(type == "Numeric"){
                if(isNaN(parseInt(input,10))){
                    console.log(curr + " isNaN")
                }
            }
            else if(type === "Pass/Fail"){
                if(toLowerCase(input) != 'pass' || toLowerCase(input) != 'fail'){
                    console.log(curr + " is not pass/fail")
                }
            }
            
        });




        
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
    });
    
    $("#result_table").change();

    // var fam = $("#id_child-family");

    // fam.attr('required', false)
});