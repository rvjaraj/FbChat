from fbchat import log, Client, Message
from os.path import join, dirname
from ibm_watson import AssistantV2, LanguageTranslatorV3, TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

correo = "ups_uclqlhf_chatt@tfbnw.net"
contra = "***123456789"
#Envia = chat_hkaepat_ups@tfbnw.net

#Connectamos al chatboot
authenticator = IAMAuthenticator('U4IKxuhQ4XBIrskFYSLLqrB29b_A2fch9uL4gWQUZ-f4')
assistant = AssistantV2(
    version='2018-09-20',
    authenticator=authenticator)
assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/20d0e70b-3f11-4c02-9137-205d38b948a9')
assistant.set_disable_ssl_verification(False)
session = assistant.create_session("633359aa-4a7e-4cfa-8ebe-78113a86ad21").get_result()

authenticatorT = IAMAuthenticator('0Iobj63HD2qz6ChKXOCkc1kARMJ8E9-Gkq1045FQIGf7')
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticatorT)
language_translator.set_service_url('https://gateway.watsonplatform.net/language-translator/api')

authenticatorV = IAMAuthenticator('rQkJz0iTpTyboZqk6SymQ2hh6zfG7sfmxdZBD9V9qQIV')
service = TextToSpeechV1(authenticator=authenticatorV)
service.set_service_url('https://stream.watsonplatform.net/text-to-speech/api')


def mensaje(text, session):
    message = assistant.message("633359aa-4a7e-4cfa-8ebe-78113a86ad21",
        session["session_id"],
        input={'message_type': 'text','text': text}).get_result()
    return (message['output']['generic'][0]['text'])

def traducir(text,language_translator):
    translation = language_translator.translate(
        text=text, model_id='en-es').get_result()
    return translation['translations'][0]['translation']

def voz(text, service):
    with open(join(dirname(__file__), 'output.mp3'),
              'wb') as audio_file:
        response = service.synthesize(
            text, accept='audio/mp3',
            voice="es-LA_SofiaV3Voice").get_result()
        audio_file.write(response.content)



class EchoBot(Client):
   def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
           self.markAsDelivered(thread_id, message_object.uid)
           self.markAsRead(thread_id)
           if author_id != self.uid:
               messenger = message_object.text
               print(messenger)
               traduccion = traducir(messenger, language_translator)
               print(traduccion)
               respuesta = mensaje(traduccion,session)
               print(respuesta)
               voz(respuesta, service)
               #self.send(Message(text=respuesta), thread_id=thread_id, thread_type=thread_type)
               self.sendLocalVoiceClips('output.mp3',Message(text=respuesta),thread_id=thread_id, thread_type=thread_type)

client = EchoBot(correo,contra)
client.listen()

