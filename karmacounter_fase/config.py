from fase_lib.server_util import config_util

import client as kc_client


def GetKarmaCounterClient(config):
  return kc_client.KarmaCounterClient(server_url=config.get('server', 'url'))


def Configurate(filename):
  karmacounter_fase_config = config_util.GetConfigFromFile(filename)
  kc_client.KarmaCounterClient.Set(GetKarmaCounterClient(karmacounter_fase_config))
