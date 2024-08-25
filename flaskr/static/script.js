async function UpdateDashboard() {
    // fetch updated data
    let response = await fetch('/get_dashboard_data');
    let data = await response.json();
    
    console.log(data.portfolio)

    //update portfolio data
    portfolio_data = data.portfolio;
    new_portfolio_value = Number(portfolio_data.portfolio_value).toFixed(2);
    document.getElementById('portfolio-value').innerHTML =  `$ ${new_portfolio_value}`;


    new_profit = Number(portfolio_data.profit).toFixed(2);
    percent_profit = Number(portfolio_data.percentage_change).toFixed(2);
    document.getElementById('profit').innerHTML = `$${new_profit} (${percent_profit}%)`;
    if (new_profit > 0){
        document.getElementById('profit').style.color = 'green';
    }
    else if (new_profit < 0){
        document.getElementById('profit').style.color = 'red';
    }
    else {
        document.getElementById('profit').style.color = 'yellow';

    }

    //update stock data
    stock_data = data.portfolio.stocks

    for (let id in stock_data) {
        stock_symbol = stock_data[id].symbol;
        stock_price = Number(stock_data[id].current_price).toFixed(2);
        stock_change = Number(stock_data[id].change).toFixed(2);

        document.getElementById(`${stock_symbol}-price`).innerHTML = `$${stock_price}`;
        document.getElementById(`${stock_symbol}-change`).innerHTML = `${stock_change}%`;

        
        if (stock_change > 0 ) {
            if (!document.getElementById(`${stock_symbol}-price`).classList.contains("text-success")){
                console.log("changing to green");
                document.getElementById(`${stock_symbol}-price`).classList.toggle("text-success");
                document.getElementById(`${stock_symbol}-change`).classList.toggle('text-success');
            }
        }
        else if (stock_change < 0 ){
            if (!document.getElementById(`${stock_symbol}-price`).classList.contains("text-danger")){
                console.log("changing to red");
                document.getElementById(`${stock_symbol}-price`).classList.toggle('text-danger');
                document.getElementById(`${stock_symbol}-change`).classList.toggle('text-danger');
            }
        }
        else {
            document.getElementById(`${stock_symbol}-price`).classList.toggle('text-white');
            document.getElementById(`${stock_symbol}-change`).classList.toggle('text-white');
        }

    }

    // update indexes
    index_data = data.indexes;
    for (let id in index_data) {
        index_symbol = index_data[id].symbol;
        index_price = Number(index_data[id].current_price).toFixed(2);
        index_change = Number(index_data[id].change).toFixed(2);

        if (index_change > 0) {
            if (!document.getElementById(`${index_symbol}-price`).classList.contains("text-success")) {
            document.getElementById(`${index_symbol}-price`).classList.toggle("text-success");
            document.getElementById(`${index_symbol}-change`).classList.toggle('text-success');
            }
        }
        else if (index_change < 0){
            if (!document.getElementById(`${index_symbol}-price`).classList.contains("text-danger")) {
            document.getElementById(`${index_symbol}-price`).classList.toggle('text-danger');
            document.getElementById(`${index_symbol}-change`).classList.toggle('text-danger');
            }
        }
        else {
            document.getElementById(`${index_symbol}-price`).classList.toggle('text-white');
            document.getElementById(`${index_symbol}-change`).classList.toggle('text-white');
        }

    }
}

async function setIntervalAndExecute(fn, t) {
    fn();
    setInterval(fn, t);
}
