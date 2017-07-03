/**
 * Created by NoOne on 17/04/04.
 */

$('#id_vote').change(function() {
    var options = '';
    faculty = $('#id_vote option:selected').text().split(' : ')[0];
        // console.log(faculty);
        $.ajax({
            type: "GET",
            url: "ajax/filterGroups/",
            data: {'faculty':faculty},
           success: function(data){
                $.each(data, function (index, value) {
                    console.log(index + ': ' + value);
                    $('#id_group').append($("<option />").val(index).text(value))
                });
            }
        });
        $('#id_group').html(options);
    });


$('#get_subjects').click(function () {
    var currentDate = new Date();
    var container = $('#subjectTeacher');
    var group = $('#id_group option:selected').text();
    var course = $('#id_course option:selected').text();
    if (group != '---------' && group != '' && course != '' && course != '---------')
    {

        var year = $('#id_vote option:selected').text().split(' : ')[1].split('/')[1];
        // console.log(year);
        var half = $('#id_vote option:selected').text().split(' : ')[2].split(' ')[0];
        $.ajax({
        type: "GET",
        url: "ajax/getSubjects/",
        data: {'group':group, 'course':course, 'year':year, 'half':half},
       success: function(data){
            // $('#subjectTeacher').empty();
            if(data == 'error'){
                $('#errorMessageContainer').html("Ви щось не так обрали, або для ваших даних немає опросів.\n" +
                    "Сторінка згодом оновиться для повторного вибору.").show();
                setTimeout(function(){
                   window.location.reload(1);
                }, 3000);
                return;
            }
            $('<input />', {type: 'hidden', name: 'faculty',value: $('#id_vote option:selected').text()}).appendTo(container);
            $('<input />', {type: 'hidden', name: 'group',value: $('#id_group option:selected').text()}).appendTo(container);
            $('<input />', {type: 'hidden', name: 'course',value: $('#id_course option:selected').text()}).appendTo(container);
            for(var key in data){
                console.log(key, data[key]);
                addChoice(key,data[key]);
            }
            $('<input />', { class: 'deanery', type: 'checkbox',
                title: 'Якщо ви не мали справ з деканатом протягом цього семестру, будь ласка утримайтесь від голосування по цьому пункту.',
                id: 'deanery', checked: false, value: 'Оцінка роботи деканату' }).appendTo(container);
            $('<label />', { for: 'deanery', text: 'Оцінка роботи деканату' }).appendTo(container);
            $('<br>').appendTo(container);
            $('<input />', {type: 'submit', class: 'btn btn-primary', value: 'Submit'}).appendTo(container);
        }
        });
        // $('#errorMessageContainer').hide();
        $('#get_subjects').remove();
        $('#errorMessageContainer').addClass('alert-info').removeClass('alert-danger').html("Оберіть викладачів та предмети що ви хотіли би оцінити.").show();
    }
    else
    {
        console.log('errorselect');
        $('#errorMessageContainer').html("<strong>Помилка! </strong>Ви щось забули обрати!").show();
    }
});


function addChoice(name, values) {
   var container = $('#subjectTeacher');
   var inputs = container.find('input');
   var id = inputs.length+1;
   $('<input />', { class: 'teacherBox', type: 'checkbox', id: 'checkTeacher'+id, checked: true, value: name }).appendTo(container);
   $('<label />', { 'for': 'checkTeacher'+id, text: name }).appendTo(container);
   var sel = $('<select class="form-control"></select>').attr("id", 'selectTeacher'+id).attr('name', name).appendTo(container);
    for (var val in values){
        sel.append($("<option>").attr('value',values[val][0] + ' ' + values[val][1] + ' ' + values[val][2])
            .text(values[val][0] + ' ' + values[val][1] + ' ' + values[val][2]));
    }
    $('<br>').appendTo(container);
}

$("#subjectTeacher").on("change", "input.teacherBox", function(){
    var index = this.id.slice(12);
    // console.log($("#subjectTeacher input:checkbox:checked").length);
    if (this.checked) {
        $("#selectTeacher"+index).prop('disabled', false);
    } else {
        $("#selectTeacher"+index).prop("disabled", true);
    }
});
$("#subjectTeacher").on("change", "input.deanery", function(){
    var container = $('#subjectTeacher');
    if (this.checked) {
        $('<input />', {type: 'hidden',id: 'deaneryHid', name: 'Деканат',value: 'Оцінка роботи деканату'}).appendTo(container);
    } else {
        $('#deaneryHid').remove();
    }
});

function createInput(container){
    var $input = $('<input type="submit" class="btn btn-primary" value="Submit" />');
    $input.appendTo(container);
}

$('#subjectTeacher').submit(function () {
    if ($("#subjectTeacher input:checkbox:checked").length > 0)
    {
        // alert("ok");
        return true;
    }
    else
    {
       // alert("WTF");
       return false;
    }
})