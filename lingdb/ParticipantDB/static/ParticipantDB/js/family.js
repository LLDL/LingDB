$(function(){
    $(".primaryContact").change(function(){
        console.log('change detected')
        var checkCount = 0
        $(".primaryContact").each(function(){
            if(this.checked){
                checkCount ++
            } 
        });
        if(checkCount === 0){
            $(".primaryContact").each(function(){
                this.setCustomValidity('Select a primary parent')
            });
        }else if(checkCount > 1){
            $(".primaryContact").each(function(){
                this.setCustomValidity('Only one parent may be the primary parent')
            });
        }else{
            $(".primaryContact").each(function(){
                this.setCustomValidity('')
            });
            
        }
    });
    
    $(".primaryContact").change();

    // var fam = $("#id_child-family");

    // fam.attr('required', false)
});