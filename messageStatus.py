import twilio.twiml.messaging_response
from twilio.rest import Client
from config import Config


def acount_sid_anonimizer(account_sid):
    # AC825ba77fb3d263cab93195d727f5e0df
    # acount_sid_anonimizer(message.account_sid)
    # print("message.account_sid:      :::", message.account_sid)  # TODO DONT PRINT THIS
    out_account_sid = account_sid[0]
    for count, char in enumerate(account_sid):
        if count == 0:
            continue
        out_account_sid = out_account_sid + "X"
    return out_account_sid


def message_uri_anonimizer(uri):
    uri = uri.split("/")
    uri[3] = acount_sid_anonimizer(uri[3])
    #uri[5] = acount_sid_anonimizer(uri[5])
    uri = "/".join(uri)
    return uri


def list_all_messages():
    """
    {
          "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
          "api_version": "2010-04-01",
          "body": "This is the ship that made the Kessel Run in fourteen parsecs?",
          "date_created": "Thu, 30 Jul 2015 20:12:31 +0000",
          "date_sent": "Thu, 30 Jul 2015 20:12:33 +0000",
          "date_updated": "Thu, 30 Jul 2015 20:12:33 +0000",
          "direction": "outbound-api",
          "error_code": null,
          "error_message": null,
          "from": "+15017122661",
          "messaging_service_sid": null,
          "num_media": "0",
          "num_segments": "1",
          "price": null,
          "price_unit": null,
          "sid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
          "status": "sent",
          "subresource_uris": {
            "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Media.json"
          },
          "to": "+15558675310",
          "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json"
        }
    :return:
    """
    # Your Account SID from twilio.com/console
    account_sid = Config.TWILLIO_SID
    # Your Auth Token from twilio.com/console
    auth_token = Config.TWILLIO_TOKEN

    client = Client(account_sid, auth_token)
    count = 0
    count_filter = 1
    for message in client.messages.list():
        count = count + 1
        #if len(str(message.body))> 160:
        #if "2021-10-12" in str(message.date_sent):
        # if message.price and message.price is not None:
        #     if float(message.price) < -0.045:
                #count_filter = count_filter + 1
        print("=" * 120)
        print("type(message)             :::", type(message))
        print("message.sid:              :::", message.sid)
        print("message.Status():         :::", message.status)
        print("message.price_unit:       :::", message.price_unit)
        print("message.price:            :::", message.price)
        print("message.body              :::", message.body)
        print("# message_characters      :::", len(message.body))
        print("message.numsegments:      :::", message.num_segments)
        print("message.to:               :::", message.to)
        print("message.from_:            :::", message.from_)
        print("message.date_updated:     :::", message.date_updated)
        print("message.date_created:     :::", message.date_created)
        print("message.direction:        :::", message.direction)
        print("dir(message.date_sent)    :::", message.date_sent, type(message.date_sent))
        #print("message.uri:              :::", message.uri)
        print("message.uri:              :::", message_uri_anonimizer(message.uri))
        print("message.error_code:       :::", message.error_code)
        #print("message.fetch():          :::", message.fetch())  # #TODO DONT PRINT THIS
        #print("message.account_sid:      :::", message.account_sid) #TODO DONT PRINT THIS
        print("message.account_sid:      :::", acount_sid_anonimizer(message.account_sid))

        #print("message.feedback:         :::", message.feedback)  # TODO DONT PRINT THIS
        #print("message.subresource_uris: :::", message.subresource_uris)  # TODO DONT PRINT THIS
        #print("message.api_version:      :::", message.api_version)  # TODO DONT PRINT THIS
        #print("message:                  :::", message)  # TODO DONT PRINT THIS

    # print("Numero mensagens (TOTAL)  ::: ", count)


    return count_filter


