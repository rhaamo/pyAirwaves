# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

# DB config
config :pyairwaves,
  ecto_repos: [Pyairwaves.Repo]

config :pyairwaves, Pyairwaves.Repo,
  adapter: Ecto.Adapters.Postgres,
  types: Pyairwaves.PostgresTypes,
  username: "pyairwaves",
  password: "",
  database: "pyairwaves",
  hostname: "127.0.0.1",
  pool_size: 10

# Configuration of the PubSub Redis server used between the backend and the data parsers
config :pyairwaves, redis: "redis://127.0.0.1:6379/4"

config :pyairwaves, :ais_client, host: "127.0.0.1", port: 10110, pos_mode: 0, name: "local", lon: 0.0, lat: 0.0

# Configures the endpoint
config :pyairwaves, PyairwavesWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "+suJD4RiZN0AFqOGYPGZJUVOhaVnEovOOO8Jt7ft3xrzwlW6OTZ++2eJc/vxrQKr",
  render_errors: [view: PyairwavesWeb.ErrorView, accepts: ~w(html json)],
  live_view: [signing_salt: "q2gfUiPH"],
  pubsub: [name: Pyairwaves.PubSub, adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

config :logger,
  backends: [:console, Sentry.LoggerBackend]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Sams for Geo Postgis
config :geo_postgis,
  json_library: Jason

# Optional sentry config
config :sentry,
  environment_name: Mix.env(),
  included_environments: [:prod],
  enable_source_code_context: true,
  root_source_code_path: File.cwd!()

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
