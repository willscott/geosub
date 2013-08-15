import tornado.template

url = "Email"

class Email:
  def __init__(self):
    self.template = template.Loader("template").load("email.html")

  def deliver(self, item, user, userprefs):
    email = userprefs.email_id
    body = self.template.generate(item)
    

