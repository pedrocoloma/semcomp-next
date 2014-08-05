var pingTimer = null;

function handleVisibilityChange() {
	clearInterval(pingTimer);
	if (document[hidden]) {
		pingTimer = setInterval(pingMessages, 15 * 60 * 1000);
	} else {
		pingMessages()
		// O delay aqui é menor do que na chamada fora do handler
		// porque se entrou aqui, eu posso setar uma frequência
		// mais baixa sem medo de ficar fazendo requisições pra sempre.
		// se entrou aqui é porque tudo isso funciona então alguma hora
		// vai parar de mandar pings
		pingTimer = setInterval(pingMessages, 10 * 1000);
	}
}

document.addEventListener(visibilityChange, handleVisibilityChange, false);

pingMessages();

pingTimer = setInterval(pingMessages, 60 * 1000);
