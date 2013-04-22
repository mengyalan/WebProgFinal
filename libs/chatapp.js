var ChatApp = {
    connection : null,
    room : null,
    nickname : null,

    SERVER : "mengyalan.com",
    CONF_ADDR : "conference.mengyalan.com",
    BOT : "bot@mengyalan.com",
    BOT_SMACK : "bot@mengyalan.com/Smack",

    bot_in_room : false,
    room_created : false,
    joined : null,
    unlocked : false,
    participants : null,

    on_presence : function(presence) {
        var from = $(presence).attr('from');
        var room = Strophe.getBareJidFromJid(from);

        // make sure this presence is for the right room
        if (room === ChatApp.room) {
            var nick = Strophe.getResourceFromJid(from);

            if ($(presence).attr('type') === 'error' && !ChatApp.joined) {
                // error joining room; reset app
                ChatApp.connection.disconnect();
            } else if (!ChatApp.participants[nick] && $(presence).attr('type') !== 'unavailable') {
                // add to participant list
                var user_jid = $(presence).find('item').attr('jid');

                ChatApp.participants[nick] = user_jid || true;
                $('#participant-list').append('<li>' + nick + '</li>');
                // if bot is present, toggle
                if (nick === ChatApp.BOT_SMACK) {
                    ChatApp.bot_in_room = true;
                }
                if (ChatApp.joined) {
                    $(document).trigger('user_joined', nick);
                }
            } else if (ChatApp.participants[nick] && $(presence).attr('type') === 'unavailable') {
                // remove from participants list
                ChatApp.participants[nick] = false;
                // if bot is NOT present, toggle
                if (nick === ChatApp.BOT_SMACK) {
                    ChatApp.bot_in_room = false;
                }

                $('#participant-list li').each(function() {
                    if (nick === $(this).text()) {
                        $(this).remove();
                        return false;
                    }
                });
                $(document).trigger('user_left', nick);

            }

            if ($(presence).attr('type') !== 'error' && !ChatApp.joined) {
                // check for status 110 to see if it's our own presence
                // if ($(presence).find("status[code='110']").length > 0) {
                if (ChatApp.unlocked) {
                    // check if server changed our nick
                    if ($(presence).find("status[code='210']").length > 0) {
                        ChatApp.nickname = Strophe.getResourceFromJid(from);
                    }

                    // room join complete
                    $(document).trigger("room_joined");
                }
            }
        }

        return true;
    },

    on_public_message : function(message) {
        var from = $(message).attr('from');
        var room = Strophe.getBareJidFromJid(from);
        var nick = Strophe.getResourceFromJid(from);

        // make sure message is from the right place
        if (room === ChatApp.room) {
            // is message from a user or the room itself?
            var notice = !nick;
            var notify = false;
            // messages from ourself will be styled differently
            var nick_class = "nick";
            if (nick === ChatApp.nickname) {
                nick_class += " self";
            } else {
                notify = true;
            }

            var body = $(message).children('body').text();

            var delayed = $(message).children("delay").length > 0 || $(message).children("x[xmlns='jabber:x:delay']").length > 0;

            // look for room topic change
            var subject = $(message).children('subject').text();
            if (subject) {
                $('#room-topic').text(subject);
            }

            if (!notice) {
                var delay_css = delayed ? " delayed" : "";

                var action = body.match(/\/me (.*)$/);
                if (!action) {
                    // Play a notification sound
                    if (notify) {
                        document.getElementById('notification').play();
                    }
                    ChatApp.add_message("<div class='message" + delay_css + "'>" + "&lt;<span class='" + nick_class + "'>" + nick + "</span>&gt; <span class='body'>" + body + "</span></div>");
                } else {
                    ChatApp.add_message("<div class='message action " + delay_css + "'>" + "* " + nick + " " + action[1] + "</div>");
                }
            } else {
                if (body.search('unlocked') > 0) {
                    ChatApp.unlocked = true;
                }
                ChatApp.add_message("<div class='notice'>*** " + body + "</div>");
            }
        }

        return true;
    },

    add_message : function(msg) {
        // detect if we are scrolled all the way down
        var chat = $('#chat').get(0);
        var at_bottom = chat.scrollTop >= chat.scrollHeight - chat.clientHeight;

        $('#chat').append(msg);

        // if we were at the bottom, keep us at the bottom
        if (at_bottom) {
            chat.scrollTop = chat.scrollHeight;
        }
    },

    on_private_message : function(message) {
        var from = $(message).attr('from');
        var room = Strophe.getBareJidFromJid(from);
        var nick = Strophe.getResourceFromJid(from);

        // make sure this message is from the correct room
        if (room === ChatApp.room) {
            var body = $(message).children('body').text();
            ChatApp.add_message("<div class='message private'>" + "@@ &lt;<span class='nick'>" + nick + "</span>&gt; <span class='body'>" + body + "</span> @@</div>");

        }

        return true;
    }
};

