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
        var val = input.val();
        if(type == "Numeric"){
            if(isNaN(parseInt(val,10))){
                input.get(0).setCustomValidity("Input a numeric score")
            }else{
                input.get(0).setCustomValidity('')
            }
        }else if(type == "Pass/Fail"){
            if(val.toLowerCase() != 'pass' && val.toLowerCase() != 'fail'){
                input.get(0).setCustomValidity("Enter 'pass' or 'fail'")
            }else{
                input.get(0).setCustomValidity('')
            }
        }else{
            if(val == '' ){
                input.get(0).setCustomValidity("Enter a value")
            }else{
                input.get(0).setCustomValidity('')

            }
        }
    });
}
function changeInputs(){
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
        console.log(input);
        console.log(type);
        if(type == "Numeric"){
            input.attr('type', 'number');
        }else if(type == "Pass/Fail"){
            input.attr('list', 'auto-passfail')
        }
    });
}
$(function(){
    changeInputs()
    if($("#result_table_ass").length==1){
        $("#result_table_ass").change(validate);
        $("#result_table_ass").change();
    }else{
        $("#result_table_exp").change(validate);
        $("#result_table_exp").change();
    }
});