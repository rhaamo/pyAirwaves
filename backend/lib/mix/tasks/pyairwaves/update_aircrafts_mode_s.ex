defmodule Mix.Tasks.Pyairwaves.UpdateAircraftsModeS do
  use Mix.Task
  import Mix.Tasks.Pyairwaves

  require Logger

  NimbleCSV.define(MyParserModeS, separator: "\t", escape: "½")

  @moduledoc """
  Update the list of aircrafts Owner

  Cron recommanded: run one time per month
  """

  @shortdoc "Update the list of Aircraft Owner"
  def run(_) do
    # start the required apps & repos
    start_apps()

    Logger.info("Starting Aircrafts ModeS update. (online)")
    HTTPoison.start()

    url = "http://data.flightairmap.com/data/modes.tsv.gz"

    Pyairwaves.Repo.delete_all(Pyairwaves.AircraftMode)
    Logger.info("Table cleaned.")

    Pyairwaves.Repo.transaction(
      fn ->
        HTTPoison.get!(url, [], []).body
        |> :zlib.gunzip()
        |> MyParserModeS.parse_string(skip_headers: true)
        |> Enum.map(fn [
                         _first_created,
                         _last_modified,
                         mode_s,
                         mode_s_country,
                         registration,
                         icao_type_code,
                         type_flight
                       ] ->
          %Pyairwaves.AircraftMode{
            updated_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
            inserted_at: NaiveDateTime.truncate(NaiveDateTime.utc_now(), :second),
            mode_s: mode_s,
            mode_s_country: mode_s_country,
            registration: registration,
            icao_type_code: icao_type_code,
            type_flight: type_flight,
            source: "modes.tsv"
          }
        end)
        |> Enum.map(fn item ->
          Pyairwaves.Repo.insert!(item, on_conflict: :nothing, log: false)
        end)
      end,
      timeout: :infinity,
      log: false
    )

    Logger.info("Mode S imported.")
  end
end
