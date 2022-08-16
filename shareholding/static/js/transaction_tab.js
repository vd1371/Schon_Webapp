function transaction_tab(){
    document.querySelector(".active").classList.remove("active");
    document.getElementById("transaction_tab").classList.add("active");
    document.getElementById("tasks_body").style.display = "none"
    document.getElementById("app_body").style.display = "inline";
    document.getElementById("app_body").innerHTML =
    `
    <form onsubmit='send_request_for_transaction_tab()' class='form-inline' id='tranaction_form'>
    
    <label for='stock_id'>Stock ID:</label>
    <input type='text' id='stock_id' placeholder='e.g., 00693'>

    <label for='thresh'>Threshold(%):</label>
    <input type='text' id='thresh' placeholder='e.g., 10'>
    
    <br>
    
    <label for='start_date'>Start Date:</label>
    <input type='text' id='start_date' placeholder='e.g., 2022-01-03'>

    <label for='end_date'>End Date:</label>
    <input type='text' id='end_date' placeholder='e.g., 2022-01-10'>
    
    <button type='submit' id = 'trend_submit_btn'>Submit</button>
    </form>
    
    <br></br>
    <h3>Buyers</h3>
    <hr style="height:2px;border-width:0;color:gray;background-color:black">
    <table id="table-buyers" class="display" style="width=50% display: inline-block;"></table>

    <br></br>
    <h3>Sellers</h3>
    <hr style="height:2px;border-width:0;color:gray;background-color:black">
    <table id="table-sellers" class="display" style="width=50% display: inline-block;"></table>
    `;
}

async function send_request_for_transaction_tab() {
    const form = document.getElementById("tranaction_form");
    var stock_id = form.elements['stock_id'];
    var end_date = form.elements['end_date'];
    var thresh = form.elements['thresh'];

    if (stock_id != null){
        stock_id = stock_id.value
    } else {
        window.alert('You need to enter a stock_id')
    }

    if (end_date != null){
        end_date = end_date.value
    } else {
        window.alert('You need to enter an end_date')
    }

    if (thresh != null){
        thresh = thresh.value
    } else {
        window.alert('You need to enter a threshold')
    }

    const url = 'http://127.0.0.1:8000/shareholdinginfo/api/get_transaction_info/?' + 
        'stock=' + stock_id +
        '&date=' + end_date +
        '&thresh=' + thresh;

    fetch(url).then((response) => {
        if (response.ok && response.status == 200) {
            return response.json();
        } else {
            window.alert("Most probably, there were no transaction that meet the criteria.\n" +
                        "Please consider changing the stock code and date");
        }
    })
    .then((responseData) => {
        add_transaction_table(responseData)
    })
    .catch((error) => {
        console.log(error)
    });

}

function submit_handler_transaction(data){
    add_transaction_table(data);
}

function add_transaction_table(data){

    var data_sorted = data.sort(function(a, b){ return a.shareholding < b.shareholding ? 1 : -1; });

    var sellers = []
    var buyers = []

    for (var i in data_sorted){
        vals = Object.values(data_sorted[i]);

        var row = [
            data_sorted[i]['participant'],
            data_sorted[i]['name'],
            data_sorted[i]['difference_percentage'],
        ];
        
        if (data_sorted[i]['difference_percentage'] < 0){
            sellers.push(row)
        } else {
            buyers.push(row)
        }
    }

    var column_names = Object.keys(data[0])
    var columns = [
        { title: "Participant ID" },
        { title: "Name" },
        { title: "Difference (%)" },

    ]

    
    document.getElementById("table-buyers").innerHTML = ""
    document.getElementById("table-sellers").innerHTML = ""

    $(document).ready(function () {
        $('#table-buyers').DataTable({
            data: buyers,
            columns: columns,
            "bDestroy": true
        });
    });

    $(document).ready(function () {
        $('#table-sellers').DataTable({
            data: sellers,
            columns: columns,
            "bDestroy": true
        });
    });

}