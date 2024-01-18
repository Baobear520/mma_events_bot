from dotenv import dotenv_values

env = dotenv_values("project/.env")
print(env["MMA_BOT_TOKEN"])