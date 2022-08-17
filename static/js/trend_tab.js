function trend_tab (){
    document.querySelector(".active").classList.remove("active");
    document.getElementById("trend_tab").classList.add("active");
    document.getElementById("tasks_body").style.display = "none";
    document.getElementById("app_body").style.display = "inline";
    document.getElementById("app_body").innerHTML =
        `
        <form onsubmit='send_request_for_trend_tab()' class='form-inline' id='trend_form'>
        
            <label for='stock_id'>Stock ID:</label>
            <input type='text' id='stock_id' placeholder='e.g., 00693'>
            
            <label for='start_date'>Start Date:</label>
            <input type='text' id='start_date' placeholder='e.g., 2022-01-03'>
            
            <label for='end_date'>End Date:</label>
            <input type='text' id='end_date' placeholder='e.g., 2022-01-10'>

            <button type='submit' id = 'trend_submit_btn'>Submit</button>
        </form>
        
        <br></br>
        <hr style="height:2px;border-width:0;color:gray;background-color:black">
        <h3>Top 10 plot</h3>
        <div id='top_10_plot'></div>

        <br></br>
        <hr style="height:2px;border-width:0;color:gray;background-color:black">
        <h3>Results</h3>
        <div>
            <table id="table-sortable" class="display"></table>
        </div>
        
        `
}

async function send_request_for_trend_tab () {
    const form = document.getElementById("trend_form");
    var stock_id = form.elements['stock_id'];
    var end_date = form.elements['end_date'];

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

    const url = 'http://127.0.0.1:8000/shareholdinginfo/api/get_stock_info/?stock=' + 
        stock_id + '&date=' + end_date;

    fetch(url)
        .then((res) => res.json())
        .then((responseData) => submit_handler_trend(responseData))
        .catch((error) => {
            console.log(error)
        })
    ;

}

function submit_handler_trend(data){
    add_table_trend(data);
    plot_top10(data);
}

function add_table_trend(data){

    var columns = [
        {title : "No."},
        {title : "Name"},
        {title : "Address"},
        {title : "Shares"},
        {title : "%"},
        {title : "Abs Diff"},
        {title : "% Diff"},
        {title : "Date"},
        {title : "Participant ID"},
        {title : "Stock code"},
    ]

    var result = [];
    for(var row in data)
        result.push(Object.values(data[row]))

    document.getElementById("table-sortable").innerHTML = ""

    $(document).ready(function () {
        $('#table-sortable').DataTable({
            data: result,
            columns: columns,
            "bDestroy": true
        });
    });

}

function plot_top10(data){
    var data_top10 = data.sort(function(a, b) { return a.shareholding < b.shareholding ? 1 : -1; })
                .slice(0, 10);

    var xValues = []
    var yValues = []

    for (var row in data_top10){
        xValues.push(data_top10[row]['name'])
        yValues.push(data_top10[row]['shareholding'])
    }

    var trace1 = {
        x: xValues,
        y: yValues,
        name: 'Top 10 shareholding',
        type: 'bar'
    }

    var data_for_plot = [trace1]
    var layout = {
        barmode: 'stack',
        xaxis :{
            automargin: true
        }
    };
    Plotly.newPlot('top_10_plot', data_for_plot, layout);
}