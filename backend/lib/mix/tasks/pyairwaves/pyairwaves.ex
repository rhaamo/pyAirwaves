defmodule Mix.Tasks.Pyairwaves do
  use Mix.Task

  @shortdoc "Prints Pyairwaves help information"

  @moduledoc """
  Prints Pyairwaves tasks and their information.

      mix pyairwaves

  """

  @doc false
  def run(args) do
    {_opts, args} = OptionParser.parse!(args, strict: [])

    case args do
      [] -> general()
      _ -> Mix.raise("Invalid arguments, expected: mix pyairwaves")
    end
  end

  defp general() do
    Mix.shell().info("pyAirwaves v#{Pyairwaves.Application.version()}")
    Mix.shell().info("ADSB and AIS mapper and logger")
    Mix.shell().info("\nAvailable tasks:\n")
    Mix.Tasks.Help.run(["--search", "pyairwaves."])
  end
end
