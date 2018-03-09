from server_util import config_util

from karmacounter_fase import client as kc_client


def GetKarmaCounterClient(config):
  return kc_client.KarmaCounterClient(server_url=config.get('server', 'url'))


karmacounter_fase_config = config_util.GetConfig('KARMACOUNTER_FASE_CONFIG_FILENAME')
kc_client.KarmaCounterClient.Set(GetKarmaCounterClient(karmacounter_fase_config))
