defmodule Pyairwaves.States.SourceCoverage do
  use GenServer
  require Logger

  # The state is key-value
  # The key is "{source name}_{source type}", ex: "foo_airAIS", "bar_airADSB"
  # The value is a map, %{source_id: 0, lat: 0, lon:0, bearings: [{bearing: 0, distance: 0}]}
  # source_id is the ArchiveSource ID in the database
  # lat and lon are the one of the source
  # The bearings list is a map of the actual bearing (1 to 360, ideally only every 30 degrees, float), and distance (in meters, integer)
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

  @doc "Add a bearing/distance into the state"
  def add(source_name, coverage) do
    GenServer.call(__MODULE__, {:add, source_name, coverage})
  end

  def handle_call({:new, source_name}, _from, table) do
    case find(source_name) do
      {:ok, source_name} ->
        {:reply, source_name, table}

      :error ->
        :ets.insert(table, {source_name, []})
        {:reply, [], table}
    end
  end

  def handle_call({:add, source_name, coverage}, _from, table) do
    # find source_name
    # if not found, create it
    # then add or mix the src_struct{bearings: ...bearing_dist}
    case find(source_name) do
      {:ok, items} ->
        items = [coverage | items]
        :ets.insert(table, {source_name, items})
        {:reply, items, table}

      :error ->
        {:reply, {:error, :list_not_found}, table}
    end
  end
end
