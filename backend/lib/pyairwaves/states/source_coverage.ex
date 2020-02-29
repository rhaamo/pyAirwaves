defmodule Pyairwaves.States.SourceCoverage do
  use GenServer
  require Logger

  # The state is key-value
  # The key is "{source name}_{source type}", ex: "foo_airAIS", "bar_airADSB"
  # The value is a map, %{source_id: 0, lat: 0, lon:0, bearings: [{bearing: 0, distance: 0}]}
  # source_id is the ArchiveSource ID in the database
  # lat and lon are the one of the source
  # The bearings list is a map of the actual bearing (1 to 360, ideally only every 30 degrees), and distance (in meters)
  # Only the longuest distance for each bearing is in this list

  def start_link(_) do
    GenServer.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  def init(:ok) do
    {:ok, :ets.new(:source_coverage, [:named_table, :protected])}
  end

  def find(name) do
    case :ets.lookup(:source_coverage, name) do
      [{^name, items}] -> {:ok, items}
      [] -> :error
    end
  end

  def new(list) do
    GenServer.call(__MODULE__, {:new, list})
  end

  def add(name, item) do
    GenServer.call(__MODULE__, {:add, name, item})
  end

  def handle_call({:new, name}, _from, table) do
    case find(name) do
      {:ok, name} ->
        {:reply, name, table}

      :error ->
        :ets.insert(table, {name, []})
        {:reply, [], table}
    end
  end

  def handle_call({:add, name, item}, _from, table) do
    case find(name) do
      {:ok, items} ->
        items = [item | items]
        :ets.insert(table, {name, items})
        {:reply, items, table}

      :error ->
        {:reply, {:error, :list_not_found}, table}
    end
  end
end
