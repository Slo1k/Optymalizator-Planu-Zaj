//Wczytywanie danych z pythona do js
//$.get("/getpythondata", function(data) {
//    console.log($.parseJSON(data))
//})

$("#lesson-number").change(function() {
    $('#time-container').html('');
    let number = $(this).val();
    for(i = 1; i <= number; i++) {
        $('#time-container').append(`
        <div>
        <label for="start-${i}">Start</label><input id="start-${i}" type="time">
        <label for="end-${i}">Koniec</label><input id="end-${i}" type="time">
        </div>
        `)
    }

});

$("#class-number").change(function() {
    // dorobic zerowanie tabelki
    $('#first-row').html('<th>Przedmiot / Klasa</th>');
    let number = $(this).val();
    //console.log(number);
    for(i = 1; i <= number; i++) {
        $('#first-row').append(`<th>${i}</th>`)
    }
});

$("#add-subject").click(function() {
    console.log($('#new-subject').val());
    let number = $("#class-number").val();

    $('#table').append(`<tr id="${$('#new-subject').val()}"><td>${$('#new-subject').val()}</td></tr>`);
    for(i = 1; i <= number; i++) {
        $(`#${$('#new-subject').val()}`).append(`<td><input type="number" min="0" class="subject-val"></td>`);
    }
});

$('#generate-graph').click(function() {
    let array = $('.subject-val');
    let number = parseInt($("#class-number").val());
    //let j = 0;
    let nodes_array = [];
    let temp = [];
    //let nodes_number = 0
    //let temp = 1;
    // for (let i = 0; i < array.length; i++){
    //     // console.log(array[j].value);
    //     nodes_number += parseInt(array[j].value);
    //     if(array[j].value == 0) {
    //         nodes_array.push([0]);
    //     } else {    
    //         let temp_array = []
    //         for(let k = 0; k<array[j].value;k++){
    //             temp_array.push(temp);
    //             temp++;
    //         }
    //         nodes_array.push(temp_array);
    //     }
    //     j+=number;
    //     if(j>=array.length){
    //         j -= array.length;
    //         j+=1;
    //     }
    // }

    for(let i = 0 ; i< array.length;i++){
        temp.push(array[i].value);
        if(temp.length == number) {
            nodes_array.push(temp);
            temp = [];
        }
    }


    console.log(nodes_array);

    //Wysyłanie danych z js do pythona
    var data = JSON.stringify(nodes_array);
    $.post( "/postmethod", {
        javascript_data: subjects
    });
});
