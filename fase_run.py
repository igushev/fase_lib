import fase_client
import fase_tk_ui_imp
import fase_ui
import fase_http_client


def Run(fase_server_url):
  http_client = fase_http_client.FaseHTTPClient(fase_server_url)
  ui_imp = fase_tk_ui_imp.FaseTkUIImp()
  ui = fase_ui.FaseUI(ui_imp)
  client = fase_client.FaseClient(http_client, ui)
  client.Run()