defmodule Pyairwaves.ClientsStarter do
  use GenServer
  require Logger

  def start_link(_) do
    GenServer.start_link(__MODULE__, [])
  end

  def init(state) do
    Pyairwaves.AisClientsSupervisor.start_ais_clients()
    {:ok, state}
  end
end
