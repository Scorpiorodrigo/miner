import logging
import requests
from TwitchChannelPointsMiner.classes.Settings import Settings

logger = logging.getLogger(__name__)

class Whatsapp(object):
    __slots__ = ["phone", "apikey", "instance"]

    def __init__(self, phone: str, apikey: str):
        self.phone = phone
        self.apikey = apikey

    def send_bet_result(self, streamer: str, choice_title: str, amount: int, win: bool, total_points: int):
        """
        Envia o resultado da aposta formatado para o WhatsApp do usuário.
        """
        if not self.phone or not self.apikey:
            logger.warning("WhatsApp não configurado. Forneça o telefone e a apikey.")
            return

        status_emoji = "✅ GANHOU" if win else "❌ PERDEU"
        lucro_prejuizo = f"+{amount}" if win else f"-{amount}"

        # Mensagem formatada usando a sintaxe de negrito do próprio WhatsApp (*)
        message = (
            f"⚡ *RESULTADO DE APOSTA* ⚡\n\n"
            f"🎥 *Streamer:* {streamer}\n"
            f"🔮 *Opção:* {choice_title}\n"
            f"📊 *Status:* {status_emoji}\n"
            f"💰 *Resultado:* {lucro_prejuizo} pontos\n"
            f"🏦 *Saldo Atual:* {total_points} pontos"
        )

        # URL da API pública e gratuita do CallMeBot
        url = f"https://api.callmebot.com/whatsapp.php?phone={self.phone}&text={requests.utils.quote(message)}&apikey={self.apikey}"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                logger.info("Notificação de aposta enviada para o WhatsApp com sucesso!")
            else:
                logger.error(f"Falha ao enviar WhatsApp. Status: {response.status_code}, Resposta: {response.text}")
        except Exception as e:
            logger.error(f"Erro ao conectar com a API do WhatsApp: {e}")
