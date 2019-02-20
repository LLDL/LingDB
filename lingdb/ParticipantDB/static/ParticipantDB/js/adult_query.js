$(function(){
    var dashedDivs = $(".removeDash")
    for(var i=0; i<dashedDivs.length; i++){

        dashedDivs[i].innerHTML = dashedDivs[i].innerHTML.replace("-<input", "<input")
    }
    // var genderCheckboxes = $("#div_id_gender").children().addClass("d-inline");
    // var genderCheckboxes = $("#div_id_gender").find($(".form-check")).children().addClass("d-inline");
});