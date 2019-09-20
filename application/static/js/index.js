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
                    <a onclick="remover(this)" class="btn btn btn-danger" style="color: white; font-weight: bold;">X</a>
                </tr>
            </tr>`);
    });
});

function tableToObject(){
    //array de servers
    var servers = [];
    //objeto servidor
    var server = {};
    var oTable = document.getElementById('table');
    for (i = 0; i < oTable.rows.length; i++){
        if(oTable.rows.item(i).className == "datarow"){
            var oCells = oTable.rows.item(i).cells;
            firstcol = oCells.item(0).children
            secondcol = oCells.item(1).children
            thicol = oCells.item(2).children
            if(firstcol[0] instanceof HTMLInputElement){
                server = {
                    'hostname' : firstcol[0].value,
                    'ip' : secondcol[0].value,
                    'passwd' : thicol[0].value
                };
                servers.push(server);
            }
        }
    } 
    return {
        'teste_name' : document.getElementById("teste_name").value,
        'servers' : servers
    };
}

function run(){
    servers = tableToObject();
    $.ajax({
        type: 'POST',
        url: `check_server_info`,
        contentType: 'application/json',
        data: JSON.stringify(servers),
        success: function (data) {
            start_install(data);
        },
        error: function () {
        }
    });
}

function start_install(data){
    $.ajax({
        type: 'POST',
        url: `start_install`,
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (response) {
            console.log(response);
        },
        error: function () {
        }
    });
}
function remover(btn){
    var table = document.getElementById("table");
    var rows = table.getElementsByClassName("datarow");
    if (rows.length > 1){
        btn.closest('tr').remove();
    }
}
