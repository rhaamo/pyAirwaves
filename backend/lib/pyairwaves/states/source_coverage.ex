defmodule Pyairwaves.States.SourceCoverage do
  use GenServer
  require Logger

  # The state is key-value
  # The key is the source ID from ArchiveSource db entry
  # The value is a map, %{lat: 0, lon:0, bearings: {bearing => distance}}
  # lat and lon are the one of the source
  # The bearings list is a map of the actual bearing (1 to 360, ideally only every 30 degrees, float), and distance (in meters, integer)
  # Only the longuest distance for each bearing is in this list

  def start_link(_) do
    GenServer.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  defp prefill_from_db(table) do
    Pyairwaves.Repo.all(Pyairwaves.ArchiveSource)
    |> Enum.each(fn source ->
      if not is_nil(source.coverage) and length(source.coverage) > 0 do
        sc =
          Enum.map(source.coverage, fn x ->
            %{x.bearing => x.distance}
          end)

        bearings =
          Enum.reduce(sc, fn x, acc ->
            Map.merge(x, acc)
          end)

        # add that map to the struct
        {lon, lat} = source.geom.coordinates

        c_struct =
          %{lat: lat, lon: lon}
          |> Map.put(:bearings, bearings)

        # insert in the state
        :ets.insert(table, {source.id, c_struct})
        Logger.info("Loaded Source Coverage state from db.")
      end
    end)
  end

  def init(:ok) do
    table = :ets.new(:source_coverage, [:named_table, :protected])
    prefill_from_db(table)
    # schedule the periodic flush
    schedule_flush_db()
    {:ok, table}
  end

  def find(name) do
    case :ets.lookup(:source_coverage, name) do
      [{^name, items}] -> {:ok, items}
      [] -> :error
    end
  end

  @doc "Add a bearing/distance into the state"
  def add(source_id, coverage) do
    GenServer.call(__MODULE__, {:add, source_id, coverage})
  end

  def handle_call({:new, source_id}, _from, table) do
    case find(source_id) do
      {:ok, source_id} ->
        {:reply, source_id, table}

      :error ->
        :ets.insert(table, {source_id, []})
        {:reply, [], table}
    end
  end

  def handle_call({:add, source_id, coverage}, _from, table) do
    case find(source_id) do
      {:ok, coverages} ->
        :ets.delete(table, source_id)

        # get the previous and next distance
        prev_distance = Map.get(coverages.bearings, coverage.bearing, nil)
        new_distance = coverage.distance

        # conditionally update new_bearings if the new distance is > old one or just return the bearings
        # if nil (not present in struct, new bearing) or anything else (inferior)
        new_bearings =
          case prev_distance do
            prev_distance when prev_distance < new_distance ->
              # Logger.debug("prev < new #{prev_distance} < #{new_distance}")
              Map.put(coverages.bearings, coverage.bearing, coverage.distance)

            nil ->
              Map.put(coverages.bearings, coverage.bearing, coverage.distance)

            _ ->
              coverages.bearings
          end

        c_new = Map.put(coverages, :bearings, new_bearings)
        :ets.insert(table, {source_id, c_new})
        {:reply, coverages, table}

      :error ->
        # build new bearings map
        bearings =
          %{}
          |> Map.put(coverage.bearing, coverage.distance)

        # add that map to the struct
        c_struct =
          %{lat: coverage.lat, lon: coverage.lon}
          |> Map.put(:bearings, bearings)

        # insert in the state
        :ets.insert(table, {source_id, c_struct})
        {:reply, c_struct, table}
    end
  end

  def schedule_flush_db() do
    # every hours
    Process.send_after(self(), :flush_to_db, 1 * 60 * 60 * 1000)
  end

  def handle_info(:flush_to_db, state) do
    Logger.debug("Syncing in-memory coverage datas to database.")

    Pyairwaves.Repo.all(Pyairwaves.ArchiveSource)
    |> Enum.each(fn source ->
      case find(source.id) do
        {:ok, coverage} ->
          # from: {bearing => distance, bearing => distance...}
          # to: [{bearing: x, distance: x}, {bearing: x, distance: x}...]
          db_coverages =
            Enum.map(coverage.bearings, fn {bearing, distance} ->
              %{bearing: bearing, distance: distance}
            end)

          new_source = Ecto.Changeset.change(source, coverage: db_coverages, coverage_updated_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second))

          case Pyairwaves.Repo.update(new_source, log: false) do
            {:ok, _struct} -> Logger.info("Source Coverage state synced.")
            {:error, changeset} -> Logger.error("Cannot sync Source Coverage state.", changeset)
          end

        :error ->
          Logger.info("Source Coverage state datas not yet available.")
      end
    end)

    # re-schedule the task to run in some time
    schedule_flush_db()
    {:noreply, state}
  end
end
