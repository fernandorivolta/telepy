$(document).ready(function(){
    $('#row-add').on('click', function(){
        $('#tbody').append(`
            <tr class="datarow">
                <td>
                    <input type="text"></input>
                </td>
                <td>
                    <input type="text"></input>
                </td>
                <td>
                    <input type="text"></input>
                </td>
                <td>
                    <a onclick="remover(this)" class="btn btn btn-danger" style="color: white; font-weight: bold;"><i class="fas fa-times"></i></a>
                </tr>
            </tr>`);
    });
});

var error_codes = ['002', '003', '004', '010', '011', '021', '022', '031'];
var request="";


function tableToObject(){
    //array de servers
    var servers = [];
    //objeto servidor
    var server = {};
    var testname=document.getElementById("teste_name").value;
    var id = 0;
    var oTable = document.getElementById('table');
    for (i = 0; i < oTable.rows.length; i++){
        if(oTable.rows.item(i).className == "datarow"){
            id+=1;
            var oCells = oTable.rows.item(i).cells;
            firstcol = oCells.item(0).children
            secondcol = oCells.item(1).children
            thirdcol = oCells.item(2).children
            if(firstcol[0] instanceof HTMLInputElement){
                server = {
                    '_hostname' : testname+"_"+firstcol[0].value,
                    '_ip' : secondcol[0].value,
                    '_passwd' : thirdcol[0].value,
                    '_id' : id
                };
                servers.push(server);
            }
        }
    } 
    return servers;
}

function end_test(){
    alert("Operacao finalizada")
    //$('#resultTable').prepend('<tr><td colspan=4>FIM DO TESTE</td></tr>');
}

function check_server_info(){
    //funcao q valida todos os campos
    if($("input").filter(function () {
        return $.trim($(this).val()).length == 0
    }).length == 0){
        $('#feedback').fadeOut();
        servers = tableToObject();
        request = $.ajax({
            type: 'POST',
            url: `check_server_info`,
            contentType: 'application/json',
            data: JSON.stringify({'servers' : servers}),
            beforeSend: function() {
                testename = $('#teste_name')[0].value;
                $('main').html('');
                $('main').html(`
                <div class="text-left"><span onclick="stop()" style="font-size: 20px; cursor:pointer;" ><i class="fas fa-undo-alt"></i> Voltar</span></div>
                <table id="table" class="table table-dark text-center table-curved">
                <thead>
                <tr>
                    <th colspan='5'>${testename}</th>
                </tr>
                <tr>
                    <th scope="col">passo</th>
                    <th scope="col">hostname</th>
                    <th scope="col">ip</th>
                    <th scope="col">descricao</th>
                </tr>
                </thead>
                <tbody id="resultTable">
                </tbody>
                <tfoot>
                </tfoot>
            </table>`);
            $('#resultTable').append(templateRow(servers, 'ChkHosts'));
            },
            success: function (data) {
                servers = JSON.parse(data);
                $.each(servers, function (server) {
                    console.log(server);
                    if(error_codes.includes(servers[server]._code)){
                        $(`#data-id-ChkHosts-${servers[server]._id}`).html(`<i class="fas fa-exclamation-circle"></i> ${servers[server]._message}`);
                        servers.pop(server);
                    }else{
                        $(`#data-id-ChkHosts-${servers[server]._id}`).html(`<i class="fas fa-check-circle"></i> ${servers[server]._message}`);
                    }
                });
                if(servers.length>0){
                    start_install(JSON.stringify(servers));
                }else{
                    end_test();
                }
            },
            error: function () {
            }
        });
    }else{
        $('#feedback').fadeOut();
        $('#feedback').fadeIn();
    }
}

function templateRow(data, step) {
    var template = '';
    $.each(data, function(index, value) {
        template += `<tr class="datarow passo1">
            <td>
                ${step}
            </td>
            <td>
                ${value._hostname}
            </td>
            <td>
                ${value._ip}
            </td>
            <td id='data-id-${step}-${value._id}'>
                <div class="loader"></div>
            </td>
        </tr>`;
    });
    return template;
}


function start_install(servers){
    request = $.ajax({
        type: 'POST',
        url: `start_install`,
        contentType: 'application/json',
        data: JSON.stringify(servers),
        beforeSend: function(){
            $('#resultTable').append(templateRow(JSON.parse(servers), 'StartInstall'));
        },
        success: function (data) {
            servers = JSON.parse(data);
            $.each(servers, function (server) {
                if(error_codes.includes(servers[server]._code)){
                    $(`#data-id-StartInstall-${servers[server]._id}`).html(`<i class="fas fa-exclamation-circle"></i> ${servers[server]._message}`);
                    servers.pop(server);
                }else{
                    $(`#data-id-StartInstall-${servers[server]._id}`).html(`<i class="fas fa-check-circle"></i> ${servers[server]._message}`);
                }
                if(servers.length>0){
                }else{
                    end_test();
                }
            });
        },
        error: function () {
        }
    });
}
/* 
function check_grafana_data(servers){
    $.ajax({
    type: 'POST',
    url: `check_grafana_data`,
    contentType: 'application/json',
    data: JSON.stringify(servers),
    beforeSend: function(){
        $('#resultTable').append(templateRow(JSON.parse(servers), 'ValidateGrfData'));
    },
    success: function (data) {
        servers = JSON.parse(data);
        $.each(servers, function (server) {
            $(`#data-id-ValidateGrfData-${servers[server]._id}`).html(servers[server]._message);
            if(error_codes.includes(servers[server]._code)){
                servers.pop(server);
            }
            if(servers.length>0){
                alert("Sucess");
            }else{
                end_test();
            }
        });
    },
    error: function () {
    }
}); 

}
*/

function stop(){
    request.abort();
    window.parent.location.reload();
}

function remover(btn){
    var table = document.getElementById("table");
    var rows = table.getElementsByClassName("datarow");
    if (rows.length > 1){
        btn.closest('tr').remove();
    }
}
