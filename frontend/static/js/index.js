async function getUser(id){
    let response = await fetch('/users/' + id, {
        method: 'GET'
    });
    let answer = await response.json();
    document.getElementById("user").innerHTML = answer['username'];
    let getCycle = await fetch('/cycles/' + answer['cycle'],{
        method: 'GET'
    });
    let cycle = await getCycle.json();
    document.getElementById("data").innerHTML = cycle['coinsCount'];
    document.getElementById("clickPower").innerHTML = cycle['clickPower'];
    let boostRequest = await fetch('/boosts/' + answer['cycle'], {
        method: 'GET'
    });
    let boosts = await boostRequest.json();
    renderAllBoosts(boosts);
    checkPrices();
    set_auto_click();
    set_send_coins_interval();
}

async function callClick() {
    const coins_counter = document.getElementById('data')
    let coins_value = parseInt(coins_counter.innerText)
    const click_power = document.getElementById('click_power').innerText
    coins_value += parseInt(click_power)
    document.getElementById("data").innerHTML = coins_value
    checkPrices();
}

function buyBoost(boost_level){
    const csrftoken = getCookie('csrftoken');
    fetch('/buyBoost/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            boost_level: boost_level
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return Promise.reject(response);
        }
    }).then(data => {
        document.getElementById("data").innerHTML = data['coinsCount'];
        document.getElementById("clickPower").innerHTML = data['clickPower'];
        document.getElementById("autoClickPower").innerHTML = data['autoClickPower'];
        document.getElementById(`boostLevel_${boost_level}`).innerHTML = data['level'];
        document.getElementById(`boostPrice_${boost_level}`).innerHTML = data['price'];
        document.getElementById(`boostPower_${boost_level}`).innerHTML = data['power'];
        checkPrices();
    });
}

function checkPrices() {
    let coinsCount = parseInt(document.getElementById("data").innerHTML);
    let boosts = document.getElementsByClassName("boost-holder");
    for (let i = 0; i < boosts.length; i++) {
        let button = boosts[i].getElementsByClassName("dog boost")[0];
        if (parseInt(boosts[i].getElementsByClassName("boostPrice")[0].innerHTML) > coinsCount) {
            button.setAttribute("disabled", "disabled");
        } else {
            button.removeAttribute("disabled");
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring((name.length + 1)));
                break;
            }
        }
    }
    return cookieValue;
}

function renderAllBoosts(boosts) {
    let parent = document.getElementById('boost-wrapper');
    parent.innerHTML = '';
    boosts.forEach(boost => {
        renderBoost(parent, boost);
    })
}

function renderBoost(parent, boost) {
    const div = document.createElement('div');
    div.setAttribute('class', 'boost-holder');
    if (boost.boost_type === 0)
        div.classList.add('autoBoost');
    div.setAttribute('id', `boost-holder-${boost.level}`);
    div.innerHTML = `
      <input type="image" src="http://www.pngmart.com/files/11/Shiba-Inu-Doge-Meme-PNG-Image.png"
      class="dog boost" alt="Boost" onclick="buyBoost(${boost.level})">
      <p> Level: <span class="boostLevel" id="boostLevel_${boost.level}">${boost.level}</span></p>
      <p> Power: +<span class="boostPower" id="boostPower_${boost.level}">${boost.power}</span> coins/click</p>
      <p> Price: <span class="boostPrice" id="boostPrice_${boost.level}">${boost.price}</span> coins</p>`;
    parent.appendChild(div);
}

function set_auto_click() {
    setInterval(function() {
        const coins_counter = document.getElementById('data')
        let coinsValue = parseInt(coins_counter.innerText)

        const auto_click_power = document.getElementById('autoClickPower').innerText
        coinsValue += parseInt(auto_click_power)
        document.getElementById("data").innerHTML = coinsValue;
    }, 1000)
}

function set_send_coins_interval() {
    setInterval(function() {
        const csrftoken = getCookie('csrftoken')
        const coins_counter = document.getElementById('data').innerText

        fetch('/set_main_cycle/', {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                coinsCount: coins_counter,
            })
        }).then(response => {
            if (response.ok) {
                return response.json()
            } else {
                return Promise.reject(response)
            }
        }).then(data => {
            console.log('Coins count sended to server')
            checkPrices()
        }).catch(err => console.log(err))
    }, 10000)
}