$(document).ready(function() {
    var name = randomNick();
    ChatApp.nickname = name;
    ChatApp.room = name + id_gen() + "@" + ChatApp.CONF_ADDR;

    $(document).trigger('connect');

    $('#leave').click(function() {
        $('#leave').attr('disabled', 'disabled');
        ChatApp.connection.send($pres({
            to : ChatApp.room + "/" + ChatApp.nickname,
            type : "unavailable"
        }));
        ChatApp.connection.disconnect();
    });

    $('#email').click(function() {

        var address = prompt("Please enter your email address", "email@example.com");

        if (email != null) {
            $.ajax({
                type : 'POST',
                url : '/email',
                data : {
                    log : $('#chat').html(),
                    email : address,
                    nickname : "Patron"
                },
                dataType : 'json',
                success : function(resp) {
                    console.info("Ajax Response is there.....");
                    console.log(resp);
                }
            });
            document.getElementById("demo").innerHTML = x;
        } else {
            alert('Invalid email address!');
        }
    });

    $('#input').keypress(function(ev) {
        if (ev.which === 13) {

            ev.preventDefault();

            var body = $(this).val();
            var match = body.match(/^\/(.*?)(?: (.*))?$/);
            var args = null;
            if (match) {
                if (match[1] === "msg") {
                    args = match[2].match(/^(.*?) (.*)$/);

                    if (ChatApp.participants[args[1]]) {
                        ChatApp.connection.send($msg({
                            to : ChatApp.room + "/" + args[1],
                            type : "chat"
                        }).c('body').t(body));
                        ChatApp.add_message("<div class='message private'>" + "@@ &lt;<span class='nick self'>" + ChatApp.nickname + "</span>&gt; <span class='body'>" + args[2] + "</span> @@</div>");
                    } else {
                        ChatApp.add_message("<div class='notice error'>" + "Error: User not in room." + "</div>");
                    }
                } else {
                    ChatApp.add_message("<div class='notice error'>" + "Error: Command is not allowed." + "</div>");
                }
            } else {
                if (ChatApp.room_created) {
                    // Room created :
                    // if bot is NOT in room
                    // invite bot again
                    if (!ChatApp.bot_in_room) {
                        ChatApp.connection.muc.invite(ChatApp.room, ChatApp.BOT, body);
                    }

                    // just send msg
                    ChatApp.connection.send($msg({
                        to : ChatApp.room,
                        type : "groupchat"
                    }).c('body').t(body));

                } else {
                    // Create room, toggle
                    // room_created, and send
                    // the message
                    ChatApp.connection.muc.invite(ChatApp.room, ChatApp.BOT, body);
                    ChatApp.room_created = true;

                    ChatApp.connection.send($msg({
                        to : ChatApp.room,
                        type : "groupchat"
                    }).c('body').t(body));

                }
            }

            $(this).val('');
        }
    });
});

