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
    },

    on_public_message : function(message) {
    },

    add_message : function(msg) {
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
