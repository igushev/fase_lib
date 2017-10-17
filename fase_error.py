import fase_model


SERVICE_NOT_FOUND = fase_model.BadRequest(
  code=101,
  message='Service with such name has not been found!')
