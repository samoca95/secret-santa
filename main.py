import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
# from google.colab import userdata # You can use this if you want to run this script in google collab

################################################################################
#################################### INPUTS ####################################
send_flag = False # Set to False if you don't want to send emails
print_pairs = True # Set to True if you want to print the pairs

# Names and emails:
participants = [
    ("Pedro", "user_1@example.com"),
    ("Maria", "user_2@example.com"),
    ("Juan", "user_3@example.com")
]

# Login info

# Email and pwd set in google collab
#sender_email = userdata.get('CT_EMAIL')
#sender_password = userdata.get('CT_PWD')

# Email and pwd set es environment variables
sender_email = os.environ.get('CT_EMAIL')
sender_password = os.environ.get('CT_PWD')
################################################################################

def generate_pairs(names):
  while True:
    try:
      missing = names.copy()
      assigned = [None] * len(names)
      for i, name in enumerate(names):
        missing_notme = [ miss for miss in missing if miss != name ]
        assigned[i] = np.random.choice(missing_notme)
        missing.remove(assigned[i])
      return dict(zip(names, assigned))
    except ValueError:
      pass # Keep searching

def send_email(sender_email, sender_password, recipient_email, subject, assigned_name):
  message = MIMEMultipart("alternative")
  message['Subject'] = subject
  message['From'] = sender_email
  message['To'] = recipient_email

  text_body = f"Hey {name} 🎅, this is yout secret santa {assigned_name}. 🎁"
  html_body = f'''
    <html>
    <body>
      <h1>🎅🏻 ¡Secret Santa arrived! 🎄</h1>

      <p><strong>Happy you!</strong> You need to prepare a gift for:</p>
      <p style="font-size: 1.5em; text-align: center; color: blue;"><strong>{assigned_name}</strong> ❤</p>
    </body>
    </html>
    '''

  # Attach both plain text and HTML versions
  message.attach(MIMEText(text_body, "plain"))
  message.attach(MIMEText(html_body, "html"))

  try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
      server.starttls()
      server.login(sender_email, sender_password)
      server.send_message(message)
      print(f"Email sent to {recipient_email}")
  except Exception as e:
    print(f"Error sending email to {recipient_email}: {e}")

# Generate pairs
names = [name for name, _ in participants]
pairs = generate_pairs(names)
if print_pairs:
  print(pairs)

# Send emails
if send_flag:
  if not sender_email or not sender_password:
    print("Please set the CT_EMAIL and CT_PWD environment variables.")
    exit
  else:
    for name, email in participants:
      assigned_name = pairs[name]
      subject = f"{name}, this is your Secret Santa!"
      send_email(sender_email, sender_password, email, subject, assigned_name)
