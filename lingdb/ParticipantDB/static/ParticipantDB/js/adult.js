
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
    
    $(".age_learning_started").change(function(){
        var started = $(".age_learning_started")
        var ended = $(".age_learning_ended")

        started.each(function(index){
            // console.log(this.value, ended[index].value, ended[index].value == '')
            if(ended[index].value != '' && this.value > ended[index].value){
                this.setCustomValidity('Learning must start before it ends')
            }else{
                this.setCustomValidity('')
            }
        });

        // for(var i=0; i<started.length; i++){
        //     console.log(i)
        //     if ($(started[i]).val() > $(ended[i]).val() && $(ended[i]).val() != 0){
        //         this.setCustomValidity('Learning must start before it ends')
        //     }
        // }

    });

    $(".age_learning_ended").change(function(){
        $(".age_learning_started").change();
    });



    $(".isNative").change();
    $(".age_learning_started").change();
    $(".age_learning_ended").change();


});
