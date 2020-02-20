defmodule Mix.Tasks.Pyairwaves.UpdateAircrafts do
  use Mix.Task

  require Logger

  @moduledoc """
  Update the list of known aircrafts models

  Cron recommanded: run one time per month
  """

  defp parse_aircraft(aircraft) do
    aircraft_shadow = "generic_#{String.slice(aircraft["EngineType"], 0, 1)}#{aircraft["EngineCount"]}#{aircraft["WTC"]}.png"
    %Pyairwaves.Aircraft{
      icao: aircraft["Designator"],
      type: aircraft["ModelFullName"],
      manufacturer: aircraft["ManufacturerCode"],
      aircraft_description: aircraft["AircraftDescription"],
      aircraft_shadow: aircraft_shadow,
      engine_type: aircraft["EngineType"],
      engine_count: aircraft["EngineCount"],
      wake_category: aircraft["WTC"]
    }
  end

  @shortdoc "Update the list of known aircrafts models"
  def run(_) do
    Application.ensure_all_started(:pyairwaves)
    Logger.info("Starting aircrafts update. (Online)")
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

    {:ok, aircrafts} = HTTPoison.post!(url, "", headers, options).body
    |> Jason.decode()

    aircrafts_db = Enum.map(aircrafts, fn ac ->
      parse_aircraft(ac)
    end)

    Pyairwaves.Repo.insert_all(Pyairwaves.Aircraft, aircrafts_db, on_conflict: :nothing)

    Logger.info("Update finished, handled #{length aircrafts} items.")

  end
end
