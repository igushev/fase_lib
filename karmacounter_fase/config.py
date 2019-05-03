from server_util import config_util

from karmacounter_fase import client as kc_client


def GetKarmaCounterClient(config):
  return kc_client.KarmaCounterClient(server_url=config.get('server', 'url'))


def Configurate(filename):
  karmacounter_fase_config = config_util.GetConfigByFilename(filename)
  kc_client.KarmaCounterClient.Set(GetKarmaCounterClient(karmacounter_fase_config))
