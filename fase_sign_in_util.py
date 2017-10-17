import datetime
import functools
import hashlib

import activation_code_generator
import sms_sender
import fase_database
import fase_model
import fase


class SignInUtil(fase.Service):

  def SignInProcedure(self, screen, skip_option=False, cancel_option=False, on_done=None):
    self.SaveScreen(id_='sign_in_screen')
    self.SaveCallback(id_='sign_in_on_done_callback')
    screen = fase.Screen()
    sign_in_layout = screen.AddLayout(id_='sign_in_layout', orientation=fase.Layout.VERTICAL)
    sign_in_layout.AddButton(id='sign_in', text='Sign In', on_click=self.OnSignInOption)
    sign_in_layout.AddButton(id='sign_up', text='Sign Up', on_click=self.OnSignUpOption)
    screen.AddPrevStepButton(on_click=self.OnSignInCancel)
    return screen

  def OnSignInOption(self, screen):
    screen = fase.Screen()
    sign_in_layout = screen.AddLayout(id_='sign_in_layout', orientation=fase.Layout.VERTICAL)
    sign_in_layout.AddText(id_='phone_number', hint='Phone Number')
    sign_in_layout.AddButton(id='sign_in', text='Sign In', on_click=self.OnSignInEnteredData)
    screen.AddPrevStepButton(on_click=self.OnSignInCancel)
    return screen
    
  def OnSignInEnteredData(self, screen):
    phone_number = screen.GetText(id_='phone_number')
    user = fase_database.FaseDatabase.Get().GetUserByPhoneNumber(phone_number)
    if not user:
      return fase.Popup('User with such phone number has not been found!')
    return self._OnEnteredData(phone_number, user.user_id)

  def OnSignUpOption(self, screen):
    screen = fase.Screen()
    sign_up_layout = screen.AddLayout(id_='sign_up_layout', orientation=fase.Layout.VERTICAL)
    sign_up_layout.AddText(id_='phone_number', hint='Phone Number')
    sign_up_layout.AddText(id_='first_name', hint='First Name')
    sign_up_layout.AddText(id_='last_name', hint='Last Name')
    sign_up_layout.AddButton(id='sign_in', text='Sign In', on_click=self.OnSignUpEnteredData)
    screen.AddPrevStepButton(on_click=self.OnSignInCancel)
    return screen
    
  def OnSignUpEnteredData(self, screen):
    phone_number = screen.GetText(id_='phone_number')
    if fase_database.FaseDatabase.Get().GetUserByPhoneNumber(phone_number):
      return fase.Popup('User with such phone number is already registered!')

    datetime_now = datetime.datetime.now()
    user_id_hash = hashlib.md5()
    user_id_hash.update(datetime_now.strftime(fase.DATETIME_FORMAT_HASH))
    user_id_hash.update(phone_number)
    user_id = user_id_hash.hexdigest()
    
    user = fase_model.User(user_id=user_id,
                            phone_number=screen.GetText(id_='phone_number').GetText(),
                            first_name=screen.GetText(id_='first_name').GetText(),
                            last_name=screen.GetText(id_='last_name').GetText(),
                            datetime_added=datetime_now)
    fase_database.FaseDatabase.Get().AddUser(user)
    return self._OnEnteredData(phone_number, user_id)

  def _OnEnteredData(self, phone_number, user_id):
    activation_code = activation_code_generator.ActivationCodeGenerator.Get().Generate()
    sms_sender.SMSSender.Get().SendSMS(phone_number, activation_code)
    screen = fase.Screen()
    text_layout = screen.AddLayout(id_='text_layout', orientation=fase.Layout.VERTICAL)
    text_layout.AddText(id_='activation_code', hint='Activation Code')
    text_layout.AddButton(
        id_='send', text='Send',
        on_click=functools.partial(self.OnActivationCodeSend, phone_number, user_id, activation_code))
    screen.AddPrevStepButton(on_click=self.OnSignInCancel)
    return screen
    
  def OnActivationCodeSend(self, phone_number, user_id, activation_code, screen):
    if screen.GetText(id_='activation_code').GetText() != activation_code:
      return fase.Popup('Wrong activation code!')
    self.SetUserId(user_id)
    screen = self.PopScreen(id_='sign_in_screen')
    on_done = self.PopCallback(id_='sign_in_on_done_callback')
    on_done(screen, False)

  def OnSignInCancel(self):
    screen = self.PopScreen(id_='sign_in_screen')
    on_done = self.PopCallback(id_='sign_in_on_done_callback')
    on_done(screen, True)
