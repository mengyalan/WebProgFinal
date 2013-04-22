
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