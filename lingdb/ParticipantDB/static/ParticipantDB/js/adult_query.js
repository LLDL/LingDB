$(function(){
    var birthDateDiv = $(".removeDash")
    birthDateDiv[0].innerHTML = birthDateDiv[0].innerHTML.replace("-<input", "<input")
    // var genderCheckboxes = $("#div_id_gender").children().addClass("d-inline");
    // var genderCheckboxes = $("#div_id_gender").find($(".form-check")).children().addClass("d-inline");
});