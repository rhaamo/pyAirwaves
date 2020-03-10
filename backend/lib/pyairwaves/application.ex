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
      Pyairwaves.States.SourceCoverage,
      # Supervisor for all AIS Clients
      Pyairwaves.AisClientsSupervisor,
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Pyairwaves.Supervisor]
    ret = Supervisor.start_link(children, opts)

    # Start AIS Clients
    Pyairwaves.AisClientsSupervisor.start_ais_clients()

    # Return the supervisor
    ret
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  def config_change(changed, _new, removed) do
    PyairwavesWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
