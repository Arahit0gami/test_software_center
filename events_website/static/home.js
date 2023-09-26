function eventsInfo() {
    fetch('/events/')
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('all_events', JSON.stringify(data))
            let allEvents = document.querySelector("#all-events")
            let myEvents = document.querySelector("#my-events")
            let myId = Number(localStorage.getItem('my_id'))

            let activeEvent = localStorage.getItem('activeEvent')
            activeEvent = activeEvent ? Number(activeEvent) : null

            let activeMyEvent = localStorage.getItem('activeMyEvent')
            activeMyEvent = activeMyEvent ? Number(activeMyEvent) : null


            let htmlAllEvents = data.map(function (item) {
                if (activeEvent && activeEvent === item.id) {
                    return `<li class="list-group-item list-group-item-action active" role="tab" data-bs-toggle="list" aria-selected="true" onclick="informEvent(${item.id})">${item.title}</li>`
                }
                return `<li class="list-group-item list-group-item-action" role="tab" data-bs-toggle="list" onclick="informEvent(${item.id})">${item.title}</li>`
            })
            let htmlMyEvents = data.map(function (item) {
                if (item.participants.some(participant => participant.id === myId)) {
                    if (activeMyEvent && activeMyEvent === item.id) {
                        return `<li class="list-group-item list-group-item-action active" role="tab" data-bs-toggle="list" aria-selected="true" onclick="informEvent(${item.id}, myEvents=true)">${item.title}</li>`
                    }
                    return `<li class="list-group-item list-group-item-action" role="tab" data-bs-toggle="list" onclick="informEvent(${item.id}, myEvents=true)">${item.title}</li>`
                }
            })

            allEvents.innerHTML = htmlAllEvents.join('')
            myEvents.innerHTML = htmlMyEvents.join('')
            if (activeEvent) {
                informEvent(activeEvent)
            } else if (activeMyEvent) {
                informEvent(activeMyEvent, true)
            }
        })
        .catch(error => console.error('Ошибка:', error))
}

function informEvent(eventId, myEvents = false) {
    if (myEvents) {
        localStorage.setItem('activeMyEvent', eventId)
        localStorage.removeItem('activeEvent')
    } else if (!myEvents) {
        localStorage.setItem('activeEvent', eventId)
        localStorage.removeItem('activeMyEvent')
    }
    let allEvents = localStorage.getItem('all_events')
    allEvents = JSON.parse(allEvents)
    let myId = Number(localStorage.getItem('my_id'))
    let item = allEvents.find(item => item.id === eventId)
    let date = new Date(item.date_event)
    let formattedDate = date.toLocaleDateString(
        'ru-RU', {day: '2-digit', month: '2-digit', year: 'numeric'}
    ) + ' ' + date.toLocaleTimeString(
        'ru-RU', {hour: '2-digit', minute: '2-digit'}
    )
    let htmlAllPartic = item.participants.map(function (item) {
        return `<p><a class="link-offset-2 link-underline link-underline-opacity-0" data-bs-toggle="modal" onclick="informUser(${item.id})" href="#informUser">${item.first_name} ${item.last_name}</a></p>`
    })
    let me_in_participant = item.participants.find(participant => participant.id === myId)
    let joinLeaveEvent
    if (me_in_participant) {
        joinLeaveEvent = `<button type="button" class="btn btn-danger" onclick="joinEvent(${eventId}, join=false, leave=true)">Отказаться от участия</button>`
    } else {
        joinLeaveEvent = `<button type="button" class="btn btn-success" onclick="joinEvent(${eventId}, join=true, leave=false)">Принять участие</button>`
    }
    document.querySelector("#title-event").innerText = item.title
    document.querySelector("#event-description").innerText = item.text
    document.querySelector("#date-event").innerText = 'Дата: ' + formattedDate
    document.querySelector("#participants").innerHTML = htmlAllPartic.join('')
    document.querySelector("#join-leave-event").innerHTML = joinLeaveEvent
}

function informUser(userId) {
    fetch(`/?user=${userId}`)
        .then(response => response.json())
        .then(data => {
            let dateOfBirth = new Date(data.date_of_birth)
            let dateJoined = new Date(data.date_joined)
            dateOfBirth = dateOfBirth.toLocaleDateString(
                'ru-RU', {day: '2-digit', month: '2-digit', year: 'numeric'}
            )
            dateJoined = dateJoined.toLocaleDateString(
                'ru-RU', {day: '2-digit', month: '2-digit', year: 'numeric'}
            )
            document.querySelector("#first-name-participant").innerText = data.first_name
            document.querySelector("#last-name-participant").innerText = data.last_name
            document.querySelector("#date-birth-participant").innerText = dateOfBirth
            document.querySelector("#date-joined-participant").innerText = dateJoined
        })
        .catch(error => console.error('Ошибка:', error))
}

function joinEvent(eventId, join = false, leave = false) {
    let myId = Number(localStorage.getItem('my_id'))
    let csrftoken = getCookie('csrftoken')

    if (join && !leave) {
        fetch(`/events/?id=${eventId}`, {
            method: 'PUT',
            headers: {"X-CSRFToken": csrftoken},
        })
            .then(response => response.json())
            .then(data => {
                if (data.result) {
                    let myFirstName = localStorage.getItem('my_first_name')
                    let myLastName = localStorage.getItem('my_last_name')
                    let newParticipant = {
                        "id": myId,
                        "first_name": myFirstName,
                        "last_name": myLastName
                    };
                    let allEvents = localStorage.getItem('all_events')
                    allEvents = JSON.parse(allEvents)
                    allEvents = allEvents.map(event => {
                        if (event.id === eventId) {
                            event.participants.push(newParticipant)
                        }
                        return event
                    })
                    localStorage.setItem('all_events', JSON.stringify(allEvents))
                    reloadMyEvents(allEvents, myId)
                    informEvent(eventId)
                }
            })
            .catch(error => console.error('Ошибка:', error))
    } else if (leave && !join) {
        fetch(`/events/?id=${eventId}`, {
            method: 'DELETE',
            headers: {"X-CSRFToken": csrftoken},
        })
            .then(response => response.json())
            .then(data => {
                if (data.result) {
                    let allEvents = localStorage.getItem('all_events')
                    allEvents = JSON.parse(allEvents)
                    allEvents = allEvents.map(event => {
                        if (event.id === eventId) {
                            event.participants = event.participants.filter(participant => participant.id !== myId)
                        }
                        return event
                    })
                    localStorage.setItem('all_events', JSON.stringify(allEvents))
                    reloadMyEvents(allEvents, myId)
                    informEvent(eventId)
                }
            })
            .catch(error => console.error('Ошибка:', error))
    }
}

function reloadMyEvents(data, myId) {
    let myEvents = document.querySelector("#my-events")
    let htmlMyEvents = data.map(function (item) {
        if (item.participants.some(participant => participant.id === myId)) {
            return `<li class="list-group-item list-group-item-action" role="tab" data-bs-toggle="list" onclick="informEvent(${item.id})">${item.title}</li>`
        }
    })
    myEvents.innerHTML = htmlMyEvents.join('')
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    eventsInfo();
})

setInterval(eventsInfo, 30000)