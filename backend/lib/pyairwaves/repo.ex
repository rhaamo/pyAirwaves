defmodule Pyairwaves.Repo do
  use Ecto.Repo,
    otp_app: :pyairwaves,
    adapter: Ecto.Adapters.Postgres
end
