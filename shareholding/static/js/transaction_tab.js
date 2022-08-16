function transaction_tab(){
    document.querySelector(".active").classList.remove("active");
    document.getElementById("transaction_tab").classList.add("active");
    document.getElementById("tasks_body").style.display = "none"
    document.getElementById("app_body").style.display = "inline";
    document.getElementById("app_body").innerHTML =
    `
    <form onsubmit='send_request()' class='form-inline' id='tranaction_form'>
    
    <label for='stock_id'>Stock ID:</label>
    <input type='text' id='stock_id' placeholder='e.g., 00693'>

    <label for='treshold'>Treshold(%):</label>
    <input type='text' id='treshold' placeholder='e.g., 10'>
    
    <br>
    
    <label for='start_date'>Start Date:</label>
    <input type='text' id='start_date' placeholder='e.g., 2022-01-03'>

    <label for='end_date'>End Date:</label>
    <input type='text' id='end_date' placeholder='e.g., 2022-01-10'>
    
    <button type='submit' id = 'trend_submit_btn'>Submit</button>
    </form>
    
    <br></br>
    <hr style="height:2px;border-width:0;color:gray;background-color:black">
    `;
}