# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

config :pyairwaves,
  ecto_repos: [Pyairwaves.Repo]

# Configures the endpoint
config :pyairwaves, PyairwavesWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "+suJD4RiZN0AFqOGYPGZJUVOhaVnEovOOO8Jt7ft3xrzwlW6OTZ++2eJc/vxrQKr",
  render_errors: [view: PyairwavesWeb.ErrorView, accepts: ~w(html json)],
  pubsub: [name: Pyairwaves.PubSub, adapter: Phoenix.PubSub.PG2],
  live_view: [signing_salt: "q2gfUiPH"],
  pubsub: [name: PyairwavesWeb.PubSub, adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
