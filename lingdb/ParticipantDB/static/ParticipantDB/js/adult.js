// $(function(){
//     var fam = $("#id_parent-family");
//     fam.attr('required', false)
// });
$(function(){
    $(".isNative").change(function(){
        var nativeCount = 0
        $(".isNative").each(function(){
            if(this.checked){
                nativeCount ++
            } 
        });
        if(nativeCount === 0){
            $(".isNative").each(function(){
                this.setCustomValidity('Select at least one native language')
            });
        }else{
            $(".isNative").each(function(){
                this.setCustomValidity('')
            });
            
        }
    });
    
    $(".isNative").change();

    // var fam = $("#id_child-family");

    // fam.attr('required', false)
});