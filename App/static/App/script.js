const socket = io('http://192.168.1.83:8000/')

function update_char_count(textarea) {
    let count_container = document.getElementById('char-count')
    let count = textarea.value.length
    let limit = count_container.innerHTML.split('/')[1]
    count_container.innerHTML = `${count} / ${limit}`
}


function create_new_msg(data, messages, name) {
    if (name == data.name) {
        var bg = 'bg-primary'
        var justify = 'justify-content-end'
        var align = 'align-self-end'
        var name_span = ''
        var p_align = 'text-end'
        var span_float = 'float-end'
    } else {
        var bg = 'bg-success'
        var justify = 'justify-content-start'
        var align = 'align-self-start'
        var name_span = `<span>${data.name}</span>`  
        var p_align = 'text-start'
        var span_float = 'float-start'
    }

    messages.insertAdjacentHTML('beforeend',
        `<div class="msg-container msg-container my-1 d-flex flex-row rounded-3 ps-3 mx-2 ${bg} ${justify} ${align}" style="max-width: 75%;">
            <div class="w-100 d-block">
                ${name_span} 
                <p class="h5 mx-2 text-wrap text-break ${p_align}">${data.message}</p>
                <span class="${span_float} d-sm-block d-none">${data.time_sent}</span>
            </div>
        </div>`)

    messages.scrollTop = messages.scrollHeight
}

function update_typing_users(name, msg_len) {
    var typing_users = document.getElementById('typing-users-row')
    var users = document.getElementsByClassName('typing-user')

    for (let i = 0; i < users.length; i ++) {
        if (users[i].getElementsByTagName('p')[0].textContent == name) {
            if (msg_len == 0) {
                users[i].remove()
            } 
            return
        }
    }

    if (msg_len != 0) {
        typing_users.insertAdjacentHTML('beforeend',
        `
        <td class="typing-user">
            <p class="loading m-0">${name}</p>
        </td>
        `
        )
    }
}

function remove_typing_user(name) {
    let users = document.getElementsByClassName('typing-user')
    for (let i = 0; i < users.length; i ++) {
        if (users[i].getElementsByTagName('p')[0].textContent == name) {
            users[i].remove('<remove_typing_user>', name)
            return
        }
    }
}

function create_connection_toast(name, session_name, type) {
    if (name != session_name) {
        let toasts = document.getElementById('new-connection-toasts')

        if (type == 'connect') {
            var connect_type = 'Joined'
        } else {
            var connect_type = 'Left'
        }

        toasts.insertAdjacentHTML('beforeend',
        `<div class="toast fade" style="width: 14rem">
            <div class="toast-header">
                <strong class="me-auto"><p>${name} ${connect_type}.</p></strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
        </div>`)

        var child_toasts = toasts.getElementsByClassName('toast')
        var last_toast = child_toasts[child_toasts.length-1]
        var toast = new bootstrap.Toast(last_toast, {
            delay:3500
        })
        toast.show()
    }
}