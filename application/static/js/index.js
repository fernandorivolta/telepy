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

function templateTable(tableData) {
    var template = '';
    $.each(tableData.servers, function(index, value) {
        template += `<tr class="datarow passo1">
            <td>
                ChkHosts
            </td>
            <td>
                ${value.hostname}
            </td>
            <td>
                ${value.ip}
            </td>
            <td>
                ${value.passwd}
            </td>
            <td id='data-id-${value.id}'>
                <img src='blob:https://loading.io/416ea189-363e-495f-bb86-f43d9862f7ad' />
            </td>
        </tr>`;
    });
    return `<table id="table" class="table text-center table-curved">
        <thead>
        <tr>
            <th colspan='5'>${tableData.teste_name}</th>
        </tr>
        <tr>
            <th scope="col">passo</th>
            <th scope="col">hostname</th>
            <th scope="col">ip</th>
            <th scope="col">senha (root)</th>
            <th scope="col">descricao</th>
        </tr>
        </thead>
        <tbody id="resultTable">
            ${template}
        </tbody>
        <tfoot>
        </tfoot>
    </table>`;
}

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
        beforeSend: function() {
            $('#result').append(templateTable(servers));
        },
        success: function (data) {
            console.log(data);
            start_install(data);
            let tableAjaxChange = document.querySelector('#resultTable');
            for (i = 0; i < tableAjaxChange.rows.length; i++) {
                for (idx = 0; idx < data.length; idx++) {
                    let compareId = `data-id-${data[idx].id}`;
                    if (tableAjaxChange.rows.item(i).lastElementChild.id == compareId) {
                        tdac = tableAjaxChange.rows.item(i).lastElementChild;
                        tdac.innerHTML = data[idx].message;
                    };
                }
            }
            //console.log(data);
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
