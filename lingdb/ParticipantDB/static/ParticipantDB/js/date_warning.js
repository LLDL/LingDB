$(function(){
    $(".dateInput").change(function(){
        console.log("test")
        $(".dateInput").each(function(index){
            var inputDate = new Date(this.value);
            var now = new Date();
            var comp = inputDate.getTime() - now.getTime();
            var helper = $(".dateHelper").eq(index);
            if(comp > 0){
                helper.text("Warning: Date is After Today");   
            }else{
                helper.text('');
            }
        });
    });
    $(".dateInput").each(function(){
        console.log($(this).parent())
        $(this).parent().append('<span class="dateHelper text-danger"></span>');
    });
    $(".dateInput").change();
});