$(document).bind('connect', function() {
    ChatApp.connection = new Strophe.Connection('http://bosh.metajack.im:5280/xmpp-httpbind');

    ChatApp.connection.connect(ChatApp.SERVER, null, function(status) {
        if (status === Strophe.Status.CONNECTED) {
            $(document).trigger('connected');
        } else if (status === Strophe.Status.DISCONNECTED) {
            $(document).trigger('disconnected');
        }
    });
});

$(document).bind('connected', function() {
    ChatApp.joined = false;
    ChatApp.participants = {};

    ChatApp.connection.send($pres().c('priority').t('-1'));

    ChatApp.connection.addHandler(ChatApp.on_presence, null, "presence");
    ChatApp.connection.addHandler(ChatApp.on_public_message, null, "message", "groupchat");
    ChatApp.connection.addHandler(ChatApp.on_private_message, null, "message", "chat");

    ChatApp.connection.send($pres({
        to : ChatApp.room + "/" + ChatApp.nickname
    }).c('x', {
        xmlns : ChatApp.NS_MUC
    }));

    ChatApp.connection.sendIQ($iq({
        to : ChatApp.room,
        type : "set"
    }).c('query', {
        xmlns : ChatApp.NS_MUC + "#owner"
    }).c('x', {
        xmlns : "jabber:x:data",
        type : "submit"
    }));

});

$(document).bind('disconnected', function() {
    ChatApp.connection = null;
    $('#room-name').empty();
    $('#room-topic').empty();
    $('#participant-list').empty();
    $('#chat').empty();
    $('#login_dialog').dialog('open');
});

$(document).bind('room_joined', function() {
    ChatApp.joined = true;

    $('#leave').removeAttr('disabled');
    $('#room-name').text(ChatApp.room);

    ChatApp.add_message("<div class='notice'>*** Room joined.</div>")
});

$(document).bind('user_joined', function(ev, nick) {
    ChatApp.add_message("<div class='notice'>*** " + nick + " joined.</div>");
});

$(document).bind('user_left', function(ev, nick) {
    ChatApp.add_message("<div class='notice'>*** " + nick + " left.</div>");
});

function randomNick() {
    var color_arr = ['atri', 'nigri', 'melano', 'cerule', 'cyano', 'viridi', 'chloro', 'albi', 'leuco', 'flav', 'xantho', 'pumili', 'nano', 'ingenti', 'colosso', 'grandi', 'macro', 'mega', 'brevi', 'brachy', 'proceri', 'alti', 'aepy', 'cyrto', 'gampso', 'ovat', 'plani', 'platy', 'cavi', 'coelo', 'cornut', 'cerato', 'circuli', 'cyclo', 'gyro', 'nudi', 'gymno', 'criniti', 'pogono', 'hirsut', 'lasio', 'trichodo', 'asper', 'trachy', 'spini', 'acantho', 'echino', 'corrugat', 'rugos', 'mono', 'uni', 'bi', 'duo', 'di', 'tri', 'tria', 'quadri', 'tetra', 'septem', 'hepta', 'decim', 'deca', 'allo', 'apato', 'bronto', 'compso', 'elasmo', 'nodo', 'ops', 'ornitho', 'raptor', 'stego', 'tyranno', 'clevergirl', 'michaelo', 'partygirl', 'depression', 'chubby', 'lol', 'noreen', 'shelli', 'maya', 'petero', 'cheong', 'shan', 'merle', 'coconut', 'apple', 'java', 'pythono', 'chambana', 'testing', 'bisexual'];

    var parts_arr = ['rostr', 'rhyncho', 'ungui', 'chelo', 'onycho', 'pedi', 'podo', 'capit', 'cephalo', 'caud', 'cerco', 'denti', 'odonto', '', '', '', '', '', '', '', '', '', '', '', '', '', ''];
    var saurus = 'saurus';
    var rand_nick = randomArrayValue(color_arr) + randomArrayValue(parts_arr) + saurus;
    return rand_nick;
}

function id_gen() {
    var text = "";
    var possible = "abcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 8; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function randomArrayValue(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}
