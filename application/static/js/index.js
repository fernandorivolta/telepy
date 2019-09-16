$(document).ready(function(){
    $('#row-add').on('click', function(){
        $('#table').prepend(`
            <tr>
                <td>
                    <input type="text"></input>
                </td>
                <td>
                    <input type="text"></input>
                </td>
                <td>
                    <a onclick="remover(this)" class="btn btn-danger"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg></a>
                </tr>
            </tr>`);
    });
});
function remover(btn){
    var table = document.getElementById("table");
    var rows = table.getElementsByTagName("tr");
    if (rows.length > 3){
        btn.closest('tr').remove();
    }
}