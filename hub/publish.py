import store
import hub
import time
import json
import smtplib

from email.mime.text import MIMEText

class Publisher:
  """  """

  from_email_address = "iamrohitbanga@banga-pc"
  delivery_mechanisms = ['email']

  def __init__(self, db):
    self.store = store.Store(db)

  def start(self):
    while True:
      print "time to send emails"

      users = self.store.db.execute("select id, prefs from users")
      # storing current ts in class variable so all notifications done in
      # this iteration use the same timestamp
      self.current_ts = time.time()

      print "current time is " + str(self.current_ts)
      print "users: "

      for (uid, prefs_json) in users:
        print uid
        prefs = json.loads(prefs_json)
        print prefs
        print prefs['publish_log']
        if u'publish_log' not in prefs:
            prefs['publish_log'] = {'last_notification_time' : '0'}
        publish_log = prefs['publish_log']
        print publish_log
        last_notification_time = publish_log['last_notification_time']
        print last_notification_time
        notifications = self.get_notifications_for_user(uid, last_notification_time)
        self.send_notifications(uid, prefs, notifications)
        print publish_log
        publish_log['last_notification_time'] = self.current_ts
        print publish_log
        print prefs
        self.store.db.execute('update users set prefs=(?) where id=(?)', (json.dumps(prefs), uid))
        self.store.db.commit()
      time.sleep(60)

  def get_notifications_for_user(self, uid, last_notification_time):
    categories_for_user = self.store.db.execute("select category from rules where user=(?)", uid)
    notifications = []
    print "looking for notifications to send"
    for category in categories_for_user:
      print category
      print type(category)
      new_items = self.store.db.execute("select id, category, data from items where category=(?) and ts > (?)",
                      (category[0], last_notification_time))
      print str(new_items)
      for (item_id, item_category, item_data) in new_items:
        notification = {}
        notification['item_id'] = item_id
        notification['category'] = item_category
        notification['notification_email'] = json.dumps(item_data)
        notifications.append(notification)
    return notifications

  def send_notifications(self, uid, prefs, notifications):
    print "sending notifications"
    for mechanism in self.delivery_mechanisms:
        print mechanism
        if mechanism == 'email':
            self.send_email_notifications(uid, prefs, notifications)

  def send_email_notifications(self, uid, prefs, notifications):
    print "ready to send email to " + str(uid)
    email_body = self.format_notifications_for_email(notifications)
    print "email body is " + str(email_body)
    msg = MIMEText(email_body)
    msg['Subject'] = "Updates for you"
    msg['From'] = self.from_email_address
    msg['To'] = prefs['email_id']
    print "sending email to: " + prefs['email_id']
    s = smtplib.SMTP('localhost')
    s.sendmail(self.from_email_address, prefs['email_id'], msg.as_string())
    s.quit()

  def format_notifications_for_email(self, notifications):
    email_body = "notifications: " + str(time.time()) + " " + str(notifications)
    return email_body

def main():
    app = Publisher("live")
    app.start()

if __name__ == "__main__":
    main()

