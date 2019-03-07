$(function(){
    $("input[type=date]").change(function(){
        $("input[type=date]").each(function(index){
            var inputDate = new Date(this.value);
            var now = new Date();
            var comp = inputDate.getTime() - now.getTime();
            var helper = $(".dateHelper").eq(index);
            if(comp > 0){
                helper.text("Warning: Date is After Today.");   
            }else{
                helper.text('');
            }
        });
    });
    $("input[type=date]").each(function(){
        $(this).parent().append('<div class="dateHelper text-danger"></div>');
    });
    $("input[type=date]").change();
});