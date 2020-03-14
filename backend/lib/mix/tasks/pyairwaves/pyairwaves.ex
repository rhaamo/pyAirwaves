defmodule Mix.Tasks.Pyairwaves do
  use Mix.Task

  @shortdoc "Prints Pyairwaves help information"

  @moduledoc """
  Prints Pyairwaves tasks and their information.

      mix pyairwaves

  """

  @start_apps [
    :crypto,
    :ssl,
    :postgrex,
    :ecto,
    :ecto_sql
  ]
  @repos [
    Pyairwaves.Repo
  ]

  @doc false
  def run(args) do
    {_opts, args} = OptionParser.parse!(args, strict: [])

    case args do
      [] -> general()
      _ -> Mix.raise("Invalid arguments, expected: mix pyairwaves")
    end
  end

  defp general do
    Mix.shell().info("pyAirwaves v#{Pyairwaves.Application.version()}")
    Mix.shell().info("ADSB and AIS mapper and logger")
    Mix.shell().info("\nAvailable tasks:\n")
    Mix.Tasks.Help.run(["--search", "pyairwaves."])
  end

  @doc "Start the required stuff for the repository"
  def start_apps do
    IO.puts("Starting apps...")
    Enum.each(@start_apps, &Application.ensure_all_started/1)
    IO.puts("Starting repos.")
    Enum.each(@repos, & &1.start_link(pool_size: 2))
  end
end