def get_messages_bigger_than():
    # Your Account SID from twilio.com/console
    account_sid = Config.TWILLIO_SID
    # Your Auth Token from twilio.com/console
    auth_token = Config.TWILLIO_TOKEN

    client = Client(account_sid, auth_token)

    count_message_body = 0
    count_message_body1 = 0
    data = [] # para mensagens >160
    data1 = [] # mensagens =<160
    output = [] # para mensagens >160
    output1 = [] # mensagens =<160
    for message in client.messages.list():
        if len(message.body) > 160:
            count_message_body = count_message_body + 1
            data = message.sid, message.price, str(message.date_sent), message.body, message.direction, \
                   message.from_, message.to, message.body
            output.append(data)
            data = []
        else:
            count_message_body1 = count_message_body1 + 1
            data1 = message.sid, message.price, str(message.date_sent), message.body, message.direction, \
                   message.from_, message.to, message.body
            output1.append(data1)
            data1= []


    output.insert(0, ["TOTAL", count_message_body])
    output1.insert(0, ["TOTAL", count_message_body1])

    final = {"MensagensMAiores160":output,
             "mensagensMenoresIgual160": output1}
    return final


def count_all_messages():
    # Your Account SID from twilio.com/console
    account_sid = Config.TWILLIO_SID
    # Your Auth Token from twilio.com/console
    auth_token = Config.TWILLIO_TOKEN

    client = Client(account_sid, auth_token)
    count = 0
    count_filter = 0

    prices = []
    prices1 = []
    all_prices = []
    # print(" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print("@@@@@@@@@@@@@   list_all_messages()     @@@@@@@@@@@@@@@@@@@@@@")
    # print(" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    list_all_messages()
    # print(len(client.messages.list()))
    output_messages = client.messages.list()  # TODO export all messages here ?

    for message in client.messages.list():
        count = count + 1
        all_prices.append(message.price)
        if message.price and message.price is not None:
            prices.append(float(message.price))
            prices1.append(message.price)

    # print(" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print("@@@@@@@@@@@@@   count_all_messages()     @@@@@@@@@@@@@@@@@@@@@@")
    # print(" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print("message.numsegments:      :::", message.num_segments)
    # print("prices (FLOAT)            :::", prices)
    # print("prices1 (string)          :::", prices1)
    # print("all_prices (string all))  :::", all_prices)
    # print("sum(prices))              :::", sum(prices) * -1)
    # print("len(prices)               :::", len(prices))
    # print("len(prices1)              :::",len(prices1))
    # print("len(all_prices)           :::", len(all_prices))
    # print("# MENSAGENS REAIS (TOTAL) :::", count)
    # print("# MENSAGENS EFECTIVAS PARA CONTAGEM (ATE 160 CARACTREs) :::", int((round(sum(prices)*-1 , 4) / 0.045)))
    custo = round( sum(prices)*-1,  4)

    resultado = get_messages_bigger_than()
    output = {"totalMensagens(REAL/TOTAL)": count,
              "mensagensEfectivasParaPagamento": int((round( sum(prices) * -1, 4)  / 0.045)),
              "custoTotalMensagens(EUROS)": sum(prices) * -1,
              }
    print("-------------")
    print("REPORT:")
    print("-------------")
    print("Numero mensagens REAIS                  (TOTAL)       ::: ", output["totalMensagens(REAL/TOTAL)"])
    print("Numero mensagens EFECTIVAS A PAGAMENTO  (TOTAL)       ::: ", output["mensagensEfectivasParaPagamento"])
    print("CUSTO TOTAL                             (EUROS)       ::: ", output["custoTotalMensagens(EUROS)"])


    return output





if __name__ == '__main__':
    #list_all_messages()
    import json

    # print("=" * 120)
    #print(f"[ START ] counting all messages")
    data_dict = count_all_messages()
    print("---")
    print(json.dumps(data_dict, indent=4))

    # print(" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print("@@@@@@@@@@@@@   get_messages_bigger_than()     @@@@@@@@@@@@@@@@@@@@@@")
    # print(" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #resultado = get_messages_bigger_than()
    #output.update(resultado)