import pytumblr

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'gEimxWUm9Iexb18iieab5lRSp4Te0pu3r3SmPRmmHHzbqCZjuK',
  '4MOvfTSuZTJyUw0iA0e8nm2XkJQlEAiieY2RqU1eVMwsG8CkJC',
  'KlawXSusUrgdSaNJznJU1Ng2ho2PMFAsMdEhURpIoBy4YzrPGL',
  'Md7oV1P0YhAKSZSEcRF9ZWh3VkNRIJwfxJMJWxRpsv825JOX5M'
)

# Make the request
client.info()


#Creating a text post
client.create_text("KristaAndChris", state="published", slug="testing-text-posts", title="Testing", body="testing1 2 3 4")
