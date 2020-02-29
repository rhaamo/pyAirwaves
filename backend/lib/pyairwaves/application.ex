defmodule Pyairwaves.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @version Mix.Project.config()[:version]

  def version, do: @version

  def start(_type, _args) do
    # List all child processes to be supervised
    children = [
      # Start the Ecto repository
      Pyairwaves.Repo,
      # Start the endpoint when the application starts
      PyairwavesWeb.Endpoint,
      # Starts a worker by calling: Pyairwaves.Worker.start_link(arg)
      # {Pyairwaves.Worker, arg},
      Pyairwaves.RedisEater,
      # Handle the in-memory source coverage plot
      Pyairwaves.States.SourceCoverage
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Pyairwaves.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  def config_change(changed, _new, removed) do
    PyairwavesWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
