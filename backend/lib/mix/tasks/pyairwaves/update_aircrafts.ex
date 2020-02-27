defmodule Mix.Tasks.Pyairwaves.UpdateAircrafts do
  use Mix.Task
  import Mix.Tasks.Pyairwaves

  require Logger

  @moduledoc """
  Update the list of known aircrafts models

  Cron recommanded: run one time per month
  """

  # FIXME TODO; The initial list contains multiple ModelFullName per Designator
  # We need to rebuild a new list, with unique Designator and a ModelFullName concatennating all the available ones

  defp parse_aircraft(aircraft) do
    aircraft_shadow =
      "generic_#{String.slice(aircraft["EngineType"], 0, 1)}#{aircraft["EngineCount"]}#{
        aircraft["WTC"]
      }.png"

    engine_count =
      case aircraft["Enginecount"] do
        "C" -> 1
        nil -> 1
        _ -> String.to_integer(aircraft["Enginecount"])
      end

    %{
      icao: aircraft["Designator"],
      type: aircraft["ModelFullName"],
      manufacturer: aircraft["ManufacturerCode"],
      aircraft_description: aircraft["AircraftDescription"],
      aircraft_shadow: aircraft_shadow,
      engine_type: aircraft["EngineType"],
      engine_count: engine_count,
      wake_category: aircraft["WTC"]
    }
  end

  # The initial dataset contains one entry per ModelFullName, we want only one per ICAO ID
  # We should dedupe the list and concat the ModelFullName per ICAO ID
  defp dedupe_list(from, to) when length(from) > 0 do
    [item | tail] = from

    type =
      if Map.has_key?(to, item["Designator"]) do
        Map.get(to, item["Designator"])["ModelFullName"] <> ", " <> item["ModelFullName"]
      else
        item["ModelFullName"]
      end

    new_entry = item |> Map.put("ModelFullName", type)

    new_to = Map.put(to, item["Designator"], new_entry)

    dedupe_list(tail, new_to)
  end

  defp dedupe_list(from, to) when length(from) == 0 do
    to
  end

  @shortdoc "Update the list of known aircrafts models"
  def run(_) do
    # start the required apps & repos
    start_apps()

    Logger.info("Starting aircrafts update. (Online)")
    Logger.info("This can take some time.")
    HTTPoison.start()

    url = "https://www4.icao.int/doc8643/External/AircraftTypes"

    headers = [
      "X-Requested-With": "XMLHttpRequest",
      Accept: "application/json, text/javascript, */*; q=0.01",
      Host: "www4.icao.int",
      Origin: "https://www.icao.int",
      "Content-Length": "0",
      Referer: "https://www.icao.int/publications/DOC8643/Pages/Search.aspx"
    ]

    options = []

    Pyairwaves.Repo.delete_all(Pyairwaves.Aircraft)
    Logger.info("Table cleaned.")

    {:ok, aircrafts} =
      HTTPoison.post!(url, "", headers, options).body
      |> Jason.decode()

    aircrafts = dedupe_list(aircrafts, %{})

    Enum.map(aircrafts, fn {_icao, ac} -> parse_aircraft(ac) end)
    # Enum.each(aircrafts, fn {})
    |> Enum.chunk_every(1000)
    |> Enum.map(fn chunk ->
      Pyairwaves.Repo.insert_all(Pyairwaves.Aircraft, chunk, on_conflict: :nothing, log: false)
    end)

    Logger.info("Update finished.")
  end
end
