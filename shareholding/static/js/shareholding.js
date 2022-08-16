function switchframe(tab) {

    console.log(tab)

    if (tab === 'tasks'){
        document.querySelector(".active").classList.remove("active");
        document.getElementById("tasks_tab").classList.add("active");
        document.getElementById("tasks_body").style.display  = 'inline';
        document.getElementById("app_body").style.display  = 'none';

    } else if (tab === 'trend'){
        trend_tab()

    } else if (tab === 'transaction'){
        transaction_tab()

    }
